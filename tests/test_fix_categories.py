import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from fix_categories import apply_aliases, dedupe_items


def test_dedupe_items_collapses_alias_duplicates_keeping_first():
    """An edited comment re-extracted with an already-corrected typo must not double-count."""
    entry = {
        "editors": [],
        "user_items": [{"username": "alice", "items": [
            {"title": "The Blood of Dawnwalker", "category": "game"},
            {"title": "Fauda", "category": "film_series"},
            {"title": "Blood of Dawnwalke", "category": "misc"},
            {"title": "fauda", "category": "film_series"},
        ]}],
    }
    apply_aliases(entry, {"Blood of Dawnwalke": "The Blood of Dawnwalker"})

    assert dedupe_items(entry) is True
    assert entry["user_items"][0]["items"] == [
        {"title": "The Blood of Dawnwalker", "category": "game"},
        {"title": "Fauda", "category": "film_series"},
    ]


def test_dedupe_items_is_per_person_and_noop_without_duplicates():
    entry = {
        "editors": [{"name": "Jörg", "items": [{"title": "Fauda", "category": "film_series"}]}],
        "user_items": [{"username": "alice", "items": [{"title": "Fauda", "category": "film_series"}]}],
    }
    assert dedupe_items(entry) is False
    assert len(entry["editors"][0]["items"]) == 1
    assert len(entry["user_items"][0]["items"]) == 1
