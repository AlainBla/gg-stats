#!/usr/bin/env python3
"""Inject manually-derived user_items for Jun/Jul/Aug 2024 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Aug 2024 ─────────────────────────────────────────────────────────────────
AUG_USER_ITEMS = [
    {"username": "euph", "items": [
        {"title": "Baldur's Gate 3", "category": "game"},
        {"title": "Nintendo World Championships", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Black Myth: Wukong", "category": "game"},
        {"title": "Alien: Romulus", "category": "film_series"},
    ]},
    {"username": "Calmon", "items": [
        {"title": "Alien: Romulus", "category": "film_series"},
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Fabledom", "category": "game"},
    ]},
    {"username": "Hermann Nasenweier", "items": [
        {"title": "Gamescom", "category": "misc"},
    ]},
    {"username": "thoohl", "items": [
        {"title": "Vikings Valhalla", "category": "film_series"},
    ]},
    {"username": "Thomas Schmitz", "items": [
        {"title": "The Bear", "category": "film_series"},
        {"title": "God of War: Ragnarök", "category": "game"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Warhammer 40,000: Space Marine 2", "category": "game"},
        {"title": "Star Wars: Outlaws", "category": "game"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Alien: Romulus", "category": "film_series"},
        {"title": "Elite Dangerous", "category": "game"},
        {"title": "Mass Effect 2", "category": "game"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "House of the Dragon", "category": "film_series"},
        {"title": "Deadpool & Wolverine", "category": "film_series"},
        {"title": "Farming Simulator 22", "category": "game"},
        {"title": "F1 24", "category": "game"},
    ]},
    {"username": "Thalavox", "items": [
        {"title": "Star Wars: Outlaws", "category": "game"},
    ]},
    {"username": "Restrictor81", "items": [
        {"title": "Star Wars: Outlaws", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Borderlands", "category": "film_series"},
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Dustborn", "category": "game"},
        {"title": "Star Wars: Outlaws", "category": "game"},
        {"title": "Visions of Mana", "category": "game"},
    ]},
    {"username": "kurosawa", "items": [
        {"title": "Time Bandits", "category": "film_series"},
    ]},
    {"username": "Pomme", "items": [
        {"title": "Kleo", "category": "film_series"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
    ]},
]

# ── Jul 2024 ─────────────────────────────────────────────────────────────────
JUL_USER_ITEMS = [
    {"username": "Olphas", "items": [
        {"title": "MaXXXine", "category": "film_series"},
        {"title": "Deadpool & Wolverine", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Baldur's Gate 3", "category": "game"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Demon's Souls", "category": "game"},
        {"title": "Final Fantasy XVI", "category": "game"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Deadpool & Wolverine", "category": "film_series"},
        {"title": "Attack on Titan", "category": "film_series"},
        {"title": "Demon Slayer", "category": "film_series"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Elden Ring: Shadow of the Erdtree", "category": "game"},
        {"title": "Alan Wake 2", "category": "game"},
        {"title": "TopSpin 2K25", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Alan Wake 2", "category": "game"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Mass Effect 2", "category": "game"},
        {"title": "Elite Dangerous", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "The Orville", "category": "film_series"},
        {"title": "La Zona", "category": "film_series"},
        {"title": "American Arcadia", "category": "game"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "House of the Dragon", "category": "film_series"},
        {"title": "The Acolyte", "category": "film_series"},
        {"title": "Kinds of Kindness", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Paper Mario: Die Legende vom Äonentor", "category": "game"},
        {"title": "House of the Dragon", "category": "film_series"},
        {"title": "Mayor of Kingstown", "category": "film_series"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Cobra Kai", "category": "film_series"},
        {"title": "Deadpool & Wolverine", "category": "film_series"},
        {"title": "Twisters", "category": "film_series"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Ghost of Tsushima", "category": "game"},
        {"title": "The Acolyte", "category": "film_series"},
    ]},
    {"username": "Harry67", "items": [
        {"title": "Diplomatische Beziehungen", "category": "film_series"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "The Legend of Heroes: Trails Through Daybreak", "category": "game"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Gentlemen", "category": "film_series"},
        {"title": "Aliens: Dark Descent", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
    {"username": "Johannes", "items": [
        {"title": "Beverly Hills Cop: Axel F", "category": "film_series"},
    ]},
]

# ── Jun 2024 ─────────────────────────────────────────────────────────────────
JUN_USER_ITEMS = [
    {"username": "Moe90", "items": [
        {"title": "Elden Ring: Shadow of the Erdtree", "category": "game"},
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Elden Ring: Shadow of the Erdtree", "category": "game"},
    ]},
    {"username": "LRod", "items": [
        {"title": "The Acolyte", "category": "film_series"},
        {"title": "Ghost of Tsushima", "category": "game"},
    ]},
    {"username": "Vampiro", "items": [
        {"title": "Field of Glory: Kingdoms", "category": "game"},
        {"title": "Age of Wonders 4", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Rock im Park", "category": "misc"},
        {"title": "EM 2024", "category": "misc"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "A Quiet Place: Day One", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Baldur's Gate 3", "category": "game"},
    ]},
    {"username": "StefanH", "items": [
        {"title": "Shin Megami Tensei 5: Vengeance", "category": "game"},
    ]},
    {"username": "Rhisdil", "items": [
        {"title": "Victoria 3: Sphere of Influence", "category": "game"},
        {"title": "EM 2024", "category": "misc"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "French Open", "category": "misc"},
        {"title": "EM 2024", "category": "misc"},
    ]},
    {"username": "Kinukawa", "items": [
        {"title": "X4: Foundations", "category": "game"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Elden Ring: Shadow of the Erdtree", "category": "game"},
        {"title": "Shin Megami Tensei 5: Vengeance", "category": "game"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Dune: Part Two", "category": "film_series"},
        {"title": "Elite Dangerous", "category": "game"},
        {"title": "Mass Effect 2", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "EM 2024", "category": "misc"},
        {"title": "Mayor of Kingstown", "category": "film_series"},
        {"title": "House of the Dragon", "category": "film_series"},
        {"title": "Paper Mario: Die Legende vom Äonentor", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "House of the Dragon", "category": "film_series"},
        {"title": "The Boys", "category": "film_series"},
    ]},
    {"username": "Henmann", "items": [
        {"title": "Green Day Konzert", "category": "misc"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "The Acolyte", "category": "film_series"},
        {"title": "Elden Ring: Shadow of the Erdtree", "category": "game"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Elden Ring: Shadow of the Erdtree", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Inside Out 2", "category": "film_series"},
        {"title": "Bramble: The Mountain King", "category": "game"},
        {"title": "Animal Well", "category": "game"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Shogun", "category": "film_series"},
        {"title": "StarCraft II", "category": "game"},
        {"title": "Stellaris", "category": "game"},
        {"title": "Smashing Pumpkins Konzert", "category": "misc"},
    ]},
]

MONTH_DATA = {
    "2024-08": AUG_USER_ITEMS,
    "2024-07": JUL_USER_ITEMS,
    "2024-06": JUN_USER_ITEMS,
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
