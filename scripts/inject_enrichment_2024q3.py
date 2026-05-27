#!/usr/bin/env python3
"""Inject manually-derived user_items for Sep/Oct/Nov 2024 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Nov 2024 ─────────────────────────────────────────────────────────────────
NOV_USER_ITEMS = [
    {"username": "Moe90", "items": [
        {"title": "Stalker 2: Heart of Chornobyl", "category": "game"},
        {"title": "The Penguin", "category": "film_series"},
        {"title": "Monsters", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "ATP Finals", "category": "misc"},
        {"title": "Stalker 2: Heart of Chornobyl", "category": "game"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Silo", "category": "film_series"},
    ]},
    {"username": "Calmon", "items": [
        {"title": "The Bazaar", "category": "game"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Lioness", "category": "film_series"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "The Penguin", "category": "film_series"},
        {"title": "Arcane", "category": "film_series"},
        {"title": "Dune: Prophecy", "category": "film_series"},
        {"title": "The Day of the Jackal", "category": "film_series"},
        {"title": "Yellowstone", "category": "film_series"},
        {"title": "Silo", "category": "film_series"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Only Murders in the Building", "category": "film_series"},
        {"title": "Delicious in Dungeon", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Life Is Strange: Double Exposure", "category": "game"},
        {"title": "Psychonauts 2", "category": "game"},
        {"title": "Tulsa King", "category": "film_series"},
        {"title": "Lioness", "category": "film_series"},
        {"title": "Kleo", "category": "film_series"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Dune: Prophecy", "category": "film_series"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "The Rise of the Golden Idol", "category": "game"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Metro: Awakening", "category": "game"},
        {"title": "Stalker 2: Heart of Chornobyl", "category": "game"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Gladiator 2", "category": "film_series"},
        {"title": "Dune: Prophecy", "category": "film_series"},
        {"title": "The Penguin", "category": "film_series"},
        {"title": "Farming Simulator 25", "category": "game"},
        {"title": "Stalker 2: Heart of Chornobyl", "category": "game"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Stalker 2: Heart of Chornobyl", "category": "game"},
        {"title": "What We Do in the Shadows", "category": "film_series"},
        {"title": "Dritte Wahl Konzert", "category": "misc"},
    ]},
    {"username": "Maverick", "items": [
        {"title": "Stalker 2: Heart of Chornobyl", "category": "game"},
    ]},
    {"username": "rammmses", "items": [
        {"title": "Dragon Age: The Veilguard", "category": "game"},
        {"title": "Stalker 2: Heart of Chornobyl", "category": "game"},
        {"title": "Metro: Awakening", "category": "game"},
    ]},
]

# ── Oct 2024 ─────────────────────────────────────────────────────────────────
OCT_USER_ITEMS = [
    {"username": "funrox", "items": [
        {"title": "Zelda: Echoes of Wisdom", "category": "game"},
        {"title": "Life Is Strange: Double Exposure", "category": "game"},
        {"title": "Slow Horses", "category": "film_series"},
        {"title": "Tulsa King", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Zelda: Echoes of Wisdom", "category": "game"},
        {"title": "Joker: Folie à Deux", "category": "film_series"},
        {"title": "Alien: Romulus", "category": "film_series"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Ys X: Nordics", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Büro der Legenden", "category": "film_series"},
        {"title": "Die Schule der magischen Tiere 3", "category": "film_series"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "Bad Monkey", "category": "film_series"},
        {"title": "Slow Horses", "category": "film_series"},
        {"title": "Baldur's Gate 3", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Silent Hill 2 Remake", "category": "game"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Zelda: Echoes of Wisdom", "category": "game"},
    ]},
    {"username": "paule99", "items": [
        {"title": "Dragon Age: The Veilguard", "category": "game"},
        {"title": "Der Kühne Knappe", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Neva", "category": "game"},
        {"title": "Metaphor: ReFantazio", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Life Is Strange: Double Exposure", "category": "game"},
        {"title": "Silent Hill 2 Remake", "category": "game"},
        {"title": "Alien", "category": "film_series"},
        {"title": "Jordskott", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Life Is Strange: Double Exposure", "category": "game"},
        {"title": "Dragon Age: The Veilguard", "category": "game"},
        {"title": "In Liebe, Eure Hilde", "category": "film_series"},
        {"title": "ATP Tennis", "category": "misc"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "The Crimson Diamond", "category": "game"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "Persona 3: FES", "category": "game"},
    ]},
    {"username": "StefanH", "items": [
        {"title": "Silent Hill 2 Remake", "category": "game"},
        {"title": "Life Is Strange: Double Exposure", "category": "game"},
    ]},
]

# ── Sep 2024 ─────────────────────────────────────────────────────────────────
SEP_USER_ITEMS = [
    {"username": "Toxoplasmaa", "items": [
        {"title": "World of Warcraft: The War Within", "category": "game"},
        {"title": "Warhammer 40,000: Space Marine 2", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "Astro Bot", "category": "game"},
    ]},
    {"username": "advfreak", "items": [
        {"title": "Astro Bot", "category": "game"},
        {"title": "The Casting of Frank Stone", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Agatha All Along", "category": "film_series"},
    ]},
    {"username": "Quirk", "items": [
        {"title": "Frostpunk 2", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Astro Bot", "category": "game"},
        {"title": "Age of Mythology: Retold", "category": "game"},
        {"title": "Baphomets Fluch Remaster", "category": "game"},
        {"title": "Zelda: Echoes of Wisdom", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Slow Horses", "category": "film_series"},
        {"title": "Astro Bot", "category": "game"},
        {"title": "Emio – The Smiling Man", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Slow Horses", "category": "film_series"},
        {"title": "Zelda: Echoes of Wisdom", "category": "game"},
        {"title": "Mayor of Kingstown", "category": "film_series"},
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
        {"title": "Tulsa King", "category": "film_series"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Warhammer 40,000: Space Marine 2", "category": "game"},
        {"title": "Final Fantasy XVI", "category": "game"},
        {"title": "Star Wars: Outlaws", "category": "game"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Astro Bot", "category": "game"},
        {"title": "Warhammer 40,000: Space Marine 2", "category": "game"},
        {"title": "Test Drive Unlimited Solar Crown", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Final Fantasy XVI", "category": "game"},
        {"title": "Warhammer 40,000: Space Marine 2", "category": "game"},
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
    {"username": "Henmann", "items": [
        {"title": "Only Murders in the Building", "category": "film_series"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Zelda: Echoes of Wisdom", "category": "game"},
    ]},
    {"username": "Timberwolf", "items": [
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
        {"title": "House of the Dragon", "category": "film_series"},
        {"title": "Terminator Zero", "category": "film_series"},
        {"title": "World of Warcraft: The War Within", "category": "game"},
    ]},
    {"username": "JarmuschX", "items": [
        {"title": "Astro Bot", "category": "game"},
        {"title": "Star Wars: Outlaws", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "The Casting of Frank Stone", "category": "game"},
        {"title": "Astro Bot", "category": "game"},
        {"title": "Zelda: Echoes of Wisdom", "category": "game"},
    ]},
    {"username": "stetra", "items": [
        {"title": "Age of Mythology: Retold", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Age of Mythology: Retold", "category": "game"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Yellowstone", "category": "film_series"},
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
        {"title": "Sumerian Six", "category": "game"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "The Lost Files of Sherlock Holmes", "category": "game"},
        {"title": "Elden Ring: Shadow of the Erdtree", "category": "game"},
    ]},
    {"username": "Thomas Schmitz", "items": [
        {"title": "God of War: Ragnarök", "category": "game"},
        {"title": "Nobody Wants to Die", "category": "game"},
    ]},
    {"username": "Berndor", "items": [
        {"title": "Astro Bot", "category": "game"},
        {"title": "Star Wars: Outlaws", "category": "game"},
        {"title": "God of War: Ragnarök", "category": "game"},
    ]},
    {"username": "duchess", "items": [
        {"title": "Gilmore Girls", "category": "film_series"},
    ]},
    {"username": "Sonyboy", "items": [
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
        {"title": "Horizon: An American Saga", "category": "film_series"},
    ]},
]

MONTH_DATA = {
    "2024-11": NOV_USER_ITEMS,
    "2024-10": OCT_USER_ITEMS,
    "2024-09": SEP_USER_ITEMS,
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
