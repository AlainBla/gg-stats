import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import json, pytest
from pathlib import Path
from scrape import parse_archive_page, parse_poll_page

ARCHIVE_HTML = """
<div class="view-content">
  <div class="views-row">
    <h3 class="title"><a href="/news/100/sonntagsfrage-foo-ergebnis">Sonntagsfrage: Foo? [Ergebnis]</a></h3>
  </div>
  <div class="views-row">
    <h3 class="title"><a href="/news/101/sonntagsfrage-bar">Sonntagsfrage: Bar?</a></h3>
  </div>
</div>
<ul class="pager"><li class="pager-next"><a href="?page=2">weiter ›</a></li></ul>
"""

ARCHIVE_HTML_LAST = """
<div class="view-content">
  <div class="views-row">
    <h3 class="title"><a href="/news/1/sonntagsfrage-old-ergebnis">Sonntagsfrage: Old? [Ergebnis]</a></h3>
  </div>
</div>
"""

POLL_HTML = """
<h1 class="title">Sonntagsfrage: Foo? [Ergebnis]<div class="node-serien-info">Teil der Exklusiv-Serie <a href="/exklusiv/sonntagsfrage">Sonntagsfrage</a></div></h1>
<div class="voll-wer-wann">
  <div class="picture">x</div>
  24. Mai 2026 - 9:00
  <span>— vor 1 Tag zuletzt aktualisiert</span>
</div>
<div class="total">
  Gesamte Stimmenzahl: 481
</div>
"""

POLL_HTML_ZERO = """
<h1 class="title">Sonntagsfrage: Baz?</h1>
<div class="voll-wer-wann">3. Januar 2016 - 9:00</div>
<div class="total">Gesamte Stimmenzahl: 0</div>
"""

POLL_HTML_THOUSANDS = """
<h1 class="title">Sonntagsfrage: Big?</h1>
<div class="voll-wer-wann">10. März 2015 - 9:00</div>
<div class="total">Gesamte Stimmenzahl: 1.234</div>
"""


def test_parse_archive_returns_polls():
    polls, has_next = parse_archive_page(ARCHIVE_HTML)
    assert len(polls) == 2
    assert polls[0]["url"] == "/news/100/sonntagsfrage-foo-ergebnis"
    assert polls[0]["title"] == "Sonntagsfrage: Foo? [Ergebnis]"
    assert polls[1]["url"] == "/news/101/sonntagsfrage-bar"


def test_parse_archive_has_next():
    _, has_next = parse_archive_page(ARCHIVE_HTML)
    assert has_next is True


def test_parse_archive_no_next():
    _, has_next = parse_archive_page(ARCHIVE_HTML_LAST)
    assert has_next is False


def test_parse_poll_votes():
    r = parse_poll_page(POLL_HTML)
    assert r["votes"] == 481


def test_parse_poll_date():
    r = parse_poll_page(POLL_HTML)
    assert r["date"] == "2026-05-24"


def test_parse_poll_date_januar():
    r = parse_poll_page(POLL_HTML_ZERO)
    assert r["date"] == "2016-01-03"


def test_parse_poll_title_strips_series_info():
    r = parse_poll_page(POLL_HTML)
    assert r["title"] == "Sonntagsfrage: Foo? [Ergebnis]"
    assert "Exklusiv-Serie" not in r["title"]


def test_parse_poll_zero_votes():
    r = parse_poll_page(POLL_HTML_ZERO)
    assert r["votes"] == 0


def test_parse_poll_votes_thousands_separator():
    r = parse_poll_page(POLL_HTML_THOUSANDS)
    assert r["votes"] == 1234


# ── run logic tests ────────────────────────────────────────────────────────

from scrape import run_incremental

ARCHIVE_BOTH_FINAL = """
<div class="view-content">
  <div class="views-row">
    <h3 class="title"><a href="/news/101/sonntagsfrage-bar-ergebnis">Sonntagsfrage: Bar? [Ergebnis]</a></h3>
  </div>
  <div class="views-row">
    <h3 class="title"><a href="/news/100/sonntagsfrage-foo-ergebnis">Sonntagsfrage: Foo? [Ergebnis]</a></h3>
  </div>
</div>
"""

ARCHIVE_ONE_PENDING = """
<div class="view-content">
  <div class="views-row">
    <h3 class="title"><a href="/news/102/sonntagsfrage-new">Sonntagsfrage: New?</a></h3>
  </div>
  <div class="views-row">
    <h3 class="title"><a href="/news/101/sonntagsfrage-bar-ergebnis">Sonntagsfrage: Bar? [Ergebnis]</a></h3>
  </div>
</div>
"""

POLL_HTML_NEW = """
<h1 class="title">Sonntagsfrage: New?</h1>
<div class="voll-wer-wann">1. Juni 2026 - 9:00</div>
<div class="total">Gesamte Stimmenzahl: 350</div>
"""

POLL_HTML_BAR_FINAL = """
<h1 class="title">Sonntagsfrage: Bar? [Ergebnis]</h1>
<div class="voll-wer-wann">25. Mai 2026 - 9:00</div>
<div class="total">Gesamte Stimmenzahl: 400</div>
"""


def _make_db(tmp_path, polls):
    p = tmp_path / "polls.json"
    p.write_text(json.dumps(polls, ensure_ascii=False))
    return str(p)


def test_incremental_skips_both_final(tmp_path, monkeypatch):
    """If both top-2 are already [Ergebnis] and known, no network calls beyond archive."""
    polls = [
        {"url": "/news/100/sonntagsfrage-foo-ergebnis", "title": "Sonntagsfrage: Foo? [Ergebnis]", "votes": 481, "date": "2026-05-17"},
        {"url": "/news/101/sonntagsfrage-bar-ergebnis", "title": "Sonntagsfrage: Bar? [Ergebnis]", "votes": 400, "date": "2026-05-24"},
    ]
    data_path = _make_db(tmp_path, polls)
    calls = []

    def mock_fetch(url):
        calls.append(url)
        return ARCHIVE_BOTH_FINAL

    import scrape
    monkeypatch.setattr(scrape, "fetch_html", mock_fetch)
    changed = run_incremental(data_path)

    assert changed is False
    assert len(calls) == 1  # only archive page, no detail fetches


def test_incremental_adds_new_poll(tmp_path, monkeypatch):
    """New poll (not in DB yet) gets fetched and added."""
    polls = [
        {"url": "/news/101/sonntagsfrage-bar-ergebnis", "title": "Sonntagsfrage: Bar? [Ergebnis]", "votes": 400, "date": "2026-05-24"},
    ]
    data_path = _make_db(tmp_path, polls)

    def mock_fetch(url):
        if "sonntagsfrage?page" in url:
            return ARCHIVE_ONE_PENDING
        if "/news/102/" in url:
            return POLL_HTML_NEW
        return POLL_HTML_BAR_FINAL

    import scrape
    monkeypatch.setattr(scrape, "fetch_html", mock_fetch)
    changed = run_incremental(data_path)

    assert changed is True
    result = json.loads(Path(data_path).read_text())
    urls = [p["url"] for p in result]
    assert "/news/102/sonntagsfrage-new" in urls
    new = next(p for p in result if p["url"] == "/news/102/sonntagsfrage-new")
    assert new["votes"] == 350
    assert new["date"] == "2026-06-01"


def test_incremental_updates_pending_poll(tmp_path, monkeypatch):
    """Poll in DB without [Ergebnis] gets votes + title refreshed (same URL, title updated)."""
    polls = [
        {"url": "/news/102/sonntagsfrage-new", "title": "Sonntagsfrage: New?", "votes": 200, "date": "2026-06-01"},
        {"url": "/news/101/sonntagsfrage-bar-ergebnis", "title": "Sonntagsfrage: Bar? [Ergebnis]", "votes": 400, "date": "2026-05-24"},
    ]
    data_path = _make_db(tmp_path, polls)

    # Same URL as in DB — only the title text changes when GG adds [Ergebnis]
    ARCHIVE_SAME_URL_NOW_FINAL = """
    <div class="view-content">
      <div class="views-row">
        <h3 class="title"><a href="/news/102/sonntagsfrage-new">Sonntagsfrage: New? [Ergebnis]</a></h3>
      </div>
      <div class="views-row">
        <h3 class="title"><a href="/news/101/sonntagsfrage-bar-ergebnis">Sonntagsfrage: Bar? [Ergebnis]</a></h3>
      </div>
    </div>
    """
    POLL_HTML_NEW_FINAL = """
    <h1 class="title">Sonntagsfrage: New? [Ergebnis]</h1>
    <div class="voll-wer-wann">1. Juni 2026 - 9:00</div>
    <div class="total">Gesamte Stimmenzahl: 350</div>
    """

    def mock_fetch(url):
        if "sonntagsfrage?page" in url:
            return ARCHIVE_SAME_URL_NOW_FINAL
        return POLL_HTML_NEW_FINAL

    import scrape
    monkeypatch.setattr(scrape, "fetch_html", mock_fetch)
    changed = run_incremental(data_path)

    assert changed is True
    result = json.loads(Path(data_path).read_text())
    assert len(result) == 2  # no duplicates added
    updated = next(p for p in result if p["url"] == "/news/102/sonntagsfrage-new")
    assert updated["votes"] == 350
    assert "[Ergebnis]" in updated["title"]
