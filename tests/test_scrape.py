import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import json, pytest
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
