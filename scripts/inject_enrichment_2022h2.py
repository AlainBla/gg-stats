#!/usr/bin/env python3
"""Inject manually-derived user_items for Jun–Nov 2022 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Nov 2022 ──────────────────────────────────────────────────────────────────
NOV_USER_ITEMS = [
    {"username": "Aladan", "items": [
        {"title": "God of War: Ragnarök", "category": "game"},
        {"title": "Black Panther: Wakanda Forever", "category": "film_series"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "God of War: Ragnarök", "category": "game"},
        {"title": "Bayonetta 3", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "1899", "category": "film_series"},
        {"title": "A Plague Tale: Requiem", "category": "game"},
    ]},
    {"username": "Vampiro", "items": [
        {"title": "Steel Division 2", "category": "game"},
        {"title": "Terra Invicta", "category": "game"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "The Peripheral", "category": "film_series"},
        {"title": "Star Wars: Andor", "category": "film_series"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Tactics Ogre: Reborn", "category": "game"},
        {"title": "Front Mission 1st Remake", "category": "game"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Warhammer 40K: Darktide", "category": "game"},
    ]},
    {"username": "Berndor", "items": [
        {"title": "God of War: Ragnarök", "category": "game"},
    ]},
    {"username": "Restrictor81", "items": [
        {"title": "Black Panther: Wakanda Forever", "category": "film_series"},
        {"title": "The Crown", "category": "film_series"},
        {"title": "1899", "category": "film_series"},
    ]},
    {"username": "The Real Maulwurfn", "items": [
        {"title": "The Hu Konzert", "category": "misc"},
    ]},
    {"username": "Drapondur", "items": [
        {"title": "God of War: Ragnarök", "category": "game"},
        {"title": "The Devil in Me", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "God of War: Ragnarök", "category": "game"},
        {"title": "Pentiment", "category": "game"},
        {"title": "1899", "category": "film_series"},
    ]},
    {"username": "Red Dox", "items": [
        {"title": "Warhammer 40K: Darktide", "category": "game"},
        {"title": "The Rookie Staffel 5", "category": "film_series"},
        {"title": "Black Panther: Wakanda Forever", "category": "film_series"},
        {"title": "Wednesday", "category": "film_series"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Mythic Quest Staffel 3", "category": "film_series"},
        {"title": "For All Mankind Staffel 3", "category": "film_series"},
        {"title": "The Crown", "category": "film_series"},
        {"title": "1899", "category": "film_series"},
    ]},
    {"username": "Henmann", "items": [
        {"title": "Return to Monkey Island", "category": "game"},
        {"title": "The Walking Dead", "category": "film_series"},
        {"title": "The Peripheral", "category": "film_series"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "The Peripheral", "category": "film_series"},
    ]},
    {"username": "Borin", "items": [
        {"title": "Star Wars: Andor", "category": "film_series"},
        {"title": "Guillermo del Toro's Pinocchio", "category": "film_series"},
        {"title": "God of War: Ragnarök", "category": "game"},
    ]},
    {"username": "Micha", "items": [
        {"title": "Pokémon Scarlet", "category": "game"},
    ]},
    {"username": "Hyperbolic", "items": [
        {"title": "Porcupine Tree Konzert", "category": "misc"},
    ]},
    {"username": "Gekko Goodkat", "items": [
        {"title": "God of War: Ragnarök", "category": "game"},
        {"title": "The Peripheral", "category": "film_series"},
    ]},
    {"username": "Necromanus", "items": [
        {"title": "God of War: Ragnarök", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
]

# ── Oct 2022 ──────────────────────────────────────────────────────────────────
OCT_USER_ITEMS = [
    {"username": "Noodles", "items": [
        {"title": "House of the Dragon", "category": "film_series"},
        {"title": "Babylon Berlin Staffel 4", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Babylon Berlin Staffel 4", "category": "film_series"},
        {"title": "Halloween Ends", "category": "film_series"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Bayonetta 3", "category": "game"},
        {"title": "The Legend of Heroes: Trails from Zero", "category": "game"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Lost Eidolons", "category": "game"},
        {"title": "Star Wars: Andor", "category": "film_series"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Halloween Ends", "category": "film_series"},
        {"title": "Elite Dangerous", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Return to Monkey Island", "category": "game"},
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
    {"username": "Maverick", "items": [
        {"title": "Scorn", "category": "game"},
        {"title": "A Plague Tale: Requiem", "category": "game"},
    ]},
    {"username": "Restrictor81", "items": [
        {"title": "Return to Monkey Island", "category": "game"},
        {"title": "Halloween Ends", "category": "film_series"},
    ]},
    {"username": "DerBesserwisser", "items": [
        {"title": "Star Trek: Lower Decks Staffel 3", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Bayonetta 3", "category": "game"},
        {"title": "A Plague Tale: Requiem", "category": "game"},
    ]},
    {"username": "AlIma", "items": [
        {"title": "Return to Monkey Island", "category": "game"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "The Rookie", "category": "film_series"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
    ]},
    {"username": "Sir MacRand", "items": [
        {"title": "Bayonetta 3", "category": "game"},
    ]},
]

# ── Sep 2022 ──────────────────────────────────────────────────────────────────
SEP_USER_ITEMS = [
    {"username": "Kinukawa", "items": [
        {"title": "Star Wars: Andor", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Return to Monkey Island", "category": "game"},
        {"title": "Counting Crows Konzert", "category": "misc"},
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
        {"title": "Star Wars: Andor", "category": "film_series"},
        {"title": "Red Dead Redemption 2", "category": "game"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "The Legend of Heroes: Trails from Zero", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Return to Monkey Island", "category": "game"},
        {"title": "Immortality", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Cobra Kai Staffel 5", "category": "film_series"},
        {"title": "She-Hulk", "category": "film_series"},
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
    ]},
    {"username": "TSH-Lightning", "items": [
        {"title": "Star Wars: Andor", "category": "film_series"},
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
        {"title": "Return to Monkey Island", "category": "game"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
        {"title": "Return to Monkey Island", "category": "game"},
        {"title": "Star Wars: Andor", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Star Wars: Andor", "category": "film_series"},
        {"title": "Herr der Ringe: Ringe der Macht", "category": "film_series"},
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "She-Hulk", "category": "film_series"},
    ]},
]

# ── Aug 2022 ──────────────────────────────────────────────────────────────────
AUG_USER_ITEMS = [
    {"username": "timeagent", "items": [
        {"title": "Prey", "category": "film_series"},
        {"title": "Elite Dangerous", "category": "game"},
    ]},
    {"username": "Slaytanic", "items": [
        {"title": "Hard West 2", "category": "game"},
        {"title": "F1 Manager 2022", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Better Call Saul Staffel 6", "category": "film_series"},
        {"title": "Red Dead Redemption 2", "category": "game"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Xenoblade Chronicles 3", "category": "game"},
        {"title": "Soul Hackers 2", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Better Call Saul Staffel 6", "category": "film_series"},
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Xenoblade Chronicles 3", "category": "game"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Tocotronic Konzert", "category": "misc"},
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
    {"username": "Alain", "items": [
        {"title": "The Boys Staffel 3", "category": "film_series"},
        {"title": "For All Mankind Staffel 3", "category": "film_series"},
        {"title": "Stray", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "House of the Dragon", "category": "film_series"},
    ]},
    {"username": "Thomas Schmitz", "items": [
        {"title": "Only Murders in the Building Staffel 2", "category": "film_series"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Xenoblade Chronicles 3", "category": "game"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "House of the Dragon", "category": "film_series"},
        {"title": "F1 22", "category": "game"},
    ]},
]

# ── Jul 2022 ──────────────────────────────────────────────────────────────────
JUL_USER_ITEMS = [
    {"username": "funrox", "items": [
        {"title": "Better Call Saul Staffel 6", "category": "film_series"},
        {"title": "Hooters Konzert", "category": "misc"},
        {"title": "Crowns and Pawns", "category": "game"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "Stray", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Thor: Love and Thunder", "category": "film_series"},
        {"title": "Ms. Marvel", "category": "film_series"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Xenoblade Chronicles 3", "category": "game"},
        {"title": "Stray", "category": "game"},
    ]},
    {"username": "marcw11", "items": [
        {"title": "Only Murders in the Building", "category": "film_series"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Better Call Saul Staffel 6", "category": "film_series"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Stray", "category": "game"},
        {"title": "GhostWire: Tokyo", "category": "game"},
        {"title": "Better Call Saul Staffel 6", "category": "film_series"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Xenoblade Chronicles 3", "category": "game"},
        {"title": "Stray", "category": "game"},
        {"title": "For All Mankind Staffel 3", "category": "film_series"},
    ]},
    {"username": "Alain", "items": [
        {"title": "For All Mankind Staffel 3", "category": "film_series"},
        {"title": "Borgen", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Stranger Things Staffel 4", "category": "film_series"},
        {"title": "Deathloop", "category": "game"},
    ]},
]

# ── Jun 2022 ──────────────────────────────────────────────────────────────────
JUN_USER_ITEMS = [
    {"username": "Mike H.", "items": [
        {"title": "Better Call Saul Staffel 6", "category": "film_series"},
        {"title": "The Orville Staffel 3", "category": "film_series"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Lagwagon Konzert", "category": "misc"},
        {"title": "Judas Priest Konzert", "category": "misc"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "The Boys Staffel 3", "category": "film_series"},
        {"title": "Obi-Wan Kenobi", "category": "film_series"},
        {"title": "V Rising", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "Stranger Things Staffel 4", "category": "film_series"},
        {"title": "Everything Everywhere All At Once", "category": "film_series"},
        {"title": "Elden Ring", "category": "game"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "The Boys Staffel 3", "category": "film_series"},
        {"title": "For All Mankind Staffel 3", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Doctor Strange in the Multiverse of Madness", "category": "film_series"},
        {"title": "Top Gun: Maverick", "category": "film_series"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Borgen Staffel 4", "category": "film_series"},
        {"title": "Severance", "category": "film_series"},
        {"title": "The Boys Staffel 3", "category": "film_series"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "The Boys Staffel 3", "category": "film_series"},
        {"title": "Peaky Blinders", "category": "film_series"},
        {"title": "Westworld", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Obi-Wan Kenobi", "category": "film_series"},
        {"title": "French Open", "category": "misc"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Star Trek: Strange New Worlds", "category": "film_series"},
    ]},
]

MONTH_DATA = {
    "2022-11": NOV_USER_ITEMS,
    "2022-10": OCT_USER_ITEMS,
    "2022-09": SEP_USER_ITEMS,
    "2022-08": AUG_USER_ITEMS,
    "2022-07": JUL_USER_ITEMS,
    "2022-06": JUN_USER_ITEMS,
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
