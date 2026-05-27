import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.gamersglobal.de"
DATA_PATH = Path(__file__).parent.parent / "data" / "polls.json"

_MONTHS_DE = {
    "Januar": 1, "Februar": 2, "März": 3, "April": 4,
    "Mai": 5, "Juni": 6, "Juli": 7, "August": 8,
    "September": 9, "Oktober": 10, "November": 11, "Dezember": 12,
}


def parse_archive_page(html: str) -> tuple[list[dict], bool]:
    """Return (polls, has_next). polls = [{"url": str, "title": str}]."""
    soup = BeautifulSoup(html, "html.parser")
    polls = []
    for a in soup.select("h3.title > a"):
        if a.get("href"):
            polls.append({"url": a["href"], "title": a.get_text(strip=True)})
    has_next = bool(soup.select_one("li.pager-next a"))
    return polls, has_next


def parse_poll_page(html: str) -> dict:
    """Return {"title": str, "votes": int, "date": str|None}."""
    soup = BeautifulSoup(html, "html.parser")

    # Title — strip embedded series-info div
    h1 = soup.select_one("h1.title")
    title = ""
    if h1:
        for tag in h1.select(".node-serien-info"):
            tag.decompose()
        title = h1.get_text(strip=True)

    # Votes
    votes = 0
    total_div = soup.select_one("div.total")
    if total_div:
        m = re.search(r"([\d.]+)", total_div.get_text())
        if m:
            votes = int(m.group(1).replace(".", ""))

    # Date — "24. Mai 2026 - 9:00" in div.voll-wer-wann
    date = None
    wer_wann = soup.select_one("div.voll-wer-wann")
    if wer_wann:
        text = wer_wann.get_text(" ", strip=True)
        m = re.search(r"(\d{1,2})\.\s+(\w+)\s+(\d{4})", text)
        if m:
            day, month_str, year = int(m.group(1)), m.group(2), int(m.group(3))
            month = _MONTHS_DE.get(month_str, 0)
            if month:
                date = f"{year:04d}-{month:02d}-{day:02d}"

    return {"title": title, "votes": votes, "date": date}


def fetch_html(url: str) -> str:
    time.sleep(0.5)
    r = requests.get(
        BASE_URL + url,
        headers={"User-Agent": "Mozilla/5.0 (gg-stats-bot/1.0)"},
        timeout=30,
    )
    r.raise_for_status()
    return r.text


def run_initial(data_path: str = str(DATA_PATH)) -> list[dict]:
    """Full crawl — scrapes every page of the archive."""
    all_polls: list[dict] = []
    page = 0
    while True:
        html = fetch_html(f"/exklusiv/sonntagsfrage?page={page}")
        entries, has_next = parse_archive_page(html)
        for e in entries:
            detail = parse_poll_page(fetch_html(e["url"]))
            all_polls.append({
                "date": detail["date"],
                "title": detail["title"],
                "votes": detail["votes"],
                "url": e["url"],
            })
            print(f"  scraped {e['url']} ({detail['votes']} votes)", flush=True)
        print(f"page {page} done ({len(entries)} polls)", flush=True)
        if not has_next:
            break
        page += 1

    all_polls.sort(key=lambda x: x["date"] or "")
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(all_polls, f, indent=2, ensure_ascii=False)
    print(f"wrote {len(all_polls)} polls to {data_path}")
    return all_polls


def run_incremental(data_path: str = str(DATA_PATH)) -> bool:
    """Check the 2 most recent polls; update votes/title if not yet [Ergebnis]."""
    with open(data_path, encoding="utf-8") as f:
        polls: list[dict] = json.load(f)

    existing = {p["url"]: p for p in polls}

    html = fetch_html("/exklusiv/sonntagsfrage?page=0")
    latest, _ = parse_archive_page(html)
    candidates = latest[:2]

    changed = False
    for c in candidates:
        if c["url"] in existing and "[Ergebnis]" in existing[c["url"]]["title"]:
            continue  # already final and known — skip

        detail = parse_poll_page(fetch_html(c["url"]))

        if c["url"] in existing:
            p = existing[c["url"]]
            p["title"] = detail["title"]
            p["votes"] = detail["votes"]
            changed = True
        else:
            polls.append({
                "date": detail["date"],
                "title": detail["title"],
                "votes": detail["votes"],
                "url": c["url"],
            })
            polls.sort(key=lambda x: x["date"] or "")
            changed = True

    if changed:
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(polls, f, indent=2, ensure_ascii=False)

    return changed


def main() -> None:
    with open(DATA_PATH, encoding="utf-8") as f:
        existing = json.load(f)

    if not existing:
        print("No data found — running initial full crawl …")
        run_initial()
    else:
        print("Existing data found — running incremental update …")
        changed = run_incremental()
        print("Changed." if changed else "No changes.")


if __name__ == "__main__":
    main()
