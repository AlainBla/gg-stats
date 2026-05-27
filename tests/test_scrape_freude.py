"""Tests for scrape_freude.py — inline HTML fixtures, no network calls."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import json
import pytest
from scrape_freude import parse_article, parse_comments, compute_stats


# ---------------------------------------------------------------------------
# Article HTML fixtures
# ---------------------------------------------------------------------------

ARTICLE_HTML_SIMPLE = """
<div class="node node-news" id="node-100001">
  <h1 class="title">Darauf freut sich die Redaktion im... Mai 2026</h1>
  <div class="news-body">
    <table class="artikel-autor"><tr><td><img src="/joerg.png"/></td></tr></table>
    <u><strong>Jörg Langer</strong></u><br/>
    [FILME/SERIEN] Ich freue mich auf <strong>The Boroughs</strong> und <strong>Cocoon</strong>.<br/>
    <br/>
    [SPIELE/BRETTSPIELE] Ich freue mich auf <strong>007 Dying Light</strong>.<br/>
    <br/>
    [SONSTIGES] Ich freue mich auf <em>Sommerurlaub</em>.

    <table class="artikel-autor"><tr><td><img src="/hagen.png"/></td></tr></table>
    <u><strong>Hagen Gehritz</strong></u><br/>
    [FILME/SERIEN] Freue mich auf <strong>Witch Hat Atelier</strong>.<br/>
    <br/>
    [SPIELE/BRETTSPIELE] Ich schaue auf <strong>Motor Slice</strong> und <strong>Inkonbini</strong>.<br/>
  </div>
</div>
"""

ARTICLE_HTML_MIXED_MARKUP = """
<div class="node node-news" id="node-100002">
  <h1 class="title">Darauf freut sich die Redaktion im... April 2026</h1>
  <div class="news-body">
    <a href="/user/2448"><img src="/benjamin.png"/></a>
    <u>Benjamin Braun</u><br/>
    [FILME/SERIEN] Nochmal Kino, aber <strong>Nürnberg</strong> brauche ich nicht.<br/>
    [SPIELE/BRETTSPIELE] <strong>Directive 8020</strong> und <strong>007 - First Light</strong>.<br/>

    <table class="artikel-autor"><tr><td><img src="/kai.png"/></td></tr></table>
    <u><strong>Kai Schmidt</strong></u><br/>
    [SPIELE/BRETTSPIELE] Ich freue mich auf <strong>Mortal Kombat 2</strong>.<br/>
    [SONSTIGES] <em>Dokomi</em> ist das Highlight.<br/>
  </div>
</div>
"""

ARTICLE_HTML_NO_EDITORS = """
<div class="node node-news" id="node-100003">
  <h1 class="title">Some other article</h1>
  <div class="news-body">
    <p>Just some text without editor sections.</p>
  </div>
</div>
"""

ARTICLE_HTML_CATEGORY_VARIANTS = """
<div class="node node-news" id="node-100004">
  <h1 class="title">Darauf freut sich die Redaktion im... März 2026</h1>
  <div class="news-body">
    <u><strong>Michael Hengst</strong></u><br/>
    [FILME/SERIEN] Freue mich auf <strong>Film A</strong> und <strong>Film B</strong>.<br/>
    [SPIELE/BRETTSPIELE] <strong>Game X</strong> sieht super aus.<br/>
    [SONSTIGES] <strong>Urlaub</strong> natürlich.<br/>
  </div>
</div>
"""


# ---------------------------------------------------------------------------
# parse_article tests
# ---------------------------------------------------------------------------

def test_parse_article_title():
    result = parse_article(ARTICLE_HTML_SIMPLE)
    assert result["title"] == "Darauf freut sich die Redaktion im... Mai 2026"


def test_parse_article_month():
    result = parse_article(ARTICLE_HTML_SIMPLE)
    assert result["month"] == "2026-05"


def test_parse_article_month_april():
    result = parse_article(ARTICLE_HTML_MIXED_MARKUP)
    assert result["month"] == "2026-04"


def test_parse_article_editor_count():
    result = parse_article(ARTICLE_HTML_SIMPLE)
    assert len(result["editors"]) == 2


def test_parse_article_editor_names():
    result = parse_article(ARTICLE_HTML_SIMPLE)
    names = [e["name"] for e in result["editors"]]
    assert "Jörg Langer" in names
    assert "Hagen Gehritz" in names


def test_parse_article_editor_without_strong_in_u():
    """Benjamin Braun uses <u>Name</u> without inner <strong>."""
    result = parse_article(ARTICLE_HTML_MIXED_MARKUP)
    names = [e["name"] for e in result["editors"]]
    assert "Benjamin Braun" in names


def test_parse_article_items_film_category():
    result = parse_article(ARTICLE_HTML_SIMPLE)
    joerg = next(e for e in result["editors"] if e["name"] == "Jörg Langer")
    film_items = [i for i in joerg["items"] if i["category"] == "film_series"]
    titles = [i["title"] for i in film_items]
    assert "The Boroughs" in titles
    assert "Cocoon" in titles


def test_parse_article_items_game_category():
    result = parse_article(ARTICLE_HTML_SIMPLE)
    joerg = next(e for e in result["editors"] if e["name"] == "Jörg Langer")
    game_items = [i for i in joerg["items"] if i["category"] == "game"]
    titles = [i["title"] for i in game_items]
    assert "007 Dying Light" in titles


def test_parse_article_items_misc_category():
    result = parse_article(ARTICLE_HTML_SIMPLE)
    joerg = next(e for e in result["editors"] if e["name"] == "Jörg Langer")
    misc_items = [i for i in joerg["items"] if i["category"] == "misc"]
    titles = [i["title"] for i in misc_items]
    assert "Sommerurlaub" in titles


def test_parse_article_em_items():
    """<em> tags should be collected as items."""
    result = parse_article(ARTICLE_HTML_MIXED_MARKUP)
    kai = next(e for e in result["editors"] if e["name"] == "Kai Schmidt")
    misc_items = [i for i in kai["items"] if i["category"] == "misc"]
    titles = [i["title"] for i in misc_items]
    assert "Dokomi" in titles


def test_parse_article_category_labels_not_in_items():
    """Category labels like [SPIELE/BRETTSPIELE] must not appear as items."""
    result = parse_article(ARTICLE_HTML_SIMPLE)
    all_titles = [
        i["title"]
        for e in result["editors"]
        for i in e["items"]
    ]
    for title in all_titles:
        assert "[" not in title, f"Category label leaked into items: {title!r}"
        assert "SPIELE" not in title
        assert "FILME" not in title
        assert "SONSTIGES" not in title


def test_parse_article_items_not_empty():
    """Items should have non-empty titles."""
    result = parse_article(ARTICLE_HTML_SIMPLE)
    for editor in result["editors"]:
        for item in editor["items"]:
            assert len(item["title"].strip()) > 2


def test_parse_article_no_editors_returns_empty():
    result = parse_article(ARTICLE_HTML_NO_EDITORS)
    assert result["editors"] == []


def test_parse_article_all_categories():
    result = parse_article(ARTICLE_HTML_CATEGORY_VARIANTS)
    michael = next(e for e in result["editors"] if e["name"] == "Michael Hengst")
    cats = {i["category"] for i in michael["items"]}
    assert "film_series" in cats
    assert "game" in cats
    assert "misc" in cats


def test_parse_article_second_editor_items():
    result = parse_article(ARTICLE_HTML_SIMPLE)
    hagen = next(e for e in result["editors"] if e["name"] == "Hagen Gehritz")
    film_items = [i for i in hagen["items"] if i["category"] == "film_series"]
    game_items = [i for i in hagen["items"] if i["category"] == "game"]
    assert any(i["title"] == "Witch Hat Atelier" for i in film_items)
    assert any(i["title"] == "Motor Slice" for i in game_items)
    assert any(i["title"] == "Inkonbini" for i in game_items)


# ---------------------------------------------------------------------------
# Comment HTML fixtures
# ---------------------------------------------------------------------------

COMMENTS_HTML = """
<div class="node node-news">
  <div class="comments">
    <div class="comment normal comment-published" id="comment-cid-3129314" uid="39476">
      <div class="comment-infos">
        <span class="author normal">
          <a href="/user/39476" title="Klexter: ">Klexter</a>
        </span>
        12 Trollwächter - 4. Mai 2026 - 16:14
      </div>
      <div class="comment-content">
        <p>Sehr interessant, vielen Dank!</p>
        <p>Keiner freut sich auf Zero Parades.</p>
      </div>
    </div>

    <div class="comment normal comment-published" id="comment-cid-3129316" uid="1104">
      <div class="comment-infos">
        <span class="author normal">
          <a href="/user/1104" title="Olphas: fine">Olphas</a>
        </span>
        26 Spiele-Kenner - 4. Mai 2026 - 16:30
      </div>
      <div class="comment-content">
        <p>Bin auch gespannt auf 007.</p>
      </div>
    </div>

    <div class="comment normal comment-published" id="comment-cid-3129400" uid="39476">
      <div class="comment-infos">
        <span class="author normal">
          <a href="/user/39476" title="Klexter: ">Klexter</a>
        </span>
        4. Mai 2026 - 18:00
      </div>
      <div class="comment-content">
        <p>Noch ein Kommentar von mir.</p>
      </div>
    </div>
  </div>
</div>
"""

COMMENTS_HTML_NO_COMMENTS = """
<div class="node node-news">
  <div class="comments">
    <p>Keine Kommentare vorhanden.</p>
  </div>
</div>
"""


# ---------------------------------------------------------------------------
# parse_comments tests
# ---------------------------------------------------------------------------

def test_parse_comments_returns_list():
    result = parse_comments(COMMENTS_HTML)
    assert isinstance(result, list)


def test_parse_comments_unique_usernames():
    """Each username appears exactly once."""
    result = parse_comments(COMMENTS_HTML)
    usernames = [c["username"] for c in result]
    assert len(usernames) == len(set(usernames))


def test_parse_comments_correct_usernames():
    result = parse_comments(COMMENTS_HTML)
    usernames = {c["username"] for c in result}
    assert "Klexter" in usernames
    assert "Olphas" in usernames


def test_parse_comments_concatenates_multi_comment_user():
    """Klexter has 2 comments — they should be merged into one entry."""
    result = parse_comments(COMMENTS_HTML)
    klexter = next(c for c in result if c["username"] == "Klexter")
    assert "Sehr interessant" in klexter["text"]
    assert "Noch ein Kommentar" in klexter["text"]


def test_parse_comments_separator_between_concatenated():
    """Concatenated comments should be separated by double newline."""
    result = parse_comments(COMMENTS_HTML)
    klexter = next(c for c in result if c["username"] == "Klexter")
    assert "\n\n" in klexter["text"]


def test_parse_comments_single_user_text():
    result = parse_comments(COMMENTS_HTML)
    olphas = next(c for c in result if c["username"] == "Olphas")
    assert "gespannt auf 007" in olphas["text"]


def test_parse_comments_empty_returns_empty_list():
    result = parse_comments(COMMENTS_HTML_NO_COMMENTS)
    assert result == []


def test_parse_comments_count():
    result = parse_comments(COMMENTS_HTML)
    assert len(result) == 2  # Klexter + Olphas (deduplicated)


# ---------------------------------------------------------------------------
# compute_stats tests
# ---------------------------------------------------------------------------

EDITORS_DATA = [
    {
        "name": "Jörg Langer",
        "items": [
            {"title": "007 Dying Light", "category": "game"},
            {"title": "The Boroughs", "category": "film_series"},
        ]
    },
    {
        "name": "Hagen Gehritz",
        "items": [
            {"title": "007 Dying Light", "category": "game"},
            {"title": "Witch Hat Atelier", "category": "film_series"},
        ]
    }
]

USER_ITEMS_DATA = [
    {
        "username": "user123",
        "items": [
            {"title": "007 Dying Light", "category": "game"},
            {"title": "Elden Ring", "category": "game"},
        ]
    }
]


def test_compute_stats_returns_dict():
    result = compute_stats(EDITORS_DATA, [])
    assert isinstance(result, dict)


def test_compute_stats_item_count():
    result = compute_stats(EDITORS_DATA, [])
    # 007 Dying Light mentioned by 2 editors → count=2
    assert result["007 Dying Light"]["count"] == 2


def test_compute_stats_unique_item():
    result = compute_stats(EDITORS_DATA, [])
    # The Boroughs mentioned by 1 editor
    assert result["The Boroughs"]["count"] == 1


def test_compute_stats_mentioners_list():
    result = compute_stats(EDITORS_DATA, [])
    mentioners = set(result["007 Dying Light"]["mentioners"])
    assert "editor:jörg_langer" in mentioners
    assert "editor:hagen_gehritz" in mentioners


def test_compute_stats_category_preserved():
    result = compute_stats(EDITORS_DATA, [])
    assert result["007 Dying Light"]["category"] == "game"
    assert result["The Boroughs"]["category"] == "film_series"


def test_compute_stats_with_user_items():
    result = compute_stats(EDITORS_DATA, USER_ITEMS_DATA)
    # 007 Dying Light: 2 editors + 1 user = count 3
    assert result["007 Dying Light"]["count"] == 3
    mentioners = set(result["007 Dying Light"]["mentioners"])
    assert "user:user123" in mentioners


def test_compute_stats_user_only_item():
    result = compute_stats(EDITORS_DATA, USER_ITEMS_DATA)
    # Elden Ring only mentioned by user
    assert result["Elden Ring"]["count"] == 1
    assert "user:user123" in result["Elden Ring"]["mentioners"]


def test_compute_stats_no_duplicate_mentioners():
    """Same editor mentioning same item twice shouldn't inflate count."""
    editors_dup = [
        {
            "name": "Jörg Langer",
            "items": [
                {"title": "Game A", "category": "game"},
                {"title": "Game A", "category": "game"},  # duplicate
            ]
        }
    ]
    result = compute_stats(editors_dup, [])
    # The item appears twice for same editor but count should be 1 unique mentioner
    assert result["Game A"]["count"] == 1


def test_compute_stats_empty_editors():
    result = compute_stats([], [])
    assert result == {}


def test_compute_stats_editor_key_format():
    """Editor key = 'editor:{name_lowercase_spaces_to_underscore}'."""
    result = compute_stats(EDITORS_DATA, [])
    joerg_items = [k for k, v in result.items() if "editor:jörg_langer" in v["mentioners"]]
    assert len(joerg_items) > 0


# ---------------------------------------------------------------------------
# discover_articles tests (basic URL construction)
# ---------------------------------------------------------------------------

from scrape_freude import _month_to_slug, _slug_to_month, _scrape_article


# ---------------------------------------------------------------------------
# _scrape_article enrichment-skip tests (F1 fix)
# ---------------------------------------------------------------------------

class _FakeHTML:
    """Minimal HTML for a single-editor article with zero comments."""
    ARTICLE = """
    <div class="node node-news">
      <h1 class="title">Darauf freut sich die Redaktion im... Juni 2026</h1>
      <div class="news-body">
        <u><strong>Jörg Langer</strong></u><br/>
        [SPIELE/BRETTSPIELE] <strong>My Game</strong>.<br/>
      </div>
    </div>
    """


def _make_existing_entry(comment_count: int, user_items: list) -> dict:
    return {
        "month": "2026-06",
        "url": "/news/99999/darauf-freut-sich-die-redaktion-im-juni-2026",
        "title": "Darauf freut sich die Redaktion im... Juni 2026",
        "comment_count": comment_count,
        "editors": [{"name": "Jörg Langer", "items": [{"title": "My Game", "category": "game"}]}],
        "comments_raw": [],
        "user_items": user_items,
        "item_stats": {},
    }


def test_scrape_article_skips_reenrichment_when_count_unchanged_and_user_items_exist(monkeypatch):
    """F1: When comment_count unchanged AND user_items populated, enrich must NOT be called."""
    existing_user_items = [{"username": "alice", "items": [{"title": "My Game", "category": "game"}]}]
    existing_entry = _make_existing_entry(comment_count=3, user_items=existing_user_items)

    enrich_called = []

    def _fake_fetch_html(url):
        return _FakeHTML.ARTICLE

    def _fake_count_comments(html):
        return 3  # unchanged

    def _fake_parse_comments(html):
        return [{"username": "alice", "text": "I love My Game!"}]

    def _fake_enrich_comments(comments, editors, api_key):
        enrich_called.append(True)
        return [{"username": "alice", "items": [{"title": "New Item", "category": "game"}]}]

    import scrape_freude
    monkeypatch.setattr(scrape_freude, "fetch_html", _fake_fetch_html)
    monkeypatch.setattr(scrape_freude, "_count_comments_in_html", _fake_count_comments)
    monkeypatch.setattr(scrape_freude, "parse_comments", _fake_parse_comments)
    monkeypatch.setattr(scrape_freude, "enrich_comments", _fake_enrich_comments)

    result = _scrape_article(
        url="/news/99999/x",
        existing_entry=existing_entry,
        enrich=True,
        api_key="fake-key",
    )

    # enrich_comments must NOT have been called
    assert enrich_called == [], "enrich_comments was called despite unchanged comment_count and populated user_items"
    # The preserved user_items should be returned unchanged
    assert result["user_items"] == existing_user_items


def test_scrape_article_does_reenrich_when_count_unchanged_but_user_items_empty(monkeypatch):
    """F1: When comment_count unchanged but user_items is empty, enrich SHOULD run."""
    existing_entry = _make_existing_entry(comment_count=3, user_items=[])  # no prior user_items

    enrich_called = []

    def _fake_fetch_html(url):
        return _FakeHTML.ARTICLE

    def _fake_count_comments(html):
        return 3  # unchanged

    def _fake_parse_comments(html):
        return [{"username": "alice", "text": "I love My Game!"}]

    def _fake_enrich_comments(comments, editors, api_key):
        enrich_called.append(True)
        return [{"username": "alice", "items": [{"title": "My Game", "category": "game"}]}]

    import scrape_freude
    monkeypatch.setattr(scrape_freude, "fetch_html", _fake_fetch_html)
    monkeypatch.setattr(scrape_freude, "_count_comments_in_html", _fake_count_comments)
    monkeypatch.setattr(scrape_freude, "parse_comments", _fake_parse_comments)
    monkeypatch.setattr(scrape_freude, "enrich_comments", _fake_enrich_comments)

    _scrape_article(
        url="/news/99999/x",
        existing_entry=existing_entry,
        enrich=True,
        api_key="fake-key",
    )

    assert enrich_called == [True], "enrich_comments should have been called when user_items was empty"


def test_scrape_article_does_reenrich_when_count_changed(monkeypatch):
    """F1: When comment_count increases, enrich SHOULD run even if user_items exist."""
    existing_user_items = [{"username": "alice", "items": [{"title": "My Game", "category": "game"}]}]
    existing_entry = _make_existing_entry(comment_count=3, user_items=existing_user_items)

    enrich_called = []

    def _fake_fetch_html(url):
        return _FakeHTML.ARTICLE

    def _fake_count_comments(html):
        return 5  # changed from 3 → 5

    def _fake_parse_comments(html):
        return [{"username": "alice", "text": "I love My Game!"}, {"username": "bob", "text": "Me too!"}]

    def _fake_enrich_comments(comments, editors, api_key):
        enrich_called.append(True)
        return [{"username": "alice", "items": [{"title": "My Game", "category": "game"}]}]

    import scrape_freude
    monkeypatch.setattr(scrape_freude, "fetch_html", _fake_fetch_html)
    monkeypatch.setattr(scrape_freude, "_count_comments_in_html", _fake_count_comments)
    monkeypatch.setattr(scrape_freude, "parse_comments", _fake_parse_comments)
    monkeypatch.setattr(scrape_freude, "enrich_comments", _fake_enrich_comments)

    _scrape_article(
        url="/news/99999/x",
        existing_entry=existing_entry,
        enrich=True,
        api_key="fake-key",
    )

    assert enrich_called == [True], "enrich_comments should run when comment_count changed"


# ---------------------------------------------------------------------------
# discover_articles tests (basic URL construction)
# ---------------------------------------------------------------------------

def test_month_to_slug_mai():
    assert _month_to_slug("2026-05") == "mai-2026"


def test_month_to_slug_januar():
    assert _month_to_slug("2026-01") == "januar-2026"


def test_month_to_slug_dezember():
    assert _month_to_slug("2025-12") == "dezember-2025"


def test_slug_to_month_mai():
    assert _slug_to_month("mai", "2026") == "2026-05"


def test_slug_to_month_maerz():
    assert _slug_to_month("maerz", "2026") == "2026-03"


def test_slug_to_month_dezember():
    assert _slug_to_month("dezember", "2025") == "2025-12"
