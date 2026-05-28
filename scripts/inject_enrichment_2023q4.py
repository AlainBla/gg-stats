#!/usr/bin/env python3
"""Inject manually-derived user_items for Oct/Nov/Dec 2023 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Dec 2023 ─────────────────────────────────────────────────────────────────
DEC_USER_ITEMS = [
    {"username": "LRod", "items": [
        {"title": "Warhammer 40,000: Rogue Trader", "category": "game"},
    ]},
    {"username": "StefanH", "items": [
        {"title": "Bravely Default", "category": "game"},
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Pioneers of Pagonia", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Final Fantasy XVI", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Baldur's Gate 3", "category": "game"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Dragon Quest Monsters: The Dark Prince", "category": "game"},
        {"title": "Neon Genesis Evangelion", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "God of War: Ragnarök", "category": "game"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Reacher", "category": "film_series"},
        {"title": "Red Dead Redemption 2", "category": "game"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Cyberpunk 2077", "category": "game"},
        {"title": "Marvel's Midnight Suns", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Indiana Jones und das Rad des Schicksals", "category": "film_series"},
        {"title": "Godzilla Minus One", "category": "film_series"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "1923", "category": "film_series"},
    ]},
    {"username": "Henmann", "items": [
        {"title": "Days Gone", "category": "game"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Shadow Gambit: The Cursed Crew", "category": "game"},
    ]},
    {"username": "Slaytanic", "items": [
        {"title": "Like a Dragon Gaiden: The Man Who Erased His Name", "category": "game"},
    ]},
    {"username": "Hyperbolic", "items": [
        {"title": "Godzilla Minus One", "category": "film_series"},
    ]},
]

# ── Nov 2023 ─────────────────────────────────────────────────────────────────
NOV_USER_ITEMS = [
    {"username": "Crizzo", "items": [
        {"title": "Napoleon", "category": "film_series"},
        {"title": "Loki", "category": "film_series"},
        {"title": "Marvel's Spider-Man 2", "category": "game"},
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Like a Dragon Gaiden: The Man Who Erased His Name", "category": "game"},
        {"title": "Marvel's Spider-Man 2", "category": "game"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "Napoleon", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Napoleon", "category": "film_series"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Alan Wake 2", "category": "game"},
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Spy x Family", "category": "film_series"},
    ]},
    {"username": "Sciron", "items": [
        {"title": "Pluto", "category": "film_series"},
    ]},
    {"username": "Dennis Hilla", "items": [
        {"title": "One Piece", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Lawmen: Bass Reeves", "category": "film_series"},
        {"title": "Final Fantasy XVI", "category": "game"},
        {"title": "Super Mario Bros. Wonder", "category": "game"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Napoleon", "category": "film_series"},
        {"title": "The Hunger Games: The Ballad of Songbirds & Snakes", "category": "film_series"},
        {"title": "The Handmaid's Tale", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Marvel's Spider-Man 2", "category": "game"},
        {"title": "Starfield", "category": "game"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Star Ocean: The Second Story R", "category": "game"},
        {"title": "Like a Dragon Gaiden: The Man Who Erased His Name", "category": "game"},
        {"title": "Persona 5 Tactica", "category": "game"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Like a Dragon Gaiden: The Man Who Erased His Name", "category": "game"},
        {"title": "Persona 5 Tactica", "category": "game"},
        {"title": "Super Mario RPG", "category": "game"},
        {"title": "Star Ocean: The Second Story R", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Attack on Titan", "category": "film_series"},
        {"title": "Alan Wake 2", "category": "game"},
        {"title": "Marvel's Spider-Man 2", "category": "game"},
        {"title": "Super Mario Bros. Wonder", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Age of Empires 4: The Sultans Ascend", "category": "game"},
        {"title": "Persona 5 Tactica", "category": "game"},
    ]},
    {"username": "rammmses", "items": [
        {"title": "RoboCop: Rogue City", "category": "game"},
        {"title": "Like a Dragon Gaiden: The Man Who Erased His Name", "category": "game"},
    ]},
]

# ── Oct 2023 ─────────────────────────────────────────────────────────────────
OCT_USER_ITEMS = [
    {"username": "Green Yoshi", "items": [
        {"title": "Marvel's Spider-Man 2", "category": "game"},
        {"title": "Super Mario Bros. Wonder", "category": "game"},
        {"title": "Alan Wake 2", "category": "game"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Sea of Stars", "category": "game"},
        {"title": "Assassin's Creed Mirage", "category": "game"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Assassin's Creed Mirage", "category": "game"},
        {"title": "Alan Wake 2", "category": "game"},
        {"title": "The Fall of the House of Usher", "category": "film_series"},
        {"title": "Lupin", "category": "film_series"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
        {"title": "Baldur's Gate 3", "category": "game"},
        {"title": "Alan Wake 2", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
        {"title": "Marvel's Spider-Man 2", "category": "game"},
    ]},
    {"username": "Calmon", "items": [
        {"title": "Cyberpunk 2077", "category": "game"},
    ]},
    {"username": "JarmuschX", "items": [
        {"title": "Sea of Stars", "category": "game"},
        {"title": "Final Fantasy XVI", "category": "game"},
        {"title": "Assassin's Creed Mirage", "category": "game"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "Assassin's Creed Mirage", "category": "game"},
        {"title": "Only Murders in the Building", "category": "film_series"},
    ]},
    {"username": "Admiral Anger", "items": [
        {"title": "Super Mario Bros. Wonder", "category": "game"},
    ]},
    {"username": "Sonry", "items": [
        {"title": "Lords of the Fallen", "category": "game"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Gen V", "category": "film_series"},
        {"title": "Lamplighters League", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Only Murders in the Building", "category": "film_series"},
        {"title": "Babylon Berlin", "category": "film_series"},
    ]},
    {"username": "Cpt. Metal", "items": [
        {"title": "Alan Wake 2", "category": "game"},
        {"title": "Marvel's Spider-Man 2", "category": "game"},
        {"title": "WRC 2023", "category": "game"},
    ]},
    {"username": "MiLe84", "items": [
        {"title": "Cities: Skylines 2", "category": "game"},
    ]},
    {"username": "StefanH", "items": [
        {"title": "Loki", "category": "film_series"},
        {"title": "Super Mario Bros. Wonder", "category": "game"},
        {"title": "Metal Gear Solid: Master Collection Vol. 1", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Final Fantasy XVI", "category": "game"},
        {"title": "Super Mario Bros. Wonder", "category": "game"},
        {"title": "Lupin", "category": "film_series"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Star Trek: Infinite", "category": "game"},
    ]},
    {"username": "TSH-Lightning", "items": [
        {"title": "Sea of Stars", "category": "game"},
        {"title": "Domina", "category": "film_series"},
    ]},
    {"username": "Nischenliebhaber", "items": [
        {"title": "Super Mario Bros. Wonder", "category": "game"},
        {"title": "Sonic Superstars", "category": "game"},
        {"title": "Gargoyles Remastered", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Babylon Berlin", "category": "film_series"},
        {"title": "Loki", "category": "film_series"},
        {"title": "The Creator", "category": "film_series"},
        {"title": "Killers of the Flower Moon", "category": "film_series"},
    ]},
    {"username": "Jonas S.", "items": [
        {"title": "The Rookie", "category": "film_series"},
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
        {"title": "Gen V", "category": "film_series"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Super Mario Bros. Wonder", "category": "game"},
    ]},
    {"username": "DerBesserwisser", "items": [
        {"title": "Gen V", "category": "film_series"},
    ]},
    {"username": "marcw11", "items": [
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
    ]},
]

MONTH_DATA = {
    "2023-12": DEC_USER_ITEMS,
    "2023-11": NOV_USER_ITEMS,
    "2023-10": OCT_USER_ITEMS,
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
