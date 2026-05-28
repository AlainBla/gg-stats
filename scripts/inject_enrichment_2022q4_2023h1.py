#!/usr/bin/env python3
"""Inject manually-derived user_items for Dec 2022 and Feb–Jun 2023 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Jun 2023 ─────────────────────────────────────────────────────────────────
JUN_USER_ITEMS = [
    {"username": "StefanH", "items": [
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
        {"title": "Street Fighter 6", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Spider-Man: Across the Spider-Verse", "category": "film_series"},
        {"title": "The Flash", "category": "film_series"},
        {"title": "Indiana Jones und das Rad des Schicksals", "category": "film_series"},
        {"title": "Secret Invasion", "category": "film_series"},
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Silo", "category": "film_series"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Final Fantasy XVI", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "A Plague Tale: Requiem", "category": "game"},
        {"title": "Hogwarts Legacy", "category": "game"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Jack Ryan Staffel 4", "category": "film_series"},
        {"title": "Diablo 4", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Succession Staffel 4", "category": "film_series"},
        {"title": "Telltale's The Expanse", "category": "game"},
    ]},
    {"username": "paule99", "items": [
        {"title": "Iron Maiden Konzert", "category": "misc"},
        {"title": "Diablo 4", "category": "game"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Final Fantasy XVI", "category": "game"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "Blood & Gold", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Final Fantasy XVI", "category": "game"},
        {"title": "French Open", "category": "misc"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Diablo 4", "category": "game"},
        {"title": "Final Fantasy XVI", "category": "game"},
        {"title": "Star Trek: Resurgence", "category": "game"},
    ]},
    {"username": "LRod", "items": [
        {"title": "System Shock Remake", "category": "game"},
        {"title": "Indiana Jones und das Rad des Schicksals", "category": "film_series"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Diablo 4", "category": "game"},
        {"title": "Aliens: Dark Descent", "category": "game"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Diablo 4", "category": "game"},
        {"title": "Telltale's The Expanse", "category": "game"},
        {"title": "Indiana Jones und das Rad des Schicksals", "category": "film_series"},
        {"title": "Elemental", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "F1 23", "category": "game"},
        {"title": "The Witcher Staffel 3", "category": "film_series"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "Borderlands 3", "category": "game"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Final Fantasy VII", "category": "game"},
    ]},
]

# ── May 2023 ─────────────────────────────────────────────────────────────────
MAY_USER_ITEMS = [
    {"username": "Hannes Herrmann", "items": [
        {"title": "Age of Wonders 4", "category": "game"},
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
        {"title": "Der Pass Staffel 3", "category": "film_series"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "Star Trek: Resurgence", "category": "game"},
        {"title": "Guardians of the Galaxy Vol. 3", "category": "film_series"},
        {"title": "Star Trek: Strange New Worlds", "category": "film_series"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Jack Ryan Staffel 3", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
        {"title": "French Open", "category": "misc"},
        {"title": "Elton John Konzert", "category": "misc"},
    ]},
    {"username": "funrox", "items": [
        {"title": "A Plague Tale: Requiem", "category": "game"},
        {"title": "Hogwarts Legacy", "category": "game"},
        {"title": "Der Pass Staffel 3", "category": "film_series"},
    ]},
    {"username": "Nischenliebhaber", "items": [
        {"title": "Babylon 5: The Road Home", "category": "film_series"},
    ]},
    {"username": "advfreak", "items": [
        {"title": "Star Trek: Resurgence", "category": "game"},
        {"title": "Eurovision Song Contest", "category": "misc"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
    ]},
    {"username": "CptTrips", "items": [
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Age of Empires 2: Return of Rome", "category": "game"},
        {"title": "Warhammer 40K: Boltgun", "category": "game"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
        {"title": "Star Trek: Strange New Worlds", "category": "film_series"},
    ]},
    {"username": "paule99", "items": [
        {"title": "Diablo 4", "category": "game"},
        {"title": "Star Wars Jedi: Survivor", "category": "game"},
    ]},
    {"username": "Henmann", "items": [
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
        {"title": "Guardians of the Galaxy Vol. 3", "category": "film_series"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "System Shock Remake", "category": "game"},
        {"title": "Succession Staffel 4", "category": "film_series"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Star Wars Jedi: Survivor", "category": "game"},
    ]},
]

# ── Apr 2023 ─────────────────────────────────────────────────────────────────
APR_USER_ITEMS = [
    {"username": "Maestro84", "items": [
        {"title": "John Wick: Chapter 4", "category": "film_series"},
        {"title": "Dungeons & Dragons: Honor Among Thieves", "category": "film_series"},
        {"title": "Suzume", "category": "film_series"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Star Wars Jedi: Survivor", "category": "game"},
        {"title": "Ted Lasso Staffel 3", "category": "film_series"},
    ]},
    {"username": "The Real Maulwurfn", "items": [
        {"title": "Dead Island 2", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Resident Evil 4 Remake", "category": "game"},
        {"title": "Star Wars Jedi: Survivor", "category": "game"},
        {"title": "The Super Mario Bros. Movie", "category": "film_series"},
        {"title": "Suzume", "category": "film_series"},
        {"title": "Succession Staffel 4", "category": "film_series"},
    ]},
    {"username": "Vampiro", "items": [
        {"title": "Everspace 2", "category": "game"},
        {"title": "Wartales", "category": "game"},
    ]},
    {"username": "Bobafetta1895", "items": [
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "Horizon Forbidden West: Burning Shores", "category": "game"},
        {"title": "Star Wars Jedi: Survivor", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Suzume", "category": "film_series"},
        {"title": "Days Gone", "category": "game"},
        {"title": "Ghost of Tsushima", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "The Last of Us Staffel 1", "category": "film_series"},
        {"title": "Maneskin Konzert", "category": "misc"},
    ]},
    {"username": "Slaytanic", "items": [
        {"title": "Everspace 2", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Hogwarts Legacy", "category": "game"},
        {"title": "The Last of Us Part II", "category": "game"},
    ]},
    {"username": "Cpt. Metal", "items": [
        {"title": "Resident Evil 4 Remake", "category": "game"},
    ]},
    {"username": "paule99", "items": [
        {"title": "Star Wars Jedi: Survivor", "category": "game"},
    ]},
]

# ── Mar 2023 ─────────────────────────────────────────────────────────────────
MAR_USER_ITEMS = [
    {"username": "funrox", "items": [
        {"title": "The Last of Us Staffel 1", "category": "film_series"},
        {"title": "Hogwarts Legacy", "category": "game"},
        {"title": "A Plague Tale: Requiem", "category": "game"},
    ]},
    {"username": "Kinukawa", "items": [
        {"title": "Bloodywood Konzert", "category": "misc"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Shrinking", "category": "film_series"},
        {"title": "The Mandalorian Staffel 3", "category": "film_series"},
        {"title": "Der Schwarm", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "The Mandalorian Staffel 3", "category": "film_series"},
        {"title": "The Last of Us Staffel 1", "category": "film_series"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Resident Evil 4 Remake", "category": "game"},
    ]},
    {"username": "Drapondur", "items": [
        {"title": "System Shock Remake", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Resident Evil 4 Remake", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Ant-Man and the Wasp: Quantumania", "category": "film_series"},
        {"title": "John Wick: Chapter 4", "category": "film_series"},
        {"title": "Star Trek: Picard Staffel 3", "category": "film_series"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Ted Lasso Staffel 3", "category": "film_series"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Scream 6", "category": "film_series"},
        {"title": "Elite Dangerous", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "The Great War: Western Front", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "System Shock Remake", "category": "game"},
        {"title": "Resident Evil 4 Remake", "category": "game"},
        {"title": "Star Trek: Picard Staffel 3", "category": "film_series"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Resident Evil 4 Remake", "category": "game"},
        {"title": "System Shock Remake", "category": "game"},
        {"title": "The Mandalorian Staffel 3", "category": "film_series"},
    ]},
    {"username": "sneaker23", "items": [
        {"title": "Der Schwarm", "category": "film_series"},
        {"title": "System Shock Remake", "category": "game"},
    ]},
    {"username": "Rialdar", "items": [
        {"title": "Dungeons & Dragons: Honor Among Thieves", "category": "film_series"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Forza Horizon 5: Rally Adventure", "category": "game"},
    ]},
    {"username": "CptTrips", "items": [
        {"title": "System Shock Remake", "category": "game"},
        {"title": "Resident Evil 4 Remake", "category": "game"},
    ]},
    {"username": "Slaytanic", "items": [
        {"title": "System Shock Remake", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Resident Evil 4 Remake", "category": "game"},
        {"title": "System Shock Remake", "category": "game"},
        {"title": "The Last of Us Staffel 1", "category": "film_series"},
    ]},
    {"username": "Calmon", "items": [
        {"title": "Star Trek: Picard Staffel 3", "category": "film_series"},
    ]},
]

# ── Feb 2023 ─────────────────────────────────────────────────────────────────
FEB_USER_ITEMS = [
    {"username": "Crizzo", "items": [
        {"title": "Company of Heroes 3", "category": "game"},
        {"title": "The Last of Us Staffel 1", "category": "film_series"},
        {"title": "Star Wars: The Bad Batch", "category": "film_series"},
        {"title": "Drive to Survive", "category": "film_series"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Star Wars: The Bad Batch", "category": "film_series"},
        {"title": "Blood Bowl 3", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Hogwarts Legacy", "category": "game"},
        {"title": "Hi-Fi Rush", "category": "game"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Hogwarts Legacy", "category": "game"},
        {"title": "Atomic Heart", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Everything Everywhere All At Once", "category": "film_series"},
    ]},
    {"username": "Restrictor81", "items": [
        {"title": "Ant-Man and the Wasp: Quantumania", "category": "film_series"},
        {"title": "Star Trek: Picard Staffel 3", "category": "film_series"},
        {"title": "Hogwarts Legacy", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Carnival Row Staffel 2", "category": "film_series"},
        {"title": "The Last of Us Staffel 1", "category": "film_series"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Dead Space Remake", "category": "game"},
        {"title": "Hi-Fi Rush", "category": "game"},
        {"title": "Hogwarts Legacy", "category": "game"},
        {"title": "Atomic Heart", "category": "game"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Hogwarts Legacy", "category": "game"},
        {"title": "Atomic Heart", "category": "game"},
        {"title": "Super Bowl", "category": "misc"},
    ]},
    {"username": "euph", "items": [
        {"title": "Everything Everywhere All At Once", "category": "film_series"},
        {"title": "The Last of Us Staffel 1", "category": "film_series"},
        {"title": "Hi-Fi Rush", "category": "game"},
    ]},
    {"username": "Pomme", "items": [
        {"title": "The Last of Us Staffel 1", "category": "film_series"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Star Trek: Picard Staffel 3", "category": "film_series"},
    ]},
    {"username": "Berndor", "items": [
        {"title": "Octopath Traveler II", "category": "game"},
        {"title": "Hogwarts Legacy", "category": "game"},
    ]},
    {"username": "jguillemont", "items": [
        {"title": "The Last of Us Staffel 1", "category": "film_series"},
        {"title": "Sons of the Forest", "category": "game"},
    ]},
]

# ── Dec 2022 ─────────────────────────────────────────────────────────────────
DEC_USER_ITEMS = [
    {"username": "Maestro84", "items": [
        {"title": "Avatar 2", "category": "film_series"},
    ]},
    {"username": "Vampiro", "items": [
        {"title": "Unity of Command 2: Desert Fox", "category": "game"},
        {"title": "Master of Magic", "category": "game"},
        {"title": "Steel Division 2: Blood Feud in Transylvania", "category": "game"},
    ]},
    {"username": "Maverick", "items": [
        {"title": "Evercade EXP", "category": "misc"},
        {"title": "Master of Magic", "category": "game"},
        {"title": "Marvel's Midnight Suns", "category": "game"},
    ]},
    {"username": "Slaytanic", "items": [
        {"title": "Evercade EXP", "category": "misc"},
        {"title": "Marvel's Midnight Suns", "category": "game"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Marvel's Midnight Suns", "category": "game"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "High on Life", "category": "game"},
        {"title": "Jack Ryan", "category": "film_series"},
        {"title": "Guillermo del Toro's Pinocchio", "category": "film_series"},
        {"title": "Glass Onion: A Knives Out Mystery", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "The Witcher: Blood Origin", "category": "film_series"},
    ]},
    {"username": "Restrictor81", "items": [
        {"title": "High on Life", "category": "game"},
        {"title": "Avatar 2", "category": "film_series"},
        {"title": "Black Panther: Wakanda Forever", "category": "film_series"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "The Callisto Protocol", "category": "game"},
    ]},
    {"username": "StefanH", "items": [
        {"title": "Marvel's Midnight Suns", "category": "game"},
        {"title": "Dragon Quest Treasures", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "A Plague Tale: Requiem", "category": "game"},
        {"title": "Wednesday", "category": "film_series"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "God of War: Ragnarök", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Avatar 2", "category": "film_series"},
        {"title": "Star Wars: Andor", "category": "film_series"},
        {"title": "Marvel's Midnight Suns", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Black Panther: Wakanda Forever", "category": "film_series"},
        {"title": "Avatar 2", "category": "film_series"},
        {"title": "Glass Onion: A Knives Out Mystery", "category": "film_series"},
        {"title": "Guillermo del Toro's Pinocchio", "category": "film_series"},
    ]},
    {"username": "vanni727", "items": [
        {"title": "Alice in Borderland Staffel 2", "category": "film_series"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Marvel's Midnight Suns", "category": "game"},
        {"title": "Cyberpunk 2077", "category": "game"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "Outriders: Worldslayer", "category": "game"},
    ]},
    {"username": "Zack", "items": [
        {"title": "Master of Magic", "category": "game"},
        {"title": "Knights of Honor II: Sovereign", "category": "game"},
    ]},
]

MONTH_DATA = {
    "2023-06": JUN_USER_ITEMS,
    "2023-05": MAY_USER_ITEMS,
    "2023-04": APR_USER_ITEMS,
    "2023-03": MAR_USER_ITEMS,
    "2023-02": FEB_USER_ITEMS,
    "2022-12": DEC_USER_ITEMS,
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
