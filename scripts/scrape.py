import re
from pathlib import Path

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
