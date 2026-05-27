"""Scraper for GG 'Darauf freut sich die Redaktion im [Month] [Year]' articles.

Usage:
    python scrape_freude.py               # incremental (current + previous month)
    python scrape_freude.py --backfill    # discover and scrape all historical articles
    python scrape_freude.py --enrich      # also run LLM enrichment on comments
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.gamersglobal.de"
DATA_PATH = Path(__file__).parent.parent / "data" / "vorfreude.json"
CSV_PATH = Path(__file__).parent.parent / "data" / "vorfreude.csv"

# German month names → month number (for title parsing)
_MONTHS_DE_NUM = {
    "Januar": 1, "Februar": 2, "März": 3, "April": 4,
    "Mai": 5, "Juni": 6, "Juli": 7, "August": 8,
    "September": 9, "Oktober": 10, "November": 11, "Dezember": 12,
}

# German month names → URL slug and vice versa
_MONTHS_SLUG_TO_NUM = {
    "januar": 1, "februar": 2, "maerz": 3, "april": 4,
    "mai": 5, "juni": 6, "juli": 7, "august": 8,
    "september": 9, "oktober": 10, "november": 11, "dezember": 12,
}
_MONTHS_NUM_TO_SLUG = {v: k for k, v in _MONTHS_SLUG_TO_NUM.items()}

# Known GG editors — strong signal for editor detection
KNOWN_EDITORS = {
    "Jörg Langer", "Michael Trier", "Andreas Göß", "Benjamin Braun",
    "Peter Bathge", "Matthias Schmid", "Petra Schmid", "Mathias Dietrich",
    "Tobias Rauscher", "Hagen Gehritz", "Kai Schmidt", "Christian Burtchen",
    "Michael Hengst", "Jens Bremicker",
}

# Category detection patterns
_CAT_FILM = re.compile(r"\[?FILME?(?:/SERIEN?)?\]?", re.IGNORECASE)
_CAT_GAME = re.compile(r"\[?(?:SPIELE?(?:/BRETTSPIELE?)?|BRETTSPIELE?)\]?", re.IGNORECASE)
_CAT_MISC = re.compile(r"\[?SONSTIGES?\]?", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Public helpers (also used by tests)
# ---------------------------------------------------------------------------

def _month_to_slug(month: str) -> str:
    """Convert 'YYYY-MM' to German URL slug 'monat-YYYY'."""
    year, m = month.split("-")
    slug = _MONTHS_NUM_TO_SLUG[int(m)]
    return f"{slug}-{year}"


def _slug_to_month(slug: str, year: str) -> str:
    """Convert German month slug + year string to 'YYYY-MM'."""
    m = _MONTHS_SLUG_TO_NUM.get(slug.lower())
    if m is None:
        return ""
    return f"{year}-{m:02d}"


def _detect_month_from_title(title: str) -> str:
    """Extract 'YYYY-MM' from article title like 'Darauf freut sich die Redaktion im... Mai 2026'."""
    # Try 'im Mai 2026' or 'im... Mai 2026'
    m = re.search(r"im\.{0,3}\s+(\w+)\s+(\d{4})", title, re.IGNORECASE)
    if m:
        month_str, year = m.group(1), m.group(2)
        # Try German name
        for de_name, num in _MONTHS_DE_NUM.items():
            if de_name.lower() == month_str.lower():
                return f"{year}-{num:02d}"
    return ""


def _detect_category(text: str) -> str | None:
    """Return category string if text contains a category label, else None."""
    if _CAT_FILM.search(text):
        return "film_series"
    if _CAT_GAME.search(text):
        return "game"
    if _CAT_MISC.search(text):
        return "misc"
    return None


def _is_category_label(text: str) -> bool:
    """Return True if text is purely a category label (not an item title)."""
    stripped = text.strip().strip("[]").upper()
    return stripped in {
        "FILME/SERIEN", "FILME", "SERIEN", "SPIELE/BRETTSPIELE",
        "SPIELE", "BRETTSPIELE", "SONSTIGES",
    }


def _is_editor_name(tag) -> str | None:
    """
    If tag is (or contains) an editor name, return the name string; else return None.
    Editor sections are marked by <u> tags (possibly with <strong> inside).
    """
    if tag.name != "u":
        return None
    name = tag.get_text(strip=True)
    if not name:
        return None
    # Must look like a name: not a category label, not all-caps bracket text
    if "[" in name or "]" in name:
        return None
    if len(name) > 50:
        return None
    return name


# ---------------------------------------------------------------------------
# Core parse functions
# ---------------------------------------------------------------------------

def parse_article(html: str) -> dict:
    """Parse a 'Darauf freut sich' article.

    Returns::
        {
            "title": str,
            "month": "YYYY-MM",
            "editors": [{"name": str, "items": [{"title": str, "category": str}]}]
        }
    """
    soup = BeautifulSoup(html, "html.parser")

    # Title
    h1 = soup.select_one("div.node-news h1.title") or soup.select_one("h1.title")
    title = h1.get_text(strip=True) if h1 else ""
    month = _detect_month_from_title(title)

    # Article body
    news_body = soup.select_one("div.node-news div.news-body") or soup.select_one("div.news-body")
    if not news_body:
        return {"title": title, "month": month, "editors": []}

    editors: list[dict] = []
    current_editor: str | None = None
    current_items: list[dict] = []
    current_category: str = "unknown"

    def _flush_editor():
        nonlocal current_editor, current_items
        if current_editor:
            editors.append({"name": current_editor, "items": list(current_items)})
        current_editor = None
        current_items = []

    # Walk ALL descendants including NavigableString nodes.
    # The category labels like "[SPIELE/BRETTSPIELE]" appear as raw text nodes,
    # while item titles appear in <strong> / <em> tags.
    from bs4 import NavigableString, Tag as BS4Tag

    for node in news_body.descendants:
        if isinstance(node, BS4Tag):
            tag = node

            # Detect new editor section via <u> tag
            if tag.name == "u":
                name = _is_editor_name(tag)
                if name:
                    _flush_editor()
                    current_editor = name
                    current_category = "unknown"
                continue  # don't process <u> children separately

            if current_editor is None:
                continue

            # Collect items from <strong> and <em> tags
            if tag.name in ("strong", "em"):
                item_text = tag.get_text(strip=True)
                # Skip empty, very short, or category labels
                if len(item_text) <= 2:
                    continue
                if _is_category_label(item_text):
                    continue
                # Skip editor names (inside a <u> ancestor, e.g. <u><strong>…</strong></u>
                # or deeper nesting like <u><strong><em>…</em></strong></u>)
                if tag.find_parent("u"):
                    continue

                current_items.append({"title": item_text, "category": current_category})

        elif isinstance(node, NavigableString):
            # Skip NavigableString nodes that are children of a <u> tag —
            # they are editor-name text, not category labels or item titles.
            if node.parent and node.parent.name == "u":
                continue
            text = str(node)
            # Category labels live as plain text nodes at the body level
            cat = _detect_category(text)
            if cat:
                current_category = cat

    _flush_editor()

    return {"title": title, "month": month, "editors": editors}


def parse_comments(html: str) -> list[dict]:
    """Parse all comments from article HTML.

    Returns list of ``{"username": str, "text": str}`` with one entry per
    unique username (multiple comments concatenated with double newline).
    """
    soup = BeautifulSoup(html, "html.parser")
    comment_divs = soup.find_all("div", class_="comment")

    # username → list of comment texts
    user_texts: dict[str, list[str]] = {}

    for div in comment_divs:
        # Extract username: first <a> in .comment-infos > .author span
        username = None
        author_span = div.select_one(".comment-infos .author a")
        if author_span:
            username = author_span.get_text(strip=True)
        if not username:
            # Fallback: first link in comment-infos
            info_div = div.select_one(".comment-infos")
            if info_div:
                a = info_div.find("a")
                if a:
                    username = a.get_text(strip=True)
        if not username:
            continue

        # Extract comment body text
        content_div = div.select_one(".comment-content") or div.select_one(".comment-body")
        if not content_div:
            continue
        text = content_div.get_text(separator="\n", strip=True)
        if not text:
            continue

        if username not in user_texts:
            user_texts[username] = []
        user_texts[username].append(text)

    return [
        {"username": uname, "text": "\n\n".join(texts)}
        for uname, texts in user_texts.items()
    ]


def compute_stats(
    editors: list[dict],
    user_items: list[dict],
) -> dict:
    """Compute per-item statistics across editor and user mentions.

    Returns::
        {
            "Item Title": {
                "count": int,        # distinct mentioners
                "category": str,
                "mentioners": [str]  # e.g. "editor:joerg_langer", "user:foo"
            }
        }
    """
    # item_title → {"category": str, "mentioners": set}
    stats: dict[str, dict] = {}

    def _add_item(title: str, category: str, mentioner_key: str) -> None:
        if title not in stats:
            stats[title] = {"category": category, "mentioners": set()}
        stats[title]["mentioners"].add(mentioner_key)
        # Update category (last write wins — fine for our use case)
        stats[title]["category"] = category

    for editor in editors:
        name = editor.get("name", "")
        key = "editor:" + name.lower().replace(" ", "_")
        for item in editor.get("items", []):
            _add_item(item["title"], item["category"], key)

    for user_entry in user_items:
        username = user_entry.get("username", "")
        key = "user:" + username
        for item in user_entry.get("items", []):
            _add_item(item["title"], item["category"], key)

    # Convert sets to lists and add count
    return {
        title: {
            "count": len(data["mentioners"]),
            "category": data["category"],
            "mentioners": sorted(data["mentioners"]),
        }
        for title, data in stats.items()
    }


# ---------------------------------------------------------------------------
# Network helpers
# ---------------------------------------------------------------------------

def fetch_html(url: str) -> str:
    """Fetch URL (relative or absolute) and return HTML string."""
    time.sleep(0.5)
    full_url = url if url.startswith("http") else BASE_URL + url
    r = requests.get(
        full_url,
        headers={"User-Agent": "Mozilla/5.0 (gg-stats-bot/1.0)"},
        timeout=30,
    )
    r.raise_for_status()
    return r.text


def _count_comments_in_html(html: str) -> int:
    soup = BeautifulSoup(html, "html.parser")
    return len(soup.find_all("div", class_="comment"))


# ---------------------------------------------------------------------------
# Article discovery
# ---------------------------------------------------------------------------

def discover_articles(existing_months: set[str], backfill: bool = False) -> list[dict]:
    """Discover new 'Darauf freut sich' articles.

    Returns list of ``{"url": str, "month": "YYYY-MM"}`` for months not in
    *existing_months*.
    """
    found: dict[str, str] = {}  # month → url

    title_pattern = re.compile(
        r"darauf\s+freut\s+sich\s+die\s+redaktion", re.IGNORECASE
    )
    url_pattern = re.compile(
        r"/news/(\d+)/darauf-freut-sich-die-redaktion-im-([a-z]+)-(\d{4})"
    )

    def _try_url(candidate_url: str) -> dict | None:
        """Try fetching a candidate URL; return {url, month} on success."""
        try:
            html = fetch_html(candidate_url)
            soup = BeautifulSoup(html, "html.parser")
            h1 = soup.select_one("div.node-news h1.title") or soup.select_one("h1.title")
            if not h1:
                return None
            title_text = h1.get_text(strip=True)
            if not title_pattern.search(title_text):
                return None
            month = _detect_month_from_title(title_text)
            if not month:
                return None
            actual_url = candidate_url
            # Normalise to relative path
            if actual_url.startswith(BASE_URL):
                actual_url = actual_url[len(BASE_URL):]
            return {"url": actual_url, "month": month}
        except Exception:
            return None

    def _scan_page(html: str) -> None:
        """Scan HTML for links matching the vorfreude URL pattern."""
        for m in url_pattern.finditer(html):
            slug_month = m.group(2)
            year = m.group(3)
            month = _slug_to_month(slug_month, year)
            url = m.group(0)
            if month and month not in found:
                found[month] = url

    # 1. Try the GG news listing pages for pattern matches
    max_pages = 50 if backfill else 5
    for page in range(max_pages):
        try:
            html = fetch_html(f"/news?page={page}")
            _scan_page(html)
            soup = BeautifulSoup(html, "html.parser")
            # Stop paginating if no more pages
            if not soup.select_one("li.pager-next"):
                break
        except Exception:
            break

    # Filter out already-known months
    result = [
        {"url": url, "month": month}
        for month, url in sorted(found.items())
        if month not in existing_months
    ]
    return result


# ---------------------------------------------------------------------------
# LLM enrichment
# ---------------------------------------------------------------------------

def enrich_comments(
    comments: list[dict],
    editor_items: list[dict],
    api_key: str,
) -> list[dict]:
    """Use Claude Haiku to extract items from comments.

    Returns list of ``{"username": str, "items": [{"title": str, "category": str}]}``.
    Only non-empty comments are processed; users with no extracted items are omitted.
    """
    import anthropic  # noqa: PLC0415 — imported only when --enrich is used

    client = anthropic.Anthropic(api_key=api_key)

    # Build seed context listing known editor items
    seed_lines = []
    for editor in editor_items:
        for item in editor.get("items", []):
            seed_lines.append(f"- {item['title']} ({item['category']})")
    seed_context = "\n".join(seed_lines) if seed_lines else "(no editor items)"

    system_text = (
        "You are a structured-data extractor for a German gaming website.\n"
        "Users comment on a monthly article where editors share what they are looking"
        " forward to (games, films/series, miscellaneous).\n\n"
        "Known items already mentioned by editors:\n"
        f"{seed_context}\n\n"
        "Your task: Given a user comment, extract any items the user is looking forward"
        " to. Return ONLY a JSON array of objects with keys 'title' (string) and"
        " 'category' (one of: game, film_series, misc, unknown).\n"
        "If no items are found, return an empty array [].\n"
        "Respond only with the JSON array, no other text."
    )

    results: list[dict] = []

    for comment in comments:
        username = comment.get("username", "")
        text = comment.get("text", "").strip()
        if len(text) < 20:
            continue

        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=512,
                system=[
                    {
                        "type": "text",
                        "text": system_text,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=[
                    {"role": "user", "content": text}
                ],
            )
            raw = response.content[0].text.strip()
            items = json.loads(raw)
            if not isinstance(items, list):
                items = []
        except Exception as exc:
            print(f"  [warn] enrich failed for {username}: {exc}", flush=True)
            items = []

        if items:
            results.append({"username": username, "items": items})

    return results


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def _load_data(path: Path) -> list[dict]:
    if path.exists() and path.stat().st_size > 4:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
    return []


def _save_data(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _save_csv(path: Path, data: list[dict]) -> None:
    """Regenerate vorfreude.csv from JSON data."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for entry in data:
        stats = entry.get("item_stats", {})
        for item_title, stat in stats.items():
            mentioners = stat.get("mentioners", [])
            editor_count = sum(1 for m in mentioners if m.startswith("editor:"))
            user_count = sum(1 for m in mentioners if m.startswith("user:"))
            rows.append({
                "month": entry["month"],
                "item_title": item_title,
                "category": stat.get("category", "unknown"),
                "count": stat.get("count", 0),
                "editor_count": editor_count,
                "user_count": user_count,
            })

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["month", "item_title", "category", "count", "editor_count", "user_count"],
        )
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Main scraping logic
# ---------------------------------------------------------------------------

def _scrape_article(url: str, existing_entry: dict | None, enrich: bool, api_key: str) -> dict:
    """Fetch and parse a single article, returning a complete entry dict."""
    print(f"  fetching {url} …", flush=True)
    html = fetch_html(url)

    comment_count = _count_comments_in_html(html)
    parsed = parse_article(html)
    comments_raw = parse_comments(html)

    # Use existing editor items if comment count unchanged and editors already populated
    reuse_user_items = False
    if (
        existing_entry
        and existing_entry.get("editors")
        and existing_entry.get("comment_count") == comment_count
    ):
        print(f"    comment count unchanged ({comment_count}) — reusing editors", flush=True)
        editors = existing_entry["editors"]
        user_items = existing_entry.get("user_items", [])
        # If user_items are already populated, skip re-enrichment and reuse stored comments_raw
        if user_items:
            reuse_user_items = True
            comments_raw = existing_entry.get("comments_raw", comments_raw)
        # else: keep freshly parsed comments_raw so enrichment can still run
    else:
        editors = parsed["editors"]
        user_items = []
        print(
            f"    parsed {len(editors)} editors, {comment_count} comments",
            flush=True,
        )

    # LLM enrichment — skip when comment count is unchanged and user_items already exist
    if enrich and comments_raw and not reuse_user_items:
        print(f"    enriching {len(comments_raw)} user comments …", flush=True)
        user_items = enrich_comments(comments_raw, editors, api_key)
        print(f"    extracted items from {len(user_items)} users", flush=True)
    elif enrich and reuse_user_items:
        print(
            f"    skipping enrichment — comment count unchanged and user_items already populated",
            flush=True,
        )

    item_stats = compute_stats(editors, user_items)

    entry: dict = {
        "month": parsed["month"] or (existing_entry or {}).get("month", ""),
        "url": url,
        "title": parsed["title"],
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "comment_count": comment_count,
        "editors": editors,
        "comments_raw": comments_raw,
        "user_items": user_items,
        "item_stats": item_stats,
    }
    return entry


def run(
    data_path: Path = DATA_PATH,
    csv_path: Path = CSV_PATH,
    backfill: bool = False,
    enrich: bool = False,
    api_key: str = "",
) -> None:
    """Main entry point."""
    existing_data = _load_data(data_path)
    existing_by_month: dict[str, dict] = {e["month"]: e for e in existing_data}
    existing_months = set(existing_by_month.keys())

    print(f"Loaded {len(existing_data)} existing entries.", flush=True)

    # Discover new articles
    print("Discovering articles …", flush=True)
    new_articles = discover_articles(existing_months, backfill=backfill)
    print(f"Found {len(new_articles)} new articles.", flush=True)

    updated_data = list(existing_data)

    for article in new_articles:
        url = article["url"]
        month = article["month"]
        existing_entry = existing_by_month.get(month)
        entry = _scrape_article(url, existing_entry, enrich, api_key)

        # Upsert
        if existing_entry:
            idx = next(i for i, e in enumerate(updated_data) if e["month"] == month)
            updated_data[idx] = entry
        else:
            updated_data.append(entry)

    # Re-check existing entries for comment updates (even if not newly discovered)
    if not backfill:
        # Check current and previous month
        now = datetime.now(timezone.utc)
        for delta in range(2):
            year = now.year
            m = now.month - delta
            if m <= 0:
                m += 12
                year -= 1
            month_str = f"{year}-{m:02d}"
            if month_str in existing_by_month and month_str not in {a["month"] for a in new_articles}:
                existing_entry = existing_by_month[month_str]
                url = existing_entry.get("url", "")
                if not url:
                    continue
                print(f"Checking existing entry {month_str} for updates …", flush=True)
                entry = _scrape_article(url, existing_entry, enrich, api_key)
                idx = next(i for i, e in enumerate(updated_data) if e["month"] == month_str)
                updated_data[idx] = entry

    # Sort by month
    updated_data.sort(key=lambda e: e.get("month", ""))

    # Save JSON
    _save_data(data_path, updated_data)
    print(f"Saved {len(updated_data)} entries to {data_path}", flush=True)

    # Save CSV
    _save_csv(csv_path, updated_data)
    print(f"Saved CSV to {csv_path}", flush=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape GG 'Darauf freut sich die Redaktion' articles."
    )
    parser.add_argument(
        "--backfill",
        action="store_true",
        help="Discover and scrape all historical articles.",
    )
    parser.add_argument(
        "--enrich",
        action="store_true",
        help="Use Claude Haiku to extract items from user comments.",
    )
    parser.add_argument(
        "--no-enrich",
        action="store_true",
        help="Explicitly disable enrichment (no-op when --enrich is not set; useful in scripts).",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var).",
    )
    args = parser.parse_args()

    # --no-enrich explicitly overrides --enrich if both are somehow passed
    enrich = args.enrich and not args.no_enrich

    api_key = args.api_key
    if not api_key and enrich:
        import os
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            parser.error("--enrich requires ANTHROPIC_API_KEY env var or --api-key flag.")

    run(
        backfill=args.backfill,
        enrich=enrich,
        api_key=api_key,
    )


if __name__ == "__main__":
    main()
