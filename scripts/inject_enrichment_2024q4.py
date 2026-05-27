#!/usr/bin/env python3
"""Inject manually-derived user_items for Dec 2024 / Feb–Mar 2025 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Mar 2025 ─────────────────────────────────────────────────────────────────
MAR_USER_ITEMS = [
    {"username": "Q-Bert", "items": [
        {"title": "Zero Day", "category": "film_series"},
        {"title": "The Gorge", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Lost Records: Bloom & Rage", "category": "game"},
        {"title": "1923", "category": "film_series"},
        {"title": "Tonbandgerät Konzert", "category": "misc"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Kingdom Come: Deliverance 2", "category": "game"},
        {"title": "The Day of the Jackal", "category": "film_series"},
        {"title": "Reacher", "category": "film_series"},
        {"title": "The Grand Tour", "category": "film_series"},
    ]},
    {"username": "Markus K.", "items": [
        {"title": "Old World: Wrath of Gods", "category": "game"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Xenoblade Chronicles X: Definitive Edition", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Zelda: Echoes of Wisdom", "category": "game"},
        {"title": "Catquest 3", "category": "game"},
        {"title": "FF7 Rebirth", "category": "game"},
        {"title": "Tesla Effect: A Tex Murphy Adventure", "category": "game"},
        {"title": "Severance", "category": "film_series"},
        {"title": "Zero Day", "category": "film_series"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Tesla Effect: A Tex Murphy Adventure", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Assassin's Creed Shadows", "category": "game"},
        {"title": "Mickey 17", "category": "film_series"},
        {"title": "Daredevil: Born Again", "category": "film_series"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Assassin's Creed Shadows", "category": "game"},
    ]},
    {"username": "jguillemont", "items": [
        {"title": "Two Point Museum", "category": "game"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "Age of Mythology: Retold", "category": "game"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Kingdom Come: Deliverance 2", "category": "game"},
        {"title": "FF7 Rebirth", "category": "game"},
        {"title": "X-Out Resurfaced", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Assassin's Creed Shadows", "category": "game"},
        {"title": "A Complete Unknown", "category": "film_series"},
    ]},
    {"username": "Keppel", "items": [
        {"title": "Daredevil: Born Again", "category": "film_series"},
    ]},
    {"username": "JensJuchzer", "items": [
        {"title": "Reacher", "category": "film_series"},
    ]},
]

# ── Feb 2025 ─────────────────────────────────────────────────────────────────
FEB_USER_ITEMS = [
    {"username": "Alain", "items": [
        {"title": "Severance", "category": "film_series"},
        {"title": "Star Trek: Prodigy", "category": "film_series"},
        {"title": "Zelda: Echoes of Wisdom", "category": "game"},
        {"title": "FF7 Rebirth", "category": "game"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Foundation", "category": "film_series"},
        {"title": "Der Graf von Monte Christo", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Kingdom Come: Deliverance 2", "category": "game"},
    ]},
    {"username": "Bishamon", "items": [
        {"title": "Severance", "category": "film_series"},
        {"title": "Civilization 7", "category": "game"},
        {"title": "Dark Matter", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "The Brutalist", "category": "film_series"},
        {"title": "Indiana Jones und der Große Kreis", "category": "game"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Like a Dragon: Pirate Yakuza in Hawaii", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Kingdom Come: Deliverance 2", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Paprika", "category": "film_series"},
        {"title": "Perfect Blue", "category": "film_series"},
        {"title": "Millennium Actress", "category": "film_series"},
        {"title": "Tokyo Godfathers", "category": "film_series"},
        {"title": "Silent Hill 2 Remake", "category": "game"},
    ]},
    {"username": "Zickendetightbombe", "items": [
        {"title": "Kingdom Come: Deliverance 2", "category": "game"},
    ]},
    {"username": "JarmuschX", "items": [
        {"title": "Schitt's Creek", "category": "film_series"},
        {"title": "Tokyo Vice", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Donkey Kong Country Returns HD", "category": "game"},
        {"title": "Little Big Adventure Remake", "category": "game"},
        {"title": "The Penguin", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "The Rookie", "category": "film_series"},
        {"title": "The Night Agent Staffel 2", "category": "film_series"},
        {"title": "Reacher Staffel 3", "category": "film_series"},
        {"title": "Captain America: Brave New World", "category": "film_series"},
        {"title": "Kingdom Come: Deliverance 2", "category": "game"},
        {"title": "Star Wars Jedi: Survivor", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Like a Dragon: Pirate Yakuza in Hawaii", "category": "game"},
        {"title": "Captain America: Brave New World", "category": "film_series"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Avowed", "category": "game"},
        {"title": "Atomfall", "category": "game"},
        {"title": "Arken Age", "category": "game"},
    ]},
    {"username": "Henmann", "items": [
        {"title": "Indiana Jones und der Große Kreis", "category": "game"},
        {"title": "Paradise", "category": "film_series"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Captain America: Brave New World", "category": "film_series"},
        {"title": "The Monkey", "category": "film_series"},
        {"title": "Cobra Kai", "category": "film_series"},
    ]},
    {"username": "thhko", "items": [
        {"title": "Yellowjackets", "category": "film_series"},
        {"title": "Invincible", "category": "film_series"},
    ]},
]

# ── Dec 2024 ─────────────────────────────────────────────────────────────────
DEC_USER_ITEMS = [
    {"username": "Q-Bert", "items": [
        {"title": "Shrinking", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Prim", "category": "game"},
        {"title": "Kena: Bridge of Spirits", "category": "game"},
        {"title": "Tulsa King Staffel 2", "category": "film_series"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Indiana Jones und der Große Kreis", "category": "game"},
        {"title": "Legacy of Kain: Soul Reaver 1&2 Remastered", "category": "game"},
    ]},
    {"username": "Thomas Schmitz", "items": [
        {"title": "Loco Motive", "category": "game"},
        {"title": "Astro Bot", "category": "game"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Silo", "category": "film_series"},
        {"title": "Indiana Jones und der Große Kreis", "category": "game"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Secret Level", "category": "film_series"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Secret Level", "category": "film_series"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Astro Bot", "category": "game"},
        {"title": "Neva", "category": "game"},
        {"title": "The Plucky Squire", "category": "game"},
        {"title": "Secret Level", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Indiana Jones und der Große Kreis", "category": "game"},
        {"title": "Star Wars: Skeleton Crew", "category": "film_series"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Indiana Jones und der Große Kreis", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "TopSpin 2K25", "category": "game"},
        {"title": "Alone in the Dark", "category": "game"},
        {"title": "RoboCop: Rogue City", "category": "game"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "James Bond", "category": "film_series"},
        {"title": "RoboCop", "category": "film_series"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Path of Exile 2", "category": "game"},
        {"title": "Indiana Jones und der Große Kreis", "category": "game"},
        {"title": "Stalker 2: Heart of Chornobyl", "category": "game"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Der kleine Lord", "category": "film_series"},
        {"title": "What We Do in the Shadows", "category": "film_series"},
        {"title": "Subnautica", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Delicious in Dungeon", "category": "film_series"},
        {"title": "Neon Genesis Evangelion", "category": "film_series"},
        {"title": "Shrinking", "category": "film_series"},
        {"title": "Only Murders in the Building", "category": "film_series"},
        {"title": "Secret Level", "category": "film_series"},
    ]},
    {"username": "Calmon", "items": [
        {"title": "Path of Exile 2", "category": "game"},
        {"title": "Der Herr der Ringe", "category": "film_series"},
        {"title": "The Bazaar", "category": "game"},
    ]},
    {"username": "Maverick", "items": [
        {"title": "Indiana Jones und der Große Kreis", "category": "game"},
        {"title": "Dragon Age: The Veilguard", "category": "game"},
    ]},
    {"username": "MiLe84", "items": [
        {"title": "Star Wars: Outlaws", "category": "game"},
        {"title": "Indiana Jones und der Große Kreis", "category": "game"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "Persona 3: FES", "category": "game"},
        {"title": "Der Pass", "category": "film_series"},
    ]},
]

MONTH_DATA = {
    "2025-03": MAR_USER_ITEMS,
    "2025-02": FEB_USER_ITEMS,
    "2024-12": DEC_USER_ITEMS,
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
