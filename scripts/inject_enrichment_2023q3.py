#!/usr/bin/env python3
"""Inject manually-derived user_items for Jul/Aug/Sep 2023 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Sep 2023 ─────────────────────────────────────────────────────────────────
SEP_USER_ITEMS = [
    {"username": "Green Yoshi", "items": [
        {"title": "The Last of Us Staffel 1", "category": "film_series"},
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
        {"title": "Arielle", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
        {"title": "Shadow Gambit: The Cursed Crew", "category": "game"},
        {"title": "F1 23", "category": "game"},
        {"title": "Gran Turismo 7", "category": "game"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
        {"title": "Futurama", "category": "film_series"},
        {"title": "Shadow Gambit: The Cursed Crew", "category": "game"},
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "A Haunting in Venice", "category": "film_series"},
    ]},
    {"username": "Jonas S.", "items": [
        {"title": "Futurama", "category": "film_series"},
        {"title": "The Bear Staffel 2", "category": "film_series"},
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Jack Ryan Staffel 4", "category": "film_series"},
        {"title": "Foundation Staffel 2", "category": "film_series"},
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
        {"title": "Baldur's Gate 3", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Armored Core VI: Fires of Rubicon", "category": "game"},
        {"title": "Starfield", "category": "game"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Baldur's Gate 3", "category": "game"},
        {"title": "Atelier Ryza 3", "category": "game"},
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
    ]},
    {"username": "Slaytanic", "items": [
        {"title": "Baldur's Gate 3", "category": "game"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "Baldur's Gate 3", "category": "game"},
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Marvel's Midnight Suns", "category": "game"},
        {"title": "Elite Dangerous", "category": "game"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
        {"title": "Love, Death & Robots", "category": "film_series"},
    ]},
    {"username": "DerBesserwisser", "items": [
        {"title": "Star Trek: Lower Decks", "category": "film_series"},
    ]},
    {"username": "Maverick", "items": [
        {"title": "Starfield", "category": "game"},
    ]},
    {"username": "rammmses", "items": [
        {"title": "Starfield", "category": "game"},
        {"title": "Cyberpunk 2077: Phantom Liberty", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "Shadow Gambit: The Cursed Crew", "category": "game"},
        {"title": "GhostWire: Tokyo", "category": "game"},
        {"title": "Marvel's Midnight Suns", "category": "game"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "Divinity: Original Sin 2", "category": "game"},
    ]},
]

# ── Aug 2023 ─────────────────────────────────────────────────────────────────
AUG_USER_ITEMS = [
    {"username": "euph", "items": [
        {"title": "The Bear Staffel 2", "category": "film_series"},
    ]},
    {"username": "Nischenliebhaber", "items": [
        {"title": "Babylon 5: The Road Home", "category": "film_series"},
        {"title": "AEW All In", "category": "misc"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "Babylon 5: The Road Home", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
        {"title": "The Lincoln Lawyer", "category": "film_series"},
        {"title": "Shadow Gambit: The Cursed Crew", "category": "game"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Wu-Tang: An American Saga", "category": "film_series"},
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
        {"title": "Oppenheimer", "category": "film_series"},
        {"title": "The Witcher Staffel 3", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Frauen-WM 2023", "category": "misc"},
        {"title": "US Open", "category": "misc"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Special Ops: Lioness", "category": "film_series"},
    ]},
    {"username": "Kinukawa", "items": [
        {"title": "Hanabie Konzert", "category": "misc"},
    ]},
    {"username": "Aladan", "items": [
        {"title": "Baldur's Gate 3", "category": "game"},
        {"title": "Atlas Fallen", "category": "game"},
        {"title": "Immortals of Aveum", "category": "game"},
        {"title": "Armored Core VI: Fires of Rubicon", "category": "game"},
        {"title": "Sea of Stars", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Oppenheimer", "category": "film_series"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Marvel's Midnight Suns", "category": "game"},
    ]},
    {"username": "Sir MacRand", "items": [
        {"title": "Zelda: Tears of the Kingdom", "category": "game"},
    ]},
    {"username": "Markus K.", "items": [
        {"title": "Baldur's Gate 3", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "A Plague Tale: Requiem", "category": "game"},
        {"title": "Placebo Konzert", "category": "misc"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Final Fantasy XVI", "category": "game"},
        {"title": "Gamescom", "category": "misc"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Baldur's Gate 3", "category": "game"},
        {"title": "Stray Gods", "category": "game"},
    ]},
    {"username": "Vampiro", "items": [
        {"title": "Harrow", "category": "film_series"},
    ]},
    {"username": "advfreak", "items": [
        {"title": "Telltale's The Expanse", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Broker", "category": "film_series"},
        {"title": "Mizzurna Falls", "category": "game"},
    ]},
    {"username": "StefanH", "items": [
        {"title": "Baldur's Gate 3", "category": "game"},
    ]},
    {"username": "hotzenrockz", "items": [
        {"title": "Steel Division 2", "category": "game"},
        {"title": "Wartales", "category": "game"},
    ]},
]

# ── Jul 2023 ─────────────────────────────────────────────────────────────────
JUL_USER_ITEMS = [
    {"username": "funrox", "items": [
        {"title": "Indiana Jones und das Rad des Schicksals", "category": "film_series"},
        {"title": "The Witcher Staffel 3", "category": "film_series"},
        {"title": "Hogwarts Legacy", "category": "game"},
        {"title": "A Plague Tale: Requiem", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Attack on Titan", "category": "film_series"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Indiana Jones und das Rad des Schicksals", "category": "film_series"},
        {"title": "Diablo 4", "category": "game"},
    ]},
    {"username": "Dennis Hilla", "items": [
        {"title": "One Piece", "category": "film_series"},
        {"title": "Indiana Jones und das Rad des Schicksals", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "The Witcher Staffel 3", "category": "film_series"},
        {"title": "F1 23", "category": "game"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Silo", "category": "film_series"},
        {"title": "Oppenheimer", "category": "film_series"},
        {"title": "Indiana Jones und das Rad des Schicksals", "category": "film_series"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "The Witcher Staffel 3", "category": "film_series"},
        {"title": "Drive to Survive", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Frauen-WM 2023", "category": "misc"},
        {"title": "Wimbledon", "category": "misc"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Oppenheimer", "category": "film_series"},
    ]},
    {"username": "Borin", "items": [
        {"title": "Only Murders in the Building", "category": "film_series"},
        {"title": "Star Wars: Ahsoka", "category": "film_series"},
        {"title": "Oppenheimer", "category": "film_series"},
    ]},
    {"username": "Thomas Schmitz", "items": [
        {"title": "The Witcher 3: Blood & Wine", "category": "game"},
        {"title": "Far Cry 6", "category": "game"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "The Legend of Heroes: Trails into Reverie", "category": "game"},
    ]},
    {"username": "Brunt", "items": [
        {"title": "Aliens: Dark Descent", "category": "game"},
    ]},
]

MONTH_DATA = {
    "2023-09": SEP_USER_ITEMS,
    "2023-08": AUG_USER_ITEMS,
    "2023-07": JUL_USER_ITEMS,
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
