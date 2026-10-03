#!/usr/bin/env python3
"""Scrape GG's monthly "Das spielen unsere User" (DU) galleries.

Writes (data/du/):
  index.json             — galleries with slide metadata (+ DU mentions), stats; loaded by du.html
  games_per_month.json   — game ranking per month (loaded on demand)
  texts/YYYY-MM.json     — slide texts per month (loaded on demand)
  comments/YYYY-MM.json  — user comments per month with matched game keys (loaded on demand)

Raw fields (``user_raw``, ``game``, ``systems``, comment ``text`` …) are stored as
scraped; everything else (canonical users, game keys, previous mentions, stats)
is derived by ``build()`` on every run, so overrides in data/du_overrides.json
apply retroactively.

Run:
    python3 scripts/scrape_du.py              # new galleries + refresh the newest two
    python3 scripts/scrape_du.py --backfill   # (re)scrape every gallery
"""
import argparse
import json
import re
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.gamersglobal.de"
INDEX_PATH = "/exklusiv/das-spielen-unsere-user"
DATA_DIR = Path("data/du")
OVERRIDES_PATH = Path("data/du_overrides.json")

# "Vor 10 Jahren"/"im Jahr 2009" retrospectives are not monthly issues
_SKIP_SLUG_RE = re.compile(r"vor-(?:10|zehn)-jahren|im-jahr-20\d\d")

_GERMAN_MONTHS = {
    "januar": 1, "februar": 2, "märz": 3, "april": 4, "mai": 5, "juni": 6,
    "juli": 7, "august": 8, "september": 9, "oktober": 10, "november": 11, "dezember": 12,
}


# ---------------------------------------------------------------------------
# Systems
# ---------------------------------------------------------------------------

# canonical → variants (casefolded); a variant mapping to None is a known non-system token
_SYSTEM_VARIANTS = {
    "PC": ["pc", "windows", "legion go"],
    "Linux": ["linux"],
    "Mac": ["mac", "macos"],
    "Steam Deck": ["steam deck"],
    "PlayStation": ["playstation", "ps1", "psx"],
    "PlayStation 2": ["playstation 2", "ps2"],
    "PlayStation 3": ["playstation 3", "ps3"],
    "PlayStation 4": ["playstation 4", "ps4", "playstation 4 vr"],
    "PlayStation 5": ["playstation 5", "ps5"],
    "PS Vita": ["psvita", "ps vita", "vita"],
    "PSP": ["psp"],
    "Xbox": ["xbox"],
    "Xbox 360": ["xbox 360"],
    "Xbox One": ["xbox one"],
    "Xbox Series X|S": ["xbox series x", "xbox series s", "xbox series x|s", "xbox series"],
    "Cloud-Gaming": ["xbox cloud gaming", "stadia", "luna", "geforce now"],
    "Switch": ["switch", "nintendo switch"],
    "Switch 2": ["switch 2", "nintendo switch 2"],
    "Wii": ["wii"],
    "Wii U": ["wiiu", "wii u", "wiiu virtual console", "wii u virtual console"],
    "GameCube": ["gamecube"],
    "N64": ["n64", "nintendo 64"],
    "SNES": ["snes", "super nintendo"],
    "NES": ["nes"],
    "Nintendo Classic Mini": ["nintendo classic mini"],
    "Game Boy": ["game boy", "gameboy", "game boy classic"],
    "Game Boy Color": ["game boy color", "game boy colour"],
    "Game Boy Advance": ["game boy advance", "gba"],
    "Game & Watch": ["game & watch"],
    "DS": ["ds", "nds", "nintendo ds"],
    "3DS": ["3ds", "nintendo 3ds"],
    "Mega Drive": ["mega drive", "genesis"],
    "C64": ["c64"],
    "Amiga": ["amiga"],
    "Atari 2600": ["atari 2600"],
    "Arcade": ["arcade"],
    "PC-98": ["pc-98"],
    "iOS": ["ios", "ipad", "iphone"],
    "Android": ["android"],
    "Browser": ["browser", "lichess"],
    "Meta Quest": ["oculus quest 2", "oculus quest", "meta quest", "quest"],
    "Analog": ["tisch", "hand", "halle"],
}
_IGNORED_SYSTEM_TOKENS = {"psvr2", "psvr", "demoversion", "minecraft-modpack", "gzdoom", "erfinder der du"}
_SYSTEM_LOOKUP = {v: canon for canon, vs in _SYSTEM_VARIANTS.items() for v in vs}
_SYSTEM_SPLIT_RE = re.compile(r"\s*(?://|/|,|&(?! watch)|\bund\b)\s*", re.IGNORECASE)

# Patterns for guessing a system from prose (case-sensitive where the word is ambiguous)
_SYSTEM_TEXT_PATTERNS = [
    ("Steam Deck", r"\bSteam[ -]?Deck\b"),
    ("PlayStation 5", r"\b(?:PS ?5|PlayStation ?5)\b"),
    ("PlayStation 4", r"\b(?:PS ?4|PlayStation ?4)\b"),
    ("PlayStation 3", r"\b(?:PS ?3|PlayStation ?3)\b"),
    ("PlayStation 2", r"\b(?:PS ?2|PlayStation ?2)\b"),
    ("PS Vita", r"\b(?:PS ?Vita|Vita)\b"),
    ("Xbox Series X|S", r"\bXbox Series [XS]\b"),
    ("Xbox One", r"\bXbox One\b"),
    ("Xbox 360", r"\bXbox 360\b"),
    ("Switch", r"\b(?:Nintendo )?Switch\b(?! 2)"),
    ("Switch 2", r"\bSwitch 2\b"),
    ("Wii U", r"\bWii ?U\b"),
    ("3DS", r"\b3DS\b"),
    ("Linux", r"\bLinux\b"),
    ("Mac", r"\b(?:Mac|macOS)\b"),
    ("iOS", r"\b(?:iOS|iPad|iPhone)\b"),
    ("Android", r"\bAndroid\b"),
    ("PC", r"\bPC\b(?!-98)"),
]
_SYSTEM_TEXT_RES = [(canon, re.compile(p)) for canon, p in _SYSTEM_TEXT_PATTERNS]


def normalize_systems(raw: str | None) -> list[str]:
    """Map a raw system string like "Xbox 360 und PC" to canonical names (unknown tokens dropped)."""
    if not raw:
        return []
    out = []
    for token in _SYSTEM_SPLIT_RE.split(raw.strip()):
        t = token.strip().casefold()
        if not t or re.fullmatch(r"\d{4}", t) or t in _IGNORED_SYSTEM_TOKENS:
            continue
        canon = _SYSTEM_LOOKUP.get(t)
        if canon and canon not in out:
            out.append(canon)
    return out


def guess_systems_from_text(text: str) -> list[str]:
    """Return the system mentioned first in *text* (empty if none)."""
    best = None
    for canon, rx in _SYSTEM_TEXT_RES:
        m = rx.search(text)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), canon)
    return [best[1]] if best else []


# ---------------------------------------------------------------------------
# Titles and game keys
# ---------------------------------------------------------------------------

_SEPARATORS = (": ", " – ", " — ", " - ")
_NON_ENTRY_RE = re.compile(r"^(?:und (?:was spielst )?du\b|grüße von |vorwort )", re.IGNORECASE)


def _split_title(title: str):
    """Return (user, game, system_raw, separator) or None for non-entry slides."""
    title = (title or "").strip()
    if not title:
        return None
    gg_prefix = title.startswith("GG-User ")
    if gg_prefix:
        title = title[len("GG-User "):]

    system = None
    m = re.search(r"\s*\(([^()]*)\)\s*$", title)
    if m:
        system = m.group(1).strip()
        title = title[: m.start()].strip()

    hits = [(title.find(sep), sep) for sep in _SEPARATORS if title.find(sep) > 0]
    if not hits:
        if system is None:
            return None
        return None, title, system, None
    pos, sep = min(hits)
    sep_kind = "gg" if gg_prefix else sep
    return title[:pos].strip(), title[pos + len(sep):].strip(), system, sep_kind


def parse_slide_title(title: str):
    """Parse "User: Game (System)" and its historic variants → (user, game, system_raw) or None."""
    parts = _split_title(title)
    return parts[:3] if parts else None


def game_key(title: str) -> str:
    """Normalized key: case/separators/punctuation folded."""
    t = re.sub(r"[‘’´`ʼ]", "'", title.casefold())
    t = re.sub(r"[™®©]", "", t)
    t = re.sub(r"[^\w+&']+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# ---------------------------------------------------------------------------
# HTML parsing
# ---------------------------------------------------------------------------

_ALLOWED_TAGS = {"a", "strong", "b", "em", "i", "br", "p", "div", "ul", "ol", "li", "blockquote", "span"}
_DROP_TAGS = {"script", "style", "iframe", "noscript", "form", "img"}


def _abs_url(href: str) -> str:
    return href if href.startswith("http") else BASE_URL + ("" if href.startswith("/") else "/") + href


def _sanitize(node) -> str:
    for tag in node.find_all(True):
        if tag.name in _DROP_TAGS:
            tag.decompose()
    for tag in node.find_all(True):
        if tag.name not in _ALLOWED_TAGS:
            tag.unwrap()
            continue
        href = tag.get("href") if tag.name == "a" else None
        tag.attrs = {"href": _abs_url(href)} if href else {}
    return "".join(str(c) for c in node.contents).strip()


def _parse_comment_date(text: str) -> str | None:
    m = re.search(r"(\d{1,2})\.\s*([A-Za-zäÄ]+)\s+(\d{4})\s*-\s*(\d{1,2}):(\d{2})", text)
    if not m or m.group(2).casefold() not in _GERMAN_MONTHS:
        return None
    d, mon, y, hh, mm = m.groups()
    return f"{y}-{_GERMAN_MONTHS[mon.casefold()]:02d}-{int(d):02d} {int(hh):02d}:{mm}"


def _parse_comments(soup) -> list[dict]:
    comments = []
    for div in soup.select("div.comment"):
        cid = re.sub(r"\D", "", div.get("id", ""))
        author = div.select_one(".author a") or div.select_one(".author")
        content = div.select_one(".comment-content")
        if not content:
            continue
        for q in content.find_all("blockquote"):
            q.decompose()  # quoted text belongs to someone else
        for br in content.find_all("br"):
            br.replace_with("\n")
        paras = content.find_all("p")
        text = "\n".join(p.get_text() for p in paras) if paras else content.get_text()
        infos = div.select_one(".comment-infos")
        comments.append({
            "cid": int(cid) if cid else None,
            "uid": int(div["uid"]) if div.get("uid", "").isdigit() else None,
            "user_raw": author.get_text(strip=True) if author else None,
            "date": _parse_comment_date(infos.get_text(" ", strip=True)) if infos else None,
            "text": text.strip(),
        })
    return comments


def parse_gallery(html: str, url: str) -> dict | None:
    """Parse one DU gallery page. Returns None if it is not a monthly issue."""
    soup = BeautifulSoup(html, "html.parser")
    page_title = soup.title.get_text(strip=True) if soup.title else ""
    m = re.search(r"DU (\d{1,2})/(\d{4})", page_title)
    if not m:
        return None
    month = f"{m.group(2)}-{int(m.group(1)):02d}"
    nid = int(re.search(r"/text-gallery/(\d+)", url).group(1))

    slides_li = soup.select("li.gallery-slide")
    participants = []
    if slides_li and slides_li[0].select_one(".desc"):
        participants = [
            p for p in (s.get_text(strip=True) for s in slides_li[0].select_one(".desc").find_all("strong"))
            if len(p) > 2 and re.search(r"\w", p) and not re.search(r"\bDU\b|spielen unsere User", p)
        ]
    participants_cf = {p.casefold() for p in participants}

    slides = []
    for li in slides_li[1:]:
        h3 = li.find("h3")
        h3_text = h3.get_text(strip=True) if h3 else ""
        desc = li.select_one(".desc")
        desc_text = desc.get_text(" ", strip=True) if desc else ""
        parts = _split_title(h3_text)
        if not parts:
            # bare game title ("Mini Metro, Race the Sun"): accept only if the first
            # sentence names a participant — filters "Und was spielst DU?", "Grüße von …"
            first_sentence = re.split(r"(?<=[.!?])\s", desc_text, maxsplit=1)[0]
            if (not h3_text or _NON_ENTRY_RE.match(h3_text)
                    or not any(p in first_sentence for p in participants)):
                continue
            parts = (None, h3_text, None, None)
        user, game, system_raw, sep = parts

        # dash separators are ambiguous ("Total War - Warhammer 2") — trust only known participants
        if user and sep in (" – ", " — ", " - ") and participants_cf and user.casefold() not in participants_cf:
            user, game = None, f"{user}{sep}{game}"
        if not user:
            if system_raw is not None and not normalize_systems(system_raw):
                continue  # "Vorwort von ChrisL (Erfinder der DU)" etc.
            found = [(desc_text.find(p), p) for p in participants if desc_text.find(p) >= 0]
            user = min(found)[1] if found else None

        systems = normalize_systems(system_raw)
        source = "title" if systems else None
        if not systems:
            systems = guess_systems_from_text(desc_text)
            source = "text" if systems else None

        img = li.find("img")
        slides.append({
            "id": li.get("id"),
            "user_raw": user,
            "game": game,
            "system_raw": system_raw,
            "systems": systems,
            "system_source": source,
            "text_html": _sanitize(desc) if desc else "",
            "image": _abs_url(img["src"]) if img and img.get("src") else None,
        })

    return {
        "month": month,
        "nid": nid,
        "url": url,
        "title": page_title.split(" - Galerie")[0].split(" | ")[0].strip(),
        "slides": slides,
        "comments": _parse_comments(soup),
    }


# ---------------------------------------------------------------------------
# Derivation
# ---------------------------------------------------------------------------

def build_user_aliases(manual: dict[str, list[str]]) -> dict[str, str]:
    """old name → canonical name, from data/du_overrides.json.

    Not derivable automatically: GG renders old comments under the author's *current*
    name, and slide titles (which keep the old name) carry no user id.
    """
    return {old: canon for canon, olds in manual.items() for old in olds if old != canon}


_MIN_MATCH_LEN = 4


def build_title_matcher(titles, usernames: set[str], stopwords: set[str] = frozenset()):
    """Compile one regex over all normalized titles (longest first)."""
    keys = {game_key(t) for t in titles}
    keys = {k for k in keys if len(k) >= _MIN_MATCH_LEN and k not in usernames and k not in stopwords}
    if not keys:
        return None
    alts = sorted(keys, key=len, reverse=True)
    return re.compile(r"(?<![\w])(?:" + "|".join(re.escape(k) for k in alts) + r")(?![\w])")


def match_games(text: str, matcher) -> set[str]:
    if matcher is None or not text:
        return set()
    return set(matcher.findall(game_key(text)))


def build(galleries: list[dict], overrides: dict) -> dict:
    """Derive canonical users, game keys, previous mentions and stats from raw galleries."""
    galleries = sorted(galleries, key=lambda g: (g["month"], g["nid"]))
    aliases = build_user_aliases(overrides.get("user_aliases", {}))
    game_aliases = {game_key(v): game_key(c) for c, vs in overrides.get("game_aliases", {}).items() for v in vs}

    def canon_user(name):
        return aliases.get(name, name) if name else None

    def canon_key(game):
        k = game_key(game)
        return game_aliases.get(k, k)

    out_galleries = []
    names_by_key: dict[str, Counter] = defaultdict(Counter)
    slides_by_key: dict[str, list[tuple[str, str]]] = defaultdict(list)  # key → [(month, slide_id)]
    for g in galleries:
        slides = []
        for s in g["slides"]:
            key = canon_key(s["game"])
            names_by_key[key][s["game"]] += 1
            slides.append({**s, "user": canon_user(s["user_raw"]), "game_key": key})
        out_galleries.append({k: v for k, v in g.items() if k != "comments"} | {"slides": slides})

    for g in out_galleries:
        for s in g["slides"]:
            s["previous"] = [sid for (m, sid) in slides_by_key[s["game_key"]] if m < g["month"]]
            s["same_month"] = [o["id"] for o in g["slides"] if o["game_key"] == s["game_key"] and o["id"] != s["id"]]
        for s in g["slides"]:
            slides_by_key[s["game_key"]].append((g["month"], s["id"]))

    games = {k: c.most_common(1)[0][0] for k, c in names_by_key.items()}
    usernames = {game_key(u) for g in out_galleries for s in g["slides"] if s["user"] for u in [s["user"]]}
    usernames |= {game_key(c["user_raw"]) for g in galleries for c in g.get("comments", []) if c.get("user_raw")}
    stopwords = {game_key(w) for w in overrides.get("comment_match_stopwords", [])}
    matcher = build_title_matcher(
        [*games.values(), *(v for vs in overrides.get("game_aliases", {}).values() for v in vs)],
        usernames=usernames, stopwords=stopwords,
    )

    comments_out = {}
    games_per_month = {}
    systems_per_month = {}
    systems_per_user: dict[str, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    for raw, g in zip(galleries, out_galleries):
        month = g["month"]
        du_users: dict[str, set] = defaultdict(set)
        sys_count = Counter()
        for s in g["slides"]:
            du_users[s["game_key"]].add(s["user"] or f"?{s['id']}")
            for sysname in s["systems"] or ["unbekannt"]:
                sys_count[sysname] += 1
                if s["user"]:
                    systems_per_user[s["user"]][month][sysname] += 1
        systems_per_month[month] = dict(sys_count)

        com_users: dict[str, set] = defaultdict(set)
        month_comments = comments_out.setdefault(month, [])
        for c in raw.get("comments", []):
            user = canon_user(c.get("user_raw"))
            keys = sorted({game_aliases.get(k, k) for k in match_games(c.get("text", ""), matcher)})
            month_comments.append({**c, "user": user, "games": keys})
            for k in keys:
                com_users[k].add(user)

        rows = []
        for k in du_users.keys() | com_users.keys():
            rows.append({
                "key": k,
                "game": games.get(k, k),
                "du": len(du_users[k]),
                "comments": len(com_users[k]),
                "total": len(du_users[k] | com_users[k]),
            })
        rows.sort(key=lambda r: (-r["total"], -r["du"], r["game"].casefold()))
        games_per_month[month] = rows

    return {
        "galleries": out_galleries,
        "comments": comments_out,
        "games": games,
        "user_aliases": aliases,
        "stats": {
            "games_per_month": games_per_month,
            "systems_per_month": systems_per_month,
            "systems_per_user": {u: {m: dict(c) for m, c in sorted(ms.items())} for u, ms in sorted(systems_per_user.items())},
        },
    }


# ---------------------------------------------------------------------------
# Fetching / discovery
# ---------------------------------------------------------------------------

def fetch_html(url: str, cache_dir: Path | None = None, use_cache: bool = True) -> str:
    cache_file = None
    m = re.search(r"/text-gallery/(\d+)", url)
    if cache_dir and m:
        cache_file = cache_dir / f"{m.group(1)}.html"
        if use_cache and cache_file.exists():
            return cache_file.read_text()
    time.sleep(0.5)
    r = requests.get(_abs_url(url), headers={"User-Agent": "Mozilla/5.0 (gg-stats-bot/1.0)"}, timeout=30)
    r.raise_for_status()
    if cache_file:
        cache_file.write_text(r.text)
    return r.text


def discover_galleries(known_urls: set[str], backfill: bool) -> list[str]:
    """Gallery URLs from the DU index pages (newest first). Stops early unless backfilling."""
    urls: list[str] = []
    for page in range(0, 100):
        html = fetch_html(f"{INDEX_PATH}?page={page}")
        found = []
        for path in re.findall(r'href="(/text-gallery/\d+/[^"#?]+)"', html):
            if "/du-" in path and not _SKIP_SLUG_RE.search(path) and path not in urls and path not in found:
                found.append(path)
        if not found:
            break
        urls.extend(found)
        if not backfill and all(u in known_urls for u in found):
            break
    return urls


_DERIVED_SLIDE = {"user", "game_key", "previous", "same_month"}
_DERIVED_COMMENT = {"user", "games"}


def _dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def save_outputs(out: dict, base: Path, now: str) -> None:
    """Split build() output into a small index plus per-month texts and comments."""
    galleries = []
    for g in out["galleries"]:
        _dump(base / "texts" / f"{g['month']}.json", {s["id"]: s.get("text_html", "") for s in g["slides"]})
        _dump(base / "comments" / f"{g['month']}.json", out["comments"].get(g["month"], []))
        slides = [{k: v for k, v in s.items() if k != "text_html"} for s in g["slides"]]
        galleries.append({**g, "slides": slides, "comment_count": len(out["comments"].get(g["month"], []))})
    stats = dict(out["stats"])
    _dump(base / "games_per_month.json", stats.pop("games_per_month"))  # only needed by one tab
    _dump(base / "index.json", {
        "last_updated": now,
        "galleries": galleries,
        "games": out["games"],
        "user_aliases": out["user_aliases"],
        "stats": stats,
    })


def load_raw(base: Path) -> list[dict]:
    """Inverse of save_outputs: raw galleries (derived fields stripped) for re-building."""
    index_path = base / "index.json"
    if not index_path.exists():
        return []
    galleries = []
    for g in json.loads(index_path.read_text())["galleries"]:
        month = g["month"]
        texts_path, comments_path = base / "texts" / f"{month}.json", base / "comments" / f"{month}.json"
        texts = json.loads(texts_path.read_text()) if texts_path.exists() else {}
        comments = json.loads(comments_path.read_text()) if comments_path.exists() else []
        galleries.append({
            **{k: v for k, v in g.items() if k != "comment_count"},
            "slides": [
                {**{k: v for k, v in s.items() if k not in _DERIVED_SLIDE}, "text_html": texts.get(s["id"], "")}
                for s in g["slides"]
            ],
            "comments": [{k: v for k, v in c.items() if k not in _DERIVED_COMMENT} for c in comments],
        })
    return galleries


def run(backfill: bool = False, cache_dir: Path | None = None, refresh_latest: int = 2) -> None:
    galleries = {g["url"]: g for g in load_raw(DATA_DIR)}
    print(f"Loaded {len(galleries)} existing galleries.", flush=True)

    urls = discover_galleries(set(galleries), backfill)
    newest_known = sorted(galleries.values(), key=lambda g: g["month"])[-refresh_latest:] if galleries else []
    to_fetch = [u for u in urls if backfill or u not in galleries]
    to_fetch += [g["url"] for g in newest_known if g["url"] not in to_fetch]

    for url in to_fetch:
        refresh = url in galleries  # comments may have grown → bypass cache
        print(f"  fetching {url} …", flush=True)
        g = parse_gallery(fetch_html(url, cache_dir, use_cache=not refresh), url)
        if g is None:
            print("    [skip] not a monthly issue", flush=True)
            continue
        print(f"    {g['month']}: {len(g['slides'])} slides, {len(g['comments'])} comments", flush=True)
        galleries[url] = g

    months = Counter(g["month"] for g in galleries.values())
    dupes = [m for m, n in months.items() if n > 1]
    if dupes:
        print(f"  [warn] several galleries for month(s): {sorted(dupes)}", flush=True)

    overrides = json.loads(OVERRIDES_PATH.read_text()) if OVERRIDES_PATH.exists() else {}
    out = build(list(galleries.values()), overrides)

    unknown = Counter(
        s.get("system_raw") for g in out["galleries"] for s in g["slides"]
        if s.get("system_raw") and not normalize_systems(s["system_raw"])
    )
    if unknown:
        print(f"  [info] unmapped system strings: {dict(unknown)}", flush=True)
    if out["user_aliases"]:
        print(f"  user renames: {out['user_aliases']}", flush=True)

    save_outputs(out, DATA_DIR, now=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    n_slides = sum(len(g["slides"]) for g in out["galleries"])
    print(f"Saved {len(out['galleries'])} galleries / {n_slides} slides to {DATA_DIR}/", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape GG 'Das spielen unsere User' galleries.")
    parser.add_argument("--backfill", action="store_true", help="Scrape every gallery, not just new ones.")
    parser.add_argument("--cache-dir", type=Path, help="Read/write raw gallery HTML here (avoids refetching).")
    args = parser.parse_args()
    if args.cache_dir:
        args.cache_dir.mkdir(parents=True, exist_ok=True)
    run(backfill=args.backfill, cache_dir=args.cache_dir)


if __name__ == "__main__":
    main()
