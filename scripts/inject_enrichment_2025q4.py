#!/usr/bin/env python3
"""Inject manually-derived user_items for Oct/Nov/Dec 2025 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Dec 2025 ─────────────────────────────────────────────────────────────────
DEC_USER_ITEMS = [
    {"username": "funrox", "items": [
        {"title": "Stranger Things Staffel 5", "category": "film_series"},
        {"title": "Slow Horses", "category": "film_series"},
        {"title": "Tulsa King", "category": "film_series"},
        {"title": "Stromberg Film", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Call My Agent", "category": "film_series"},
        {"title": "Stranger Things Staffel 5", "category": "film_series"},
        {"title": "Clair Obscur: Expedition 33", "category": "game"},
        {"title": "Death Stranding 2", "category": "game"},
        {"title": "Metroid Prime 4: Beyond", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Kingdom Come Deliverance 2 – Mysteria Ecclesia", "category": "game"},
        {"title": "Warfare", "category": "film_series"},
        {"title": "Anora", "category": "film_series"},
        {"title": "Stranger Things Staffel 5", "category": "film_series"},
        {"title": "A House of Dynamite", "category": "film_series"},
        {"title": "Wake Up Dead Man: A Knives Out Mystery", "category": "film_series"},
        {"title": "Monster: The Ed Gein Story", "category": "film_series"},
        {"title": "Retro Gamer Sonderheft 90er", "category": "misc"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Stromberg Film", "category": "film_series"},
        {"title": "Stranger Things Staffel 5", "category": "film_series"},
        {"title": "Metroid Prime 4: Beyond", "category": "game"},
        {"title": "Marvel: Cosmic Invasion", "category": "game"},
        {"title": "Vierschanzentournee", "category": "misc"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Metroid Prime 4: Beyond", "category": "game"},
        {"title": "Thief VR: Legacy of Shadow", "category": "game"},
        {"title": "Troll 2", "category": "film_series"},
    ]},
    {"username": "Tasmanius", "items": [
        {"title": "Weihnachten", "category": "misc"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Man on the Inside Staffel 2", "category": "film_series"},
        {"title": "The Pentaverate", "category": "film_series"},
        {"title": "Billionaires' Bunker", "category": "film_series"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Metroid Prime 4: Beyond", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Strange New Worlds Staffel 3", "category": "film_series"},
        {"title": "Dexter: Resurrection", "category": "film_series"},
        {"title": "A House of Dynamite", "category": "film_series"},
        {"title": "Wake Up Dead Man: A Knives Out Mystery", "category": "film_series"},
        {"title": "Avatar: Fire and Ash", "category": "film_series"},
        {"title": "Pioneers of Pagonia", "category": "game"},
    ]},
    {"username": "Flooraimer", "items": [
        {"title": "Wake Up Dead Man: A Knives Out Mystery", "category": "film_series"},
        {"title": "Eddington", "category": "film_series"},
        {"title": "Marvel: Cosmic Invasion", "category": "game"},
        {"title": "Routine", "category": "game"},
    ]},
]

# ── Nov 2025 ─────────────────────────────────────────────────────────────────
NOV_USER_ITEMS = [
    {"username": "Sokar", "items": [
        {"title": "Age of Mythology Retold – Arena of the Gods", "category": "game"},
        {"title": "Age of Mythology Retold – Heavenly Spear", "category": "game"},
        {"title": "Age of Empires 2 DE – Chronicles DLC", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Marvel's Deadpool VR", "category": "game"},
        {"title": "Stranger Things Staffel 5", "category": "film_series"},
        {"title": "ATP Finals", "category": "misc"},
    ]},
    {"username": "Tasmanius", "items": [
        {"title": "Weihnachten", "category": "misc"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "The Witcher Staffel 4", "category": "film_series"},
        {"title": "Kingdom Come Deliverance 2 DLC", "category": "game"},
        {"title": "Project Motor Racing", "category": "game"},
        {"title": "LS25 Highland Fishing DLC", "category": "game"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Wake Up Dead Man: A Knives Out Mystery", "category": "film_series"},
        {"title": "The Witcher", "category": "film_series"},
        {"title": "World of Warcraft", "category": "game"},
        {"title": "Ale Abbey", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "Mafia: The Old Country", "category": "game"},
        {"title": "Der Kühne Knappe", "category": "game"},
        {"title": "Super Mario Galaxy 2", "category": "game"},
    ]},
    {"username": "Vampiro", "items": [
        {"title": "Europa Universalis 5", "category": "game"},
        {"title": "Flashpoint Campaigns: Cold War", "category": "game"},
        {"title": "Age of Wonders 4 DLC", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Call of Duty: Black Ops 7", "category": "game"},
        {"title": "Planescape: Torment", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Kingdom Come Deliverance 2 – Mysteria Ecclesia", "category": "game"},
        {"title": "Stranger Things Staffel 5", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Tulsa King neue Staffel", "category": "film_series"},
        {"title": "Mayor of Kingstown neue Staffel", "category": "film_series"},
        {"title": "Slow Horses", "category": "film_series"},
        {"title": "The Witcher Staffel 4", "category": "film_series"},
        {"title": "Stranger Things Staffel 5", "category": "film_series"},
        {"title": "Banishers: Ghosts of New Eden", "category": "game"},
        {"title": "Mafia: The Old Country", "category": "game"},
        {"title": "Roxette Konzert", "category": "misc"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Stranger Things Staffel 5", "category": "film_series"},
    ]},
    {"username": "Alain", "items": [
        {"title": "A House of Dynamite", "category": "film_series"},
        {"title": "Thursday Murder Club", "category": "film_series"},
        {"title": "Slow Horses", "category": "film_series"},
        {"title": "Jackie Chan Filme", "category": "film_series"},
        {"title": "Ranma ½", "category": "film_series"},
        {"title": "Sakamoto Days", "category": "film_series"},
    ]},
    {"username": "Gucky", "items": [
        {"title": "Predator: Badlands", "category": "film_series"},
        {"title": "Running Man", "category": "film_series"},
        {"title": "Robin Hood Serie", "category": "film_series"},
    ]},
    {"username": "Flooraimer", "items": [
        {"title": "Eddington", "category": "film_series"},
        {"title": "Predator: Badlands", "category": "film_series"},
    ]},
    {"username": "Hermann Nasenweier", "items": [
        {"title": "Hogwarts Legacy", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Strange New Worlds neue Staffel", "category": "film_series"},
        {"title": "Dexter: Resurrection", "category": "film_series"},
        {"title": "Running Man", "category": "film_series"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Outlaws Remastered", "category": "game"},
    ]},
]

# ── Oct 2025 ─────────────────────────────────────────────────────────────────
OCT_USER_ITEMS = [
    {"username": "Green Yoshi", "items": [
        {"title": "Splinter Cell Serie", "category": "film_series"},
        {"title": "ATP Masters Paris", "category": "misc"},
    ]},
    {"username": "euph", "items": [
        {"title": "Hades 2", "category": "game"},
        {"title": "The Bear Staffel 4", "category": "film_series"},
        {"title": "Alien Earth", "category": "film_series"},
        {"title": "Tron: Ares", "category": "film_series"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Age of Mythology Retold – Heavenly Spear", "category": "game"},
        {"title": "Age of Empires 4 – Chronicles DLC", "category": "game"},
    ]},
    {"username": "Batwayne", "items": [
        {"title": "Jurassic World 4", "category": "film_series"},
        {"title": "Mission Impossible 8", "category": "film_series"},
        {"title": "Superman", "category": "film_series"},
        {"title": "Dirt 5", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Banishers: Ghosts of New Eden", "category": "game"},
        {"title": "Psychonauts 2", "category": "game"},
        {"title": "Simon the Sorcerer", "category": "game"},
        {"title": "Of Monsters and Men Album", "category": "misc"},
    ]},
    {"username": "Flooraimer", "items": [
        {"title": "Blood & Sinners", "category": "film_series"},
        {"title": "The Smashing Machine", "category": "film_series"},
        {"title": "Digimon Story: Time Stranger", "category": "game"},
        {"title": "Vampire: The Masquerade – Bloodlines 2", "category": "game"},
        {"title": "Arc Raiders", "category": "game"},
        {"title": "Mina the Hollower", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Ghost of Yotei", "category": "game"},
        {"title": "Assassin's Creed Shadows Addon", "category": "game"},
        {"title": "Silent Hill f", "category": "game"},
        {"title": "Super Mario Galaxy 1 & 2", "category": "game"},
        {"title": "Vampire: The Masquerade – Bloodlines 2", "category": "game"},
        {"title": "Shogun", "category": "film_series"},
        {"title": "Andor Staffel 2", "category": "film_series"},
        {"title": "Alien Earth", "category": "film_series"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Die Schule der magischen Tiere 4", "category": "film_series"},
        {"title": "Only Murders in the Building Staffel 5", "category": "film_series"},
        {"title": "Alien Earth", "category": "film_series"},
        {"title": "Tulsa King", "category": "film_series"},
        {"title": "Strange New Worlds", "category": "film_series"},
        {"title": "Red Matter", "category": "game"},
        {"title": "Half-Life: Alyx", "category": "game"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Ghost of Yotei", "category": "game"},
        {"title": "Tron: Ares", "category": "film_series"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "Borderlands 3", "category": "game"},
        {"title": "Tatort", "category": "film_series"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Super Mario Galaxy 1 & 2", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Hades 2", "category": "game"},
        {"title": "Ghost of Yotei", "category": "game"},
        {"title": "Rise of the Golden Idol DLC", "category": "game"},
        {"title": "Only Murders in the Building Staffel 5", "category": "film_series"},
        {"title": "Slow Horses", "category": "film_series"},
        {"title": "Tron: Ares", "category": "film_series"},
    ]},
    {"username": "rammmses", "items": [
        {"title": "Vampire: The Masquerade – Bloodlines 2", "category": "game"},
        {"title": "The Outer Worlds 2", "category": "game"},
        {"title": "Silent Hill f", "category": "game"},
        {"title": "Dying Light: The Beast", "category": "game"},
        {"title": "Frostpunk 2", "category": "game"},
    ]},
    {"username": "toreyam", "items": [
        {"title": "Space Scum", "category": "game"},
    ]},
    {"username": "TSH-Lightning", "items": [
        {"title": "Trails in the Sky: First Chapter", "category": "game"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Final Fantasy Tactics", "category": "game"},
        {"title": "Yooka-Replaylee", "category": "game"},
        {"title": "Dragon Quest I & II HD-2D-Remake", "category": "game"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "City Hunter", "category": "film_series"},
        {"title": "Cat's Eye", "category": "film_series"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Tron: Ares", "category": "film_series"},
    ]},
    {"username": "Chorazeck", "items": [
        {"title": "PanzerCorps Grand Campaign", "category": "game"},
        {"title": "Pokémon Legenden: Z-A", "category": "game"},
    ]},
]

MONTH_DATA = {
    "2025-12": DEC_USER_ITEMS,
    "2025-11": NOV_USER_ITEMS,
    "2025-10": OCT_USER_ITEMS,
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
