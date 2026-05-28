#!/usr/bin/env python3
"""Inject manually-derived user_items for Feb/Mar/Apr 2024 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Apr 2024 ─────────────────────────────────────────────────────────────────
APR_USER_ITEMS = [
    {"username": "Pomme", "items": [
        {"title": "Star Trek: Discovery", "category": "film_series"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "Fallout", "category": "film_series"},
        {"title": "Stellar Blade", "category": "game"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "WrestleMania", "category": "misc"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Harold Halibut", "category": "game"},
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
        {"title": "Fallout", "category": "film_series"},
        {"title": "Like a Dragon: Infinite Wealth", "category": "game"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Shogun", "category": "film_series"},
        {"title": "3 Body Problem", "category": "film_series"},
        {"title": "Kung Fu Panda 4", "category": "film_series"},
    ]},
    {"username": "rammmses", "items": [
        {"title": "Rise of the Ronin", "category": "game"},
        {"title": "Shogun", "category": "film_series"},
        {"title": "Fallout", "category": "film_series"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Fallout", "category": "film_series"},
        {"title": "Harold Halibut", "category": "game"},
    ]},
    {"username": "Dreadxx", "items": [
        {"title": "TopSpin 2K25", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "American Arcadia", "category": "game"},
        {"title": "Manor Lords", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Depeche Mode Konzert", "category": "misc"},
        {"title": "Final Fantasy XVI", "category": "game"},
    ]},
]

# ── Mar 2024 ─────────────────────────────────────────────────────────────────
MAR_USER_ITEMS = [
    {"username": "Lencer", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Anno 1800", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "The Zone of Interest", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Peaky Blinders", "category": "film_series"},
        {"title": "Prince of Persia: The Lost Crown", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Jordskott", "category": "film_series"},
        {"title": "Final Fantasy XV", "category": "game"},
        {"title": "Final Fantasy VII Remake Intergrade", "category": "game"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Dragon's Dogma 2", "category": "game"},
        {"title": "Outcast: A New Beginning", "category": "game"},
    ]},
    {"username": "StefanH", "items": [
        {"title": "Crusader Kings 3", "category": "game"},
        {"title": "Unicorn Overlord", "category": "game"},
    ]},
    {"username": "Thomas Schmitz", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Poor Things", "category": "film_series"},
        {"title": "Fargo", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Shogun", "category": "film_series"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Godzilla x Kong: The New Empire", "category": "film_series"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
    ]},
    {"username": "Henmann", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Ghostbusters: Frozen Empire", "category": "film_series"},
    ]},
    {"username": "Jonas S.", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Cyberpunk 2077", "category": "game"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Persona 3 Reload", "category": "game"},
        {"title": "Final Fantasy VII Rebirth", "category": "game"},
    ]},
]

# ── Feb 2024 ─────────────────────────────────────────────────────────────────
FEB_USER_ITEMS = [
    {"username": "unregistriert", "items": [
        {"title": "Winnie-the-Pooh: Blood and Honey 2", "category": "film_series"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Banishers: Ghosts of New Eden", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "The Holdovers", "category": "film_series"},
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Banishers: Ghosts of New Eden", "category": "game"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Halo", "category": "film_series"},
        {"title": "Dune: Part Two", "category": "film_series"},
    ]},
    {"username": "Calmon", "items": [
        {"title": "Curb Your Enthusiasm", "category": "film_series"},
        {"title": "Star Trek: Strange New Worlds", "category": "film_series"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Poor Things", "category": "film_series"},
        {"title": "Fargo", "category": "film_series"},
        {"title": "True Detective", "category": "film_series"},
        {"title": "Final Fantasy VII Rebirth", "category": "game"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Elite Dangerous", "category": "game"},
    ]},
    {"username": "The Real Maulwurfn", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Shogun", "category": "film_series"},
        {"title": "Halo", "category": "film_series"},
        {"title": "Le Mans Ultimate", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "True Detective", "category": "film_series"},
        {"title": "Final Fantasy XVI", "category": "game"},
    ]},
    {"username": "MiLe84", "items": [
        {"title": "Alan Wake 2", "category": "game"},
        {"title": "What We Do in the Shadows", "category": "film_series"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Shogun", "category": "film_series"},
        {"title": "Baldur's Gate 3", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "The Brothers Sun", "category": "film_series"},
        {"title": "For All Mankind", "category": "film_series"},
        {"title": "Persona 5 Royal", "category": "game"},
        {"title": "Like a Dragon", "category": "game"},
        {"title": "Star Trek: Resurgence", "category": "game"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Tekken 8", "category": "game"},
    ]},
    {"username": "Alter Hase", "items": [
        {"title": "The Thaumaturge", "category": "game"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Hogwarts Legacy", "category": "game"},
        {"title": "Baldur's Gate 3", "category": "game"},
    ]},
]

MONTH_DATA = {
    "2024-04": APR_USER_ITEMS,
    "2024-03": MAR_USER_ITEMS,
    "2024-02": FEB_USER_ITEMS,
}


def compute_stats(editors, user_items):
    stats = {}
    for editor in editors:
        key = "editor:" + re.sub(r"\s+", "_", editor["name"].lower())
        for item in editor["items"]:
            t = item["title"]
            if t not in stats:
                stats[t] = {"count": 0, "category": item["category"], "mentioners": []}
            if key not in stats[t]["mentioners"]:
                stats[t]["mentioners"].append(key)
                stats[t]["count"] += 1
    for user in user_items:
        key = "user:" + user["username"]
        for item in user["items"]:
            t = item["title"]
            if t not in stats:
                stats[t] = {"count": 0, "category": item["category"], "mentioners": []}
            if key not in stats[t]["mentioners"]:
                stats[t]["mentioners"].append(key)
                stats[t]["count"] += 1
    return stats


def main():
    data = json.loads(DATA_FILE.read_text())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for entry in data:
        month = entry["month"]
        if month not in MONTH_DATA:
            continue
        entry["user_items"] = MONTH_DATA[month]
        entry["item_stats"] = compute_stats(entry["editors"], entry["user_items"])
        entry["last_updated"] = now
        print(f"  {month}: {len(entry['user_items'])} users, {len(entry['item_stats'])} unique items")

    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print("Written data/vorfreude.json")


if __name__ == "__main__":
    main()
