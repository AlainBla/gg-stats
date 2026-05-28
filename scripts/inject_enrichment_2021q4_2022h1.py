#!/usr/bin/env python3
"""Inject manually-derived user_items for Nov/Dec 2021 + Feb–May 2022 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── May 2022 ──────────────────────────────────────────────────────────────────
MAY_USER_ITEMS = [
    {"username": "hotzenrockz", "items": [
        {"title": "Doctor Strange in the Multiverse of Madness", "category": "film_series"},
        {"title": "Star Trek: Picard Staffel 2", "category": "film_series"},
        {"title": "Fargo Staffel 4", "category": "film_series"},
    ]},
    {"username": "Restrictor81", "items": [
        {"title": "Doctor Strange in the Multiverse of Madness", "category": "film_series"},
        {"title": "Stranger Things Staffel 4", "category": "film_series"},
        {"title": "Obi-Wan Kenobi", "category": "film_series"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Doctor Strange in the Multiverse of Madness", "category": "film_series"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Warhammer 40000: Chaos Gate - Daemonhunters", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "French Open", "category": "misc"},
        {"title": "Champions League Finale", "category": "misc"},
    ]},
    {"username": "Tr1nity", "items": [
        {"title": "Top Gun: Maverick", "category": "film_series"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Sniper Elite 5", "category": "game"},
        {"title": "Vampire: The Masquerade - Swansong", "category": "game"},
        {"title": "Stranger Things Staffel 4", "category": "film_series"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Obi-Wan Kenobi", "category": "film_series"},
        {"title": "Love, Death & Robots Staffel 3", "category": "film_series"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Star Trek: Strange New Worlds", "category": "film_series"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "Love, Death & Robots Staffel 3", "category": "film_series"},
        {"title": "Better Call Saul Staffel 6", "category": "film_series"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Neonschwarz Konzert", "category": "misc"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Obi-Wan Kenobi", "category": "film_series"},
    ]},
    {"username": "Humpsi", "items": [
        {"title": "Top Gun: Maverick", "category": "film_series"},
    ]},
    {"username": "Maverick", "items": [
        {"title": "Forgotten Fables: Wolves of the Westwind", "category": "game"},
        {"title": "Sniper Elite 5", "category": "game"},
    ]},
]

# ── Apr 2022 ──────────────────────────────────────────────────────────────────
APR_USER_ITEMS = [
    {"username": "Olphas", "items": [
        {"title": "Moon Knight", "category": "film_series"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "Better Call Saul Staffel 6", "category": "film_series"},
    ]},
    {"username": "TheLastToKnow", "items": [
        {"title": "Better Call Saul Staffel 6", "category": "film_series"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Ghostwire: Tokyo", "category": "game"},
        {"title": "Elden Ring", "category": "game"},
        {"title": "Better Call Saul Staffel 6", "category": "film_series"},
    ]},
    {"username": "Wuslon", "items": [
        {"title": "Moon Knight", "category": "film_series"},
    ]},
    {"username": "Slaytanic", "items": [
        {"title": "King Arthur: A Knight's Tale", "category": "game"},
        {"title": "Rammstein: Zeit", "category": "misc"},
    ]},
    {"username": "euph", "items": [
        {"title": "Vikings Valhalla", "category": "film_series"},
        {"title": "Bridgerton Staffel 2", "category": "film_series"},
        {"title": "The Batman", "category": "film_series"},
    ]},
    {"username": "Maverick", "items": [
        {"title": "Weird West", "category": "game"},
        {"title": "PanzerCorps 2", "category": "game"},
    ]},
    {"username": "Tr1nity", "items": [
        {"title": "Ozark Finale", "category": "film_series"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Chrono Cross: The Radical Dreamers Edition", "category": "game"},
    ]},
    {"username": "StefanH", "items": [
        {"title": "Chrono Cross: The Radical Dreamers Edition", "category": "game"},
    ]},
    {"username": "andima", "items": [
        {"title": "Ozark Finale", "category": "film_series"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "Chrono Cross: The Radical Dreamers Edition", "category": "game"},
        {"title": "Voice of Cards: The Isle Dragon Roars", "category": "game"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Better Call Saul Staffel 6", "category": "film_series"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Chrono Cross: The Radical Dreamers Edition", "category": "game"},
        {"title": "Lego Star Wars: Die Skywalker Saga", "category": "game"},
    ]},
    {"username": "hotzenrockz", "items": [
        {"title": "Ozark Finale", "category": "film_series"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Star Trek: Lower Decks Staffel 2", "category": "film_series"},
    ]},
]

# ── Mar 2022 ──────────────────────────────────────────────────────────────────
MAR_USER_ITEMS = [
    {"username": "AlexCartman", "items": [
        {"title": "Horizon Forbidden West", "category": "game"},
        {"title": "Triangle Strategy", "category": "game"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Rune Factory 5", "category": "game"},
        {"title": "Triangle Strategy", "category": "game"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "The Batman", "category": "film_series"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Wu-Tang: An American Saga Staffel 2", "category": "film_series"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Gran Turismo 7", "category": "game"},
        {"title": "Vigil", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "The Last Kingdom Staffel 5", "category": "film_series"},
        {"title": "Vikings Valhalla", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Gran Turismo 7", "category": "game"},
        {"title": "Kirby und das vergessene Land", "category": "game"},
        {"title": "The Batman", "category": "film_series"},
        {"title": "Severance", "category": "film_series"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Star Trek: Picard Staffel 2", "category": "film_series"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "Gran Turismo 7", "category": "game"},
        {"title": "Elden Ring", "category": "game"},
    ]},
    {"username": "Player One", "items": [
        {"title": "Horizon Forbidden West", "category": "game"},
        {"title": "Elex 2", "category": "game"},
        {"title": "Triangle Strategy", "category": "game"},
        {"title": "Gran Turismo 7", "category": "game"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "Shadow Warrior 3", "category": "game"},
        {"title": "Gran Turismo 7", "category": "game"},
        {"title": "Ghostwire: Tokyo", "category": "game"},
        {"title": "Tiny Tina's Wonderlands", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Ghostwire: Tokyo", "category": "game"},
        {"title": "Killing Eve Staffel 4", "category": "film_series"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Fargo Staffel 4", "category": "film_series"},
    ]},
    {"username": "TSH-Lightning", "items": [
        {"title": "WARNO", "category": "game"},
    ]},
    {"username": "Vampiro", "items": [
        {"title": "WARNO", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Ghostwire: Tokyo", "category": "game"},
        {"title": "Tiny Tina's Wonderlands", "category": "game"},
    ]},
    {"username": "st4tic -ZG-", "items": [
        {"title": "Gran Turismo 7", "category": "game"},
    ]},
]

# ── Feb 2022 ──────────────────────────────────────────────────────────────────
FEB_USER_ITEMS = [
    {"username": "unregistriert", "items": [
        {"title": "Book of Boba Fett", "category": "film_series"},
        {"title": "Vikings Valhalla", "category": "film_series"},
        {"title": "Jurassic World: Camp Cretaceous Staffel 5", "category": "film_series"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Crusader Kings III: Royal Court", "category": "game"},
        {"title": "Elden Ring", "category": "game"},
    ]},
    {"username": "The Real Maulwurfn", "items": [
        {"title": "Crusader Kings III: Royal Court", "category": "game"},
        {"title": "Elden Ring", "category": "game"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Elden Ring", "category": "game"},
        {"title": "Horizon Forbidden West", "category": "game"},
    ]},
    {"username": "Shake_s_beer", "items": [
        {"title": "The Cuphead Show!", "category": "film_series"},
        {"title": "Vikings Valhalla", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Vikings Valhalla", "category": "film_series"},
    ]},
    {"username": "LRod", "items": [
        {"title": "Total War: Warhammer 3", "category": "game"},
    ]},
    {"username": "Drapondur", "items": [
        {"title": "Horizon Forbidden West", "category": "game"},
    ]},
    {"username": "Hyperbolic", "items": [
        {"title": "Brooklyn Nine-Nine Staffel 8", "category": "film_series"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Horizon Forbidden West", "category": "game"},
        {"title": "Elden Ring", "category": "game"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Uncharted", "category": "film_series"},
        {"title": "Elite Dangerous", "category": "game"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "Elden Ring", "category": "game"},
    ]},
    {"username": "Wuslon", "items": [
        {"title": "Legend of Vox Machina", "category": "film_series"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "The Expanse Staffel 6", "category": "film_series"},
        {"title": "Book of Boba Fett", "category": "film_series"},
    ]},
    {"username": "TSH-Lightning", "items": [
        {"title": "Horizon Forbidden West", "category": "game"},
    ]},
    {"username": "Sciron", "items": [
        {"title": "Elden Ring", "category": "game"},
    ]},
    {"username": "1000dinge", "items": [
        {"title": "Elden Ring", "category": "game"},
        {"title": "Horizon Forbidden West", "category": "game"},
    ]},
    {"username": "Vampiro", "items": [
        {"title": "Steel Division 2: Tribute to the Liberation of Italy", "category": "game"},
        {"title": "Crusader Kings III: Royal Court", "category": "game"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "Horizon Forbidden West", "category": "game"},
    ]},
]

# ── Dec 2021 ──────────────────────────────────────────────────────────────────
DEC_USER_ITEMS = [
    {"username": "euph", "items": [
        {"title": "Ghostbusters: Legacy", "category": "film_series"},
    ]},
    {"username": "The Real Maulwurfn", "items": [
        {"title": "The Expanse Staffel 6", "category": "film_series"},
        {"title": "Book of Boba Fett", "category": "film_series"},
        {"title": "The Witcher Staffel 2", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Rad der Zeit", "category": "film_series"},
        {"title": "The Witcher Staffel 2", "category": "film_series"},
        {"title": "Hawkeye", "category": "film_series"},
        {"title": "Book of Boba Fett", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "The Witcher Staffel 2", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Halo Infinite", "category": "game"},
        {"title": "The Game Awards", "category": "misc"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Final Fantasy XIV: Endwalker", "category": "game"},
        {"title": "Spider-Man: No Way Home", "category": "film_series"},
    ]},
    {"username": "Trax", "items": [
        {"title": "Final Fantasy XIV: Endwalker", "category": "game"},
    ]},
    {"username": "Slevin", "items": [
        {"title": "Halo Infinite", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Guardians of the Galaxy", "category": "game"},
    ]},
    {"username": "timeagent", "items": [
        {"title": "Mass Effect Legendary Edition", "category": "game"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Hawkeye", "category": "film_series"},
        {"title": "Blade Runner: Black Lotus", "category": "film_series"},
    ]},
    {"username": "Wuslon", "items": [
        {"title": "Eternals", "category": "film_series"},
        {"title": "Spider-Man: No Way Home", "category": "film_series"},
        {"title": "Don't Look Up", "category": "film_series"},
        {"title": "Hawkeye", "category": "film_series"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Chorus", "category": "game"},
        {"title": "Syberia: The World Before", "category": "game"},
    ]},
    {"username": "Inso", "items": [
        {"title": "Cobra Kai Staffel 4", "category": "film_series"},
    ]},
    {"username": "e5150", "items": [
        {"title": "Riddle of Steel Festival", "category": "misc"},
    ]},
    {"username": "NguyenTranLoc", "items": [
        {"title": "Arcane", "category": "film_series"},
    ]},
    {"username": "Vidar", "items": [
        {"title": "Chorus", "category": "game"},
    ]},
]

# ── Nov 2021 ──────────────────────────────────────────────────────────────────
NOV_USER_ITEMS = [
    {"username": "Green Yoshi", "items": [
        {"title": "Ghostbusters: Legacy", "category": "film_series"},
        {"title": "Forza Horizon 5", "category": "game"},
    ]},
    {"username": "Berndor", "items": [
        {"title": "Horizon Forbidden West", "category": "game"},
        {"title": "Gran Turismo 7", "category": "game"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Forza Horizon 5", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "No Time to Die", "category": "film_series"},
        {"title": "Ghostbusters: Legacy", "category": "film_series"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Bright Memory: Infinite", "category": "game"},
    ]},
    {"username": "Maverick", "items": [
        {"title": "Forza Horizon 5", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Final Fantasy XIV: Endwalker", "category": "game"},
        {"title": "Shin Megami Tensei V", "category": "game"},
    ]},
    {"username": "Jonas S.", "items": [
        {"title": "Ghostbusters: Legacy", "category": "film_series"},
        {"title": "Rad der Zeit", "category": "film_series"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "Skyrim Anniversary Edition", "category": "game"},
        {"title": "GTA: The Trilogy", "category": "game"},
        {"title": "Sherlock Holmes: Chapter One", "category": "game"},
    ]},
    {"username": "Wunderheiler", "items": [
        {"title": "Animal Crossing: New Horizons 2.0", "category": "game"},
        {"title": "Forza Horizon 5", "category": "game"},
        {"title": "Shin Megami Tensei V", "category": "game"},
    ]},
    {"username": "The Real Maulwurfn", "items": [
        {"title": "The Expanse Staffel 6", "category": "film_series"},
        {"title": "Book of Boba Fett", "category": "film_series"},
        {"title": "The Witcher Staffel 2", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Rad der Zeit", "category": "film_series"},
        {"title": "The Witcher Staffel 2", "category": "film_series"},
        {"title": "Hawkeye", "category": "film_series"},
        {"title": "Book of Boba Fett", "category": "film_series"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Hawkeye", "category": "film_series"},
        {"title": "Blade Runner: Black Lotus", "category": "film_series"},
    ]},
    {"username": "Slevin", "items": [
        {"title": "Halo Infinite", "category": "game"},
    ]},
    {"username": "e5150", "items": [
        {"title": "Keep It True Rising Festival", "category": "misc"},
    ]},
    {"username": "Lefty", "items": [
        {"title": "Football Manager 2022", "category": "game"},
    ]},
    {"username": "Inso", "items": [
        {"title": "Cobra Kai Staffel 4", "category": "film_series"},
    ]},
]

MONTH_DATA = {
    "2022-05": MAY_USER_ITEMS,
    "2022-04": APR_USER_ITEMS,
    "2022-03": MAR_USER_ITEMS,
    "2022-02": FEB_USER_ITEMS,
    "2021-12": DEC_USER_ITEMS,
    "2021-11": NOV_USER_ITEMS,
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
