#!/usr/bin/env python3
"""Patch missed user items found via quoted-title scan of comments_raw."""
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "vorfreude.json"

PATCHES = {
    "2020-02": [
        ("AlexCartman", [
            {"title": "Die drei Sonnen", "category": "misc"},
        ]),
    ],
    "2020-08": [
        ("AlexCartman", [
            {"title": "The Legend of Zelda: A Link to the Past", "category": "game"},
            {"title": "Devil Survivor: Overclocked", "category": "game"},
        ]),
    ],
    "2021-03": [
        ("Bruno Lawrie", [
            {"title": "To the Moon", "category": "game"},
        ]),
    ],
    "2021-05": [
        ("Q-Bert", [
            {"title": "Solasta: Crown of the Magister", "category": "game"},
            {"title": "Shadow and Bones", "category": "film_series"},
            {"title": "The Nevers", "category": "film_series"},
        ]),
    ],
    "2022-09": [
        ("Hannes Herrmann", [
            {"title": "Der Herr der Ringe: Die Ringe der Macht", "category": "film_series"},
        ]),
        ("Philipp Spilker", [
            {"title": "Der Herr der Ringe: Die Ringe der Macht", "category": "film_series"},
            {"title": "Steelrising", "category": "game"},
        ]),
        ("unregistriert", [
            {"title": "Der Herr der Ringe: Die Ringe der Macht", "category": "film_series"},
            {"title": "Star Trek: Lower Decks", "category": "film_series"},
        ]),
    ],
    "2023-02": [
        ("Thomas Schmitz", [
            {"title": "Pentiment", "category": "game"},
            {"title": "Cunk on Earth", "category": "film_series"},
        ]),
        ("Ramona Kiuntke", [
            {"title": "Cunk on Earth", "category": "film_series"},
        ]),
    ],
}


def compute_stats(editors, user_items):
    stats = {}

    def add_item(title, category, mentioner):
        if title not in stats:
            stats[title] = {"count": 0, "category": category, "mentioners": []}
        if mentioner not in stats[title]["mentioners"]:
            stats[title]["mentioners"].append(mentioner)
            stats[title]["count"] += 1
        if category and category != "unknown":
            stats[title]["category"] = category

    for ed in editors:
        for item in ed.get("items", []):
            add_item(item["title"], item.get("category", "unknown"), f"editor:{ed['name']}")

    for u in user_items:
        for item in u.get("items", []):
            add_item(item["title"], item.get("category", "unknown"), f"user:{u['username']}")

    return stats


def main():
    data = json.loads(DATA_FILE.read_text())
    by_month = {e["month"]: e for e in data}

    for month, patches in PATCHES.items():
        entry = by_month.get(month)
        if not entry:
            print(f"WARN: month {month} not found")
            continue

        user_items = entry.setdefault("user_items", [])
        by_user = {u["username"]: u for u in user_items}

        for username, new_items in patches:
            if username not in by_user:
                by_user[username] = {"username": username, "items": []}
                user_items.append(by_user[username])

            existing_titles = {i["title"] for i in by_user[username]["items"]}
            added = []
            for item in new_items:
                if item["title"] not in existing_titles:
                    by_user[username]["items"].append(item)
                    existing_titles.add(item["title"])
                    added.append(item["title"])
            if added:
                print(f"  {month} {username}: +{added}")

        entry["item_stats"] = compute_stats(entry.get("editors", []), user_items)

    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print("Done.")


if __name__ == "__main__":
    main()
