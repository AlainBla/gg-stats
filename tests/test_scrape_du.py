import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from scrape_du import (
    parse_slide_title,
    normalize_systems,
    guess_systems_from_text,
    game_key,
    parse_gallery,
    build_user_aliases,
    build_title_matcher,
    match_games,
    build,
)


# ---------------------------------------------------------------------------
# Slide titles
# ---------------------------------------------------------------------------

def test_parse_title_colon_format():
    assert parse_slide_title("Mario: Tunic (PlayStation 5)") == ("Mario", "Tunic", "PlayStation 5")


def test_parse_title_colon_keeps_colon_in_game():
    assert parse_slide_title("Alain: Star Wars: Andor (PC)") == ("Alain", "Star Wars: Andor", "PC")


def test_parse_title_gg_user_prefix_without_system():
    assert parse_slide_title("GG-User Major_Panno – This War of Mine") == ("Major_Panno", "This War of Mine", None)


def test_parse_title_en_dash_with_system_and_hyphen_in_game():
    assert parse_slide_title("CaptainKidd – Das Schwarze Auge - Schicksalsklinge HD (PC)") == (
        "CaptainKidd", "Das Schwarze Auge - Schicksalsklinge HD", "PC"
    )


def test_parse_title_hyphen_separator():
    assert parse_slide_title("crux - GT Legends") == ("crux", "GT Legends", None)


def test_parse_title_without_user():
    assert parse_slide_title("Elex (PC)") == (None, "Elex", "PC")


def test_parse_title_non_entry_slides():
    assert parse_slide_title("Und was spielst DU?") is None
    assert parse_slide_title("Grüße von Michael Hengst") is None
    assert parse_slide_title("") is None


# ---------------------------------------------------------------------------
# Systems
# ---------------------------------------------------------------------------

def test_normalize_systems_aliases_and_splits():
    assert normalize_systems("PS4") == ["PlayStation 4"]
    assert normalize_systems("Xbox 360 und PC") == ["Xbox 360", "PC"]
    assert normalize_systems("WiiU Virtual Console / SNES") == ["Wii U", "SNES"]
    assert normalize_systems("Demoversion // PlayStation 4") == ["PlayStation 4"]
    assert normalize_systems("2019, Xbox One") == ["Xbox One"]
    assert normalize_systems("PlayStation 5/PSVR2") == ["PlayStation 5"]


def test_normalize_systems_keeps_game_and_watch_together():
    assert normalize_systems("Game & Watch") == ["Game & Watch"]


def test_normalize_systems_unknown_is_empty():
    assert normalize_systems("Erfinder der DU") == []
    assert normalize_systems(None) == []


def test_guess_systems_from_text_takes_first_mention():
    assert guess_systems_from_text("Maverick bereist die Welt am PC. Später kommt es auf die PS4.") == ["PC"]
    assert guess_systems_from_text("Auf der Switch macht das richtig Spaß") == ["Switch"]
    assert guess_systems_from_text("Ein tolles Spiel ohne Plattformangabe") == []


def test_guess_systems_does_not_match_inside_words():
    assert guess_systems_from_text("Die PCs von damals und das switchen der Waffen") == []


# ---------------------------------------------------------------------------
# Game keys
# ---------------------------------------------------------------------------

def test_game_key_folds_apostrophe_variants():
    assert game_key("Kirby´s Dream Land") == game_key("Kirby's Dream Land") == game_key("Kirby’s Dream Land") == game_key("Kirby‘s Dream Land")


def test_game_key_folds_separators_and_case():
    assert game_key("Prince of Persia - The Lost Crown") == game_key("Prince of Persia: The Lost Crown")
    assert game_key("TUNIC") == game_key("Tunic")
    assert game_key("Civilization 7") != game_key("Civilization 6")


# ---------------------------------------------------------------------------
# Gallery parsing
# ---------------------------------------------------------------------------

GALLERY_HTML = """
<html><head><title>DU 9/2026: Das spielen unsere User - Galerie+ | GamersGlobal.de</title></head><body>
<ul>
<li class="gallery-slide" id="slide-0-field_text_gallery_images-352134">
  <a href="https://www.gamersglobal.de/full/intro.jpg"><img src="/imagecache/intro.jpg" /></a>
  <div class="panel-overlay"><div class="overlay-inner"><h3>DU 9/2026: Das spielen unsere User</h3>
  <div class="desc"><div>Willkommen bei <strong>DU</strong>! Teilgenommen haben die User <strong>Mario</strong> (3x), <strong>Bruno Lawrie</strong> und <strong>crux</strong>.</div></div></div></div>
</li>
<li class="gallery-slide" id="slide-1-field_text_gallery_images-352134">
  <a href="https://www.gamersglobal.de/full/mario.jpg"><img src="/sites/imagecache/mario.jpg" /></a>
  <div class="panel-overlay"><div class="overlay-inner"><h3>Mario: Tunic (PlayStation 5)</h3>
  <div class="desc"><div><em>Die Screenshots von <strong>Tunic</strong> haben <strong>Mario</strong> gefallen.</em></div>
  <div>Parallelen zu <a href="https://www.gamersglobal.de/text-gallery/319682/du-42025?h=slide-1-field_text_gallery_images-319682" onclick="x()"><strong>Blue Prince</strong></a>.</div>
  <script>alert(1)</script></div></div></div>
</li>
<li class="gallery-slide" id="slide-2-field_text_gallery_images-352134">
  <a href="https://www.gamersglobal.de/full/b.jpg"><img src="/sites/imagecache/b.jpg" /></a>
  <div class="panel-overlay"><div class="overlay-inner"><h3>Total War - Warhammer 2 (PC)</h3>
  <div class="desc"><div>Diesmal zieht <strong>Bruno Lawrie</strong> in die Schlacht.</div></div></div></div>
</li>
<li class="gallery-slide" id="slide-3-field_text_gallery_images-352134">
  <a href="https://www.gamersglobal.de/full/c.jpg"><img src="/sites/imagecache/c.jpg" /></a>
  <div class="panel-overlay"><div class="overlay-inner"><h3>GG-User crux – Civilization 7</h3>
  <div class="desc"><div>crux spielt Civilization 7 am PC unter Linux.</div></div></div></div>
</li>
<li class="gallery-slide" id="slide-5-field_text_gallery_images-352134">
  <div class="panel-overlay"><div class="overlay-inner"><h3>Mini Metro, Race the Sun</h3>
  <div class="desc"><div>Wenn crux entspannen will, greift er zu Mini Metro und Race the Sun am PC.</div></div></div></div>
</li>
<li class="gallery-slide" id="slide-6-field_text_gallery_images-352134">
  <div class="panel-overlay"><div class="overlay-inner"><h3>Grüße von Michael Hengst</h3>
  <div class="desc"><div>Liebe DU-Gemeinde, schon zehn Jahre! Danke an Mario, crux und alle anderen.</div></div></div></div>
</li>
<li class="gallery-slide" id="slide-4-field_text_gallery_images-352134">
  <div class="panel-overlay"><div class="overlay-inner"><h3>Und was spielst DU?</h3><div class="desc">Mach mit wie Mario am PC!</div></div></div>
</li>
</ul>
<div id="comments">
<a id="comment-1"></a>
<div id="comment-cid-1" class="comment normal comment-published" uid="6923">
  <div class="comment-infos"><span class="author normal"><a href="/user/6923" title="Hendrik: Status">Hendrik</a></span>
  30 Pro-Gamer - 3. Oktober 2026 - 7:45 <a href="#comment-1" class="comment-anchor-link">#</a></div>
  <div class="comment-content"><p>Tunic ist toll!<br />Und Civilization 7 auch.</p></div>
</div>
</div>
</body></html>
"""


def test_parse_gallery_extracts_month_slides_and_comments():
    g = parse_gallery(GALLERY_HTML, url="/text-gallery/352134/du-92026-das-spielen-unsere-user")

    assert g["month"] == "2026-09"
    assert g["nid"] == 352134
    assert [s["id"] for s in g["slides"]] == [
        "slide-1-field_text_gallery_images-352134",
        "slide-2-field_text_gallery_images-352134",
        "slide-3-field_text_gallery_images-352134",
        "slide-5-field_text_gallery_images-352134",
    ]

    tunic, warhammer, civ, minimetro = g["slides"]
    assert (tunic["user_raw"], tunic["game"], tunic["systems"], tunic["system_source"]) == (
        "Mario", "Tunic", ["PlayStation 5"], "title"
    )
    assert tunic["image"] == "https://www.gamersglobal.de/sites/imagecache/mario.jpg"
    assert "<script" not in tunic["text_html"] and "onclick" not in tunic["text_html"]
    assert 'href="https://www.gamersglobal.de/text-gallery/319682/du-42025?h=slide-1-field_text_gallery_images-319682"' in tunic["text_html"]

    # no user in title → first participant mentioned in the text
    assert (warhammer["user_raw"], warhammer["game"], warhammer["systems"]) == ("Bruno Lawrie", "Total War - Warhammer 2", ["PC"])

    # no system in title → guessed from text
    assert (civ["user_raw"], civ["systems"], civ["system_source"]) == ("crux", ["PC"], "text")

    # neither user nor system in title → participant named at the start of the text
    assert (minimetro["user_raw"], minimetro["game"], minimetro["systems"]) == ("crux", "Mini Metro, Race the Sun", ["PC"])

    assert g["comments"] == [{
        "cid": 1, "uid": 6923, "user_raw": "Hendrik", "date": "2026-10-03 07:45",
        "text": "Tunic ist toll!\nUnd Civilization 7 auch.",
    }]


# ---------------------------------------------------------------------------
# User renames
# ---------------------------------------------------------------------------

def _gallery(month, slides=(), comments=()):
    return {
        "month": month, "nid": int(month.replace("-", "")), "url": f"/text-gallery/{month}",
        "title": f"DU {month}",
        "slides": [
            {"id": f"slide-{i}-{month}", "user_raw": u, "game": g, "systems": s, "system_source": "title",
             "text_html": "", "image": None}
            for i, (u, g, s) in enumerate(slides, 1)
        ],
        "comments": [
            {"cid": i, "uid": uid, "user_raw": u, "date": f"{month}-01 10:00", "text": t}
            for i, (uid, u, t) in enumerate(comments, 1)
        ],
    }


def test_build_user_aliases_from_manual_list():
    assert build_user_aliases({"Sheerluck": ["StefanH"], "Z": ["A", "Z"]}) == {"StefanH": "Sheerluck", "A": "Z"}


# ---------------------------------------------------------------------------
# Comment matching
# ---------------------------------------------------------------------------

def test_match_games_prefers_longest_title_and_word_boundaries():
    matcher = build_title_matcher(["Civilization", "Civilization 7", "Tunic", "Prey"], usernames=set())
    assert match_games("Civilization 7 und TUNIC, aber keine Preyed-Sachen", matcher) == {
        game_key("Civilization 7"), game_key("Tunic"),
    }


def test_match_games_ignores_titles_equal_to_usernames_and_short_titles():
    matcher = build_title_matcher(["Mario", "Gris", "Ys", "Hades"], usernames={"mario"})
    assert match_games("@Mario: Hades und Ys sind super, Gris auch", matcher) == {game_key("Hades"), game_key("Gris")}


# ---------------------------------------------------------------------------
# build(): renames, previous mentions, per-month stats, system trends
# ---------------------------------------------------------------------------

def test_build_applies_renames_previous_mentions_and_stats():
    galleries = [
        _gallery("2025-01",
                 slides=[("StefanH", "Tunic", ["PC"])],
                 comments=[(42, "StefanH", "Tunic!"), (7, "Bob", "Tunic sieht gut aus. Tunic!")]),
        _gallery("2026-09",
                 slides=[("Mario", "TUNIC", ["PlayStation 5"]), ("Sheerluck", "Tunic", ["Switch"])],
                 comments=[(42, "Sheerluck", "Mein Tunic-Text"), (7, "Bob", "Nix")]),
    ]
    out = build(galleries, overrides={"user_aliases": {"Sheerluck": ["StefanH"]}})

    by_month = {g["month"]: g for g in out["galleries"]}
    old_slide = by_month["2025-01"]["slides"][0]
    assert old_slide["user"] == "Sheerluck"

    mario, sheer = by_month["2026-09"]["slides"]
    assert mario["previous"] == [old_slide["id"]]
    assert sheer["previous"] == [old_slide["id"]]
    assert old_slide["previous"] == []

    key = game_key("Tunic")
    jan = {r["key"]: r for r in out["stats"]["games_per_month"]["2025-01"]}
    # Sheerluck (as StefanH) presented + commented → counted once; Bob mentioned twice → once
    assert jan[key]["du"] == 1 and jan[key]["comments"] == 2 and jan[key]["total"] == 2
    sep = {r["key"]: r for r in out["stats"]["games_per_month"]["2026-09"]}
    assert sep[key]["du"] == 2 and sep[key]["comments"] == 1 and sep[key]["total"] == 2

    assert out["stats"]["systems_per_month"]["2026-09"] == {"PlayStation 5": 1, "Switch": 1}
    assert out["stats"]["systems_per_user"]["Sheerluck"] == {"2025-01": {"PC": 1}, "2026-09": {"Switch": 1}}
    assert out["user_aliases"] == {"StefanH": "Sheerluck"}
