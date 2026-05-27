#!/usr/bin/env python3
"""Inject manually-derived user_items for Apr/May/Jun 2025 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Jun 2025 ─────────────────────────────────────────────────────────────────
JUN_USER_ITEMS = [
    {"username": "funrox", "items": [
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "Duru – About Mole Rats and Depression", "category": "game"},
        {"title": "Dept. Q", "category": "film_series"},
    ]},
    {"username": "Flooraimer", "items": [
        {"title": "Ted Lasso", "category": "film_series"},
        {"title": "Stick", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Switch 2", "category": "misc"},
        {"title": "Mario Kart World", "category": "game"},
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "Indiana Jones and the Great Circle", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Elden Ring: Nightreign", "category": "game"},
        {"title": "Kingdom Come: Deliverance 2 – Brushes of Death", "category": "game"},
        {"title": "Doom: The Dark Ages", "category": "game"},
        {"title": "Blue Prince", "category": "game"},
    ]},
    {"username": "Calmon", "items": [
        {"title": "Stellaris", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Bodkins", "category": "film_series"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "Switch 2", "category": "misc"},
        {"title": "Mario Kart World", "category": "game"},
        {"title": "The Last of Us Staffel 2", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "French Open", "category": "misc"},
        {"title": "Switch 2", "category": "misc"},
        {"title": "Death Stranding 2", "category": "game"},
    ]},
    {"username": "MiLe84", "items": [
        {"title": "Mario Kart World", "category": "game"},
    ]},
    {"username": "duchess", "items": [
        {"title": "Tiny Glade", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Mario Kart World", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Switch 2", "category": "misc"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Duster", "category": "film_series"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Switch 2", "category": "misc"},
        {"title": "Mario Kart World", "category": "game"},
        {"title": "Fast Fusion", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "Doom: The Dark Ages", "category": "game"},
    ]},
    {"username": "rammmses", "items": [
        {"title": "Death Stranding 2", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "The Eternaut", "category": "film_series"},
    ]},
]

# ── May 2025 ─────────────────────────────────────────────────────────────────
MAY_USER_ITEMS = [
    {"username": "funrox", "items": [
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "The Last of Us Staffel 2", "category": "film_series"},
        {"title": "Counting Crows Album", "category": "misc"},
    ]},
    {"username": "Flooraimer", "items": [
        {"title": "Final Destination: Bloodlines", "category": "film_series"},
        {"title": "Labyrinth of the Demon King", "category": "game"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "The Last of Us Staffel 2", "category": "film_series"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Old Skies", "category": "game"},
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "Indiana Jones and the Great Circle", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "French Open", "category": "misc"},
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "South of Midnight", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "Doom: The Dark Ages", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "The Last of Us Staffel 2", "category": "film_series"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Thunderbolts", "category": "film_series"},
        {"title": "Andor Staffel 2", "category": "film_series"},
    ]},
    {"username": "Mario", "items": [
        {"title": "Andor Staffel 2", "category": "film_series"},
        {"title": "Wheel of Time Staffel 3", "category": "film_series"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Last Epoch Season 2", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Doom: The Dark Ages", "category": "game"},
    ]},
    {"username": "rammmses", "items": [
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "The Elder Scrolls IV: Oblivion Remastered", "category": "game"},
        {"title": "Kingdom Come: Deliverance 2 DLC", "category": "game"},
    ]},
    {"username": "duchess", "items": [
        {"title": "Final Fantasy IX", "category": "game"},
    ]},
    {"username": "dr_daniel", "items": [
        {"title": "Dredge", "category": "game"},
        {"title": "Ender Magnolia", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Duck Detective: The Ghost of Glamping", "category": "game"},
        {"title": "Blue Prince", "category": "game"},
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Thunderbolts", "category": "film_series"},
        {"title": "Final Destination: Bloodlines", "category": "film_series"},
        {"title": "Mission: Impossible – The Final Reckoning", "category": "film_series"},
        {"title": "Karate Kid Legends", "category": "film_series"},
        {"title": "Blood & Sinners", "category": "film_series"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Death Stranding 2", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Death Stranding 2", "category": "game"},
    ]},
    {"username": "Calmon", "items": [
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
    ]},
]

# ── Apr 2025 ─────────────────────────────────────────────────────────────────
APR_USER_ITEMS = [
    {"username": "Ganon", "items": [
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "Tempest Rising", "category": "game"},
        {"title": "Switch 2 Präsentation", "category": "misc"},
    ]},
    {"username": "duchess", "items": [
        {"title": "The Last of Us Part II", "category": "game"},
    ]},
    {"username": "Thalavox", "items": [
        {"title": "South of Midnight", "category": "game"},
    ]},
    {"username": "Christian Just", "items": [
        {"title": "Der Dunkle Turm", "category": "film_series"},
    ]},
    {"username": "Hendrik", "items": [
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
    ]},
    {"username": "Dennis Hilla", "items": [
        {"title": "One Piece", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "The Last of Us Staffel 2", "category": "film_series"},
    ]},
    {"username": "Gucky", "items": [
        {"title": "Hausparty 2025", "category": "misc"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Andor Staffel 2", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "The Last of Us Staffel 2", "category": "film_series"},
        {"title": "1923", "category": "film_series"},
    ]},
    {"username": "rammmses", "items": [
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "Assassin's Creed Shadows", "category": "game"},
        {"title": "Atomfall", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Xenoblade Chronicles X: Definitive Edition", "category": "game"},
    ]},
    {"username": "Wuslon", "items": [
        {"title": "Indiana Jones and the Great Circle", "category": "game"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "Tempest Rising", "category": "game"},
        {"title": "Days Gone Remastered", "category": "game"},
        {"title": "Indiana Jones and the Great Circle", "category": "game"},
    ]},
]

MONTH_DATA = {
    "2025-06": JUN_USER_ITEMS,
    "2025-05": MAY_USER_ITEMS,
    "2025-04": APR_USER_ITEMS,
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
