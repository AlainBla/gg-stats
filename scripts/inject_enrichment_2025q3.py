#!/usr/bin/env python3
"""Inject manually-derived user_items for Jul/Aug/Sep 2025 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Sep 2025 ─────────────────────────────────────────────────────────────────
SEP_USER_ITEMS = [
    {"username": "Vendetti", "items": [
        {"title": "Denshattack!", "category": "game"},
    ]},
    {"username": "Hyperbolic", "items": [
        {"title": "Demon Slayer: Infinity Castle", "category": "film_series"},
        {"title": "Trails in the Sky: First Chapter", "category": "game"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "World of Warcraft Midnight", "category": "game"},
        {"title": "Assassin's Creed Shadows", "category": "game"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Trails in the Sky: First Chapter", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Wednesday Staffel 2", "category": "film_series"},
        {"title": "Death Stranding 2", "category": "game"},
        {"title": "RoboCop: Rogue City", "category": "game"},
        {"title": "US Open", "category": "misc"},
    ]},
    {"username": "euph", "items": [
        {"title": "Donkey Kong Bananza", "category": "game"},
    ]},
    {"username": "BruderSamedi", "items": [
        {"title": "Star Trek: Strange New Worlds", "category": "film_series"},
        {"title": "Feuer & Flamme Staffel 10", "category": "film_series"},
        {"title": "Hogwarts Legacy", "category": "game"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Indiana Jones DLC", "category": "game"},
        {"title": "Foundation Staffel 3", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Wednesday Staffel 2", "category": "film_series"},
        {"title": "Tulsa King", "category": "film_series"},
        {"title": "Children of Silenttown", "category": "game"},
        {"title": "Lost Records: Bloom & Rage", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Swords of the Sea", "category": "game"},
        {"title": "Baby Steps", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Anno 117 Demo", "category": "game"},
        {"title": "Borderlands 4", "category": "game"},
        {"title": "Age of Mythology Retold DLC 2", "category": "game"},
        {"title": "Kreuzweg des Raben", "category": "misc"},
    ]},
    {"username": "Moriarty1779", "items": [
        {"title": "No Man's Sky Update", "category": "game"},
        {"title": "Planet Coaster 2", "category": "game"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "Task", "category": "film_series"},
        {"title": "Weapons", "category": "film_series"},
    ]},
]

# ── Aug 2025 ─────────────────────────────────────────────────────────────────
AUG_USER_ITEMS = [
    {"username": "Maestro84", "items": [
        {"title": "Assassin's Creed Shadows", "category": "game"},
        {"title": "World of Warcraft", "category": "game"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Metal Gear Solid Delta: Snake Eater", "category": "game"},
        {"title": "Whisper Mountain Outbreak", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Titan Quest 2", "category": "game"},
    ]},
    {"username": "TSH-Lightning", "items": [
        {"title": "Titan Quest 2", "category": "game"},
        {"title": "Wednesday Staffel 2", "category": "film_series"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Mafia: The Old Country", "category": "game"},
        {"title": "Metal Gear Solid Delta: Snake Eater", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Eriksholm: The Stolen Child", "category": "game"},
        {"title": "The Alters", "category": "game"},
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "Donkey Kong Bananza", "category": "game"},
        {"title": "Drova: Forsaken Kin", "category": "game"},
        {"title": "Black Mirror", "category": "film_series"},
        {"title": "Death Note", "category": "film_series"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "Star Trek: Strange New Worlds", "category": "film_series"},
        {"title": "Alien: Earth", "category": "film_series"},
        {"title": "Mocro Maffia", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Mafia: The Old Country", "category": "game"},
        {"title": "Kirby und das vergessene Land", "category": "game"},
        {"title": "Gamescom", "category": "misc"},
    ]},
    {"username": "Flooraimer", "items": [
        {"title": "Mafia: The Old Country", "category": "game"},
        {"title": "Gears of War: Reloaded", "category": "game"},
    ]},
    {"username": "Batwayne", "items": [
        {"title": "Thief 2", "category": "game"},
        {"title": "Gankutsuō", "category": "film_series"},
        {"title": "Es (Stephen King)", "category": "misc"},
    ]},
    {"username": "euph", "items": [
        {"title": "Donkey Kong Bananza", "category": "game"},
        {"title": "Mario + Rabbids: Sparks of Hope", "category": "game"},
        {"title": "Kingdom Come Deliverance 2 DLC", "category": "game"},
        {"title": "Ghostbusters: Frozen Empire", "category": "film_series"},
        {"title": "Gamescom", "category": "misc"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Mafia: The Old Country", "category": "game"},
        {"title": "Wednesday Staffel 2", "category": "film_series"},
        {"title": "Gamescom", "category": "misc"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Fantastic Four", "category": "film_series"},
        {"title": "Die Nackte Kanone", "category": "film_series"},
        {"title": "Barbie", "category": "film_series"},
        {"title": "Alien: Earth", "category": "film_series"},
        {"title": "Wednesday Staffel 2", "category": "film_series"},
    ]},
]

# ── Jul 2025 ─────────────────────────────────────────────────────────────────
JUL_USER_ITEMS = [
    {"username": "Maestro84", "items": [
        {"title": "Reacher", "category": "film_series"},
    ]},
    {"username": "CptTrips", "items": [
        {"title": "Daredevil Comics – Charles Soule", "category": "misc"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Tony Hawk's Pro Skater 3+4", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Tony Hawk's Pro Skater 3+4", "category": "game"},
        {"title": "Donkey Kong Bananza", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "The Rookie", "category": "film_series"},
        {"title": "Children of Silenttown", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "Mario Kart World", "category": "game"},
        {"title": "Fast Fusion", "category": "game"},
        {"title": "Mario + Rabbids: Sparks of Hope", "category": "game"},
        {"title": "Octopath Traveller 2", "category": "game"},
    ]},
    {"username": "Calmon", "items": [
        {"title": "Squid Game Staffel 2", "category": "film_series"},
        {"title": "Terra Invicta", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "The Bear", "category": "film_series"},
        {"title": "Beef", "category": "film_series"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Stalker 2", "category": "game"},
        {"title": "Andor Staffel 2", "category": "film_series"},
        {"title": "Judas Priest Konzert", "category": "misc"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Superman", "category": "film_series"},
        {"title": "Fantastic Four", "category": "film_series"},
        {"title": "F1", "category": "film_series"},
        {"title": "The Old Guard 2", "category": "film_series"},
        {"title": "Tony Hawk's Pro Skater 3+4", "category": "game"},
    ]},
    {"username": "Flooraimer", "items": [
        {"title": "Ich weiß was du letzten Sommer getan hast", "category": "film_series"},
        {"title": "Squid Game Staffel 2", "category": "film_series"},
    ]},
    {"username": "Hendrik", "items": [
        {"title": "Superman", "category": "film_series"},
        {"title": "Fantastic Four", "category": "film_series"},
        {"title": "The Walking Dead Marathon", "category": "film_series"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Death Stranding 2", "category": "game"},
        {"title": "Date Everything", "category": "game"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "Tony Hawk's Pro Skater 3+4", "category": "game"},
        {"title": "Diablo 4", "category": "game"},
    ]},
]

MONTH_DATA = {
    "2025-09": SEP_USER_ITEMS,
    "2025-08": AUG_USER_ITEMS,
    "2025-07": JUL_USER_ITEMS,
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
