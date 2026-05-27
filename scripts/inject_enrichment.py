#!/usr/bin/env python3
"""Inject manually-derived user_items for Feb/Mar/Apr 2026 into vorfreude.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/vorfreude.json")

# ── Feb 2026 ────────────────────────────────────────────────────────────────
FEB_USER_ITEMS = [
    {"username": "Crizzo", "items": [
        {"title": "Lincoln Lawyer", "category": "film_series"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Nier Automata", "category": "game"},
        {"title": "Resident Evil Requiem", "category": "game"},
        {"title": "Romeo is a Dead Man", "category": "game"},
        {"title": "No Other Choice", "category": "film_series"},
        {"title": "Stranger Things S5", "category": "film_series"},
        {"title": "Fallout S2", "category": "film_series"},
        {"title": "Dexter: Resurrection", "category": "film_series"},
        {"title": "Welcome to Derry", "category": "film_series"},
        {"title": "A Knight of Seven Kingdoms", "category": "film_series"},
        {"title": "The Pitt", "category": "film_series"},
        {"title": "Heated Rivalry", "category": "film_series"},
        {"title": "Marty Supreme", "category": "film_series"},
    ]},
    {"username": "Flooraimer", "items": [
        {"title": "Romeo is a Dead Man", "category": "game"},
        {"title": "Styx: Blades of Greed", "category": "game"},
        {"title": "Fallout S2", "category": "film_series"},
        {"title": "Hallow Road", "category": "film_series"},
        {"title": "Good Fortune", "category": "film_series"},
        {"title": "Marty Supreme", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Indiana Jones und der große Kreis", "category": "game"},
        {"title": "Slay the Spire", "category": "game"},
        {"title": "Hades 2", "category": "game"},
        {"title": "Resident Evil 9", "category": "game"},
        {"title": "Stranger Things", "category": "film_series"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Fallout S2", "category": "film_series"},
    ]},
    {"username": "Jonas S.", "items": [
        {"title": "Indiana Jones und der große Kreis", "category": "game"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Voxel-Mods für Doom und Duke Nukem 3D", "category": "game"},
        {"title": "Resident Evil Requiem", "category": "game"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Aces of Thunder", "category": "game"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Shrinking S3", "category": "film_series"},
    ]},
    {"username": "JensJuchzer", "items": [
        {"title": "Scream 7", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Dragon Quest VII", "category": "game"},
        {"title": "Resident Evil Requiem", "category": "game"},
        {"title": "Baphomets Fluch - Die Spiegel der Finsternis: Reforged", "category": "game"},
        {"title": "GEE Magazin", "category": "misc"},
        {"title": "Retro Gamer", "category": "misc"},
        {"title": "Winter Olympics 2026", "category": "misc"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "Watch Dogs", "category": "game"},
        {"title": "Transformers", "category": "film_series"},
        {"title": "Jack Reacher 2", "category": "film_series"},
        {"title": "Rivers of London", "category": "misc"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Scream 7", "category": "film_series"},
        {"title": "Tulsa King S3", "category": "film_series"},
        {"title": "The Witcher", "category": "film_series"},
        {"title": "Hollow Knight", "category": "game"},
        {"title": "Mafia", "category": "game"},
        {"title": "Donkey Kong Bananza", "category": "game"},
        {"title": "Clair-Obscur Soundtrack", "category": "misc"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Shrinking S3", "category": "film_series"},
        {"title": "Fallout S2", "category": "film_series"},
        {"title": "No Other Choice", "category": "film_series"},
        {"title": "Cylia Journey", "category": "game"},
        {"title": "Lost Judgment", "category": "game"},
        {"title": "Yakuza Kiwami 3", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Nioh 3", "category": "game"},
        {"title": "Yakuza Kiwami 3", "category": "game"},
        {"title": "No Other Choice", "category": "film_series"},
    ]},
    {"username": "Berndor", "items": [
        {"title": "Stalker 2", "category": "game"},
        {"title": "Trails in the Sky 1st Chapter", "category": "game"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "Fallout S2", "category": "film_series"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Shadow Warrior 3", "category": "game"},
        {"title": "Evil West", "category": "game"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Scream 7", "category": "film_series"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Return to Silent Hill", "category": "film_series"},
        {"title": "Send Help", "category": "film_series"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Rings of Power S2", "category": "film_series"},
        {"title": "Fallout S2", "category": "film_series"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Dragon Quest VII", "category": "game"},
        {"title": "Nioh 3", "category": "game"},
        {"title": "EU5 Patch 1.1", "category": "game"},
        {"title": "Enshrouded", "category": "game"},
        {"title": "Fallout S2", "category": "film_series"},
        {"title": "Return to Silent Hill", "category": "film_series"},
    ]},
    {"username": "B1ixX0r", "items": [
        {"title": "Dawnless", "category": "game"},
    ]},
    {"username": "Sciron", "items": [
        {"title": "Warhammer 40.000: Space Marine 2", "category": "game"},
        {"title": "Call of Duty Black Ops 7 Season 2", "category": "game"},
        {"title": "Stargate SG-1", "category": "film_series"},
        {"title": "Stories of Your Life and Others", "category": "misc"},
    ]},
]

# ── Mar 2026 ────────────────────────────────────────────────────────────────
MAR_USER_ITEMS = [
    {"username": "Crizzo", "items": [
        {"title": "F1 25", "category": "game"},
        {"title": "Landwirtschafts-Simulator 25", "category": "game"},
        {"title": "Der Astronaut", "category": "film_series"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Islets", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Resident Evil Requiem", "category": "game"},
        {"title": "Gelbe Briefe", "category": "film_series"},
        {"title": "Marty Supreme", "category": "film_series"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Monster", "category": "film_series"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "World of Warcraft Midnight", "category": "game"},
    ]},
    {"username": "Shake_s_beer", "items": [
        {"title": "Crimson Desert", "category": "game"},
        {"title": "Greedfall 2", "category": "game"},
        {"title": "The Outer Worlds 2", "category": "game"},
        {"title": "Fallout S2", "category": "film_series"},
    ]},
    {"username": "Flooraimer", "items": [
        {"title": "Scrubs Reboot", "category": "film_series"},
        {"title": "Esoteric Ebb", "category": "game"},
        {"title": "Slay the Spire 2", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Hollow Knight: Silksong", "category": "game"},
    ]},
    {"username": "Keppel", "items": [
        {"title": "Scrubs Reboot", "category": "film_series"},
        {"title": "Daredevil: Born Again S2", "category": "film_series"},
        {"title": "World of Warcraft Midnight", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Resident Evil Requiem", "category": "game"},
        {"title": "Death Stranding 2", "category": "game"},
        {"title": "Crimson Desert", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Shrinking", "category": "film_series"},
        {"title": "Slow Horses", "category": "film_series"},
        {"title": "Scrubs Reboot", "category": "film_series"},
        {"title": "Crimson Desert", "category": "game"},
        {"title": "Death Stranding 2", "category": "game"},
    ]},
    {"username": "mrkhfloppy", "items": [
        {"title": "Replaced", "category": "game"},
        {"title": "Daredevil: Born Again S2", "category": "film_series"},
    ]},
    {"username": "Calmon", "items": [
        {"title": "Slay the Spire 2", "category": "game"},
        {"title": "The Bazaar", "category": "game"},
    ]},
    {"username": "Thomas Schmitz", "items": [
        {"title": "The Pitt S2", "category": "film_series"},
        {"title": "Succession", "category": "film_series"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Fallout S2", "category": "film_series"},
        {"title": "Resident Evil Requiem", "category": "game"},
        {"title": "Kathy Rain", "category": "game"},
        {"title": "Death Stranding 2", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Der Astronaut", "category": "film_series"},
        {"title": "Stargate SG-1", "category": "film_series"},
        {"title": "Scrubs Reboot", "category": "film_series"},
    ]},
    {"username": "Juuunior", "items": [
        {"title": "Billions", "category": "film_series"},
    ]},
    {"username": "Wuslon", "items": [
        {"title": "Dungeon Crawler Carl", "category": "misc"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Dungeon Crawler Carl Buch 8", "category": "misc"},
        {"title": "Operation Bounce House", "category": "misc"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Project Hail Mary", "category": "film_series"},
        {"title": "Good Luck Have Fun Don't Die", "category": "film_series"},
        {"title": "Strange New Worlds S3", "category": "film_series"},
        {"title": "Dexter: Resurrection", "category": "film_series"},
        {"title": "The Substance", "category": "film_series"},
        {"title": "Kraftklub Konzert", "category": "misc"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Fallout S2", "category": "film_series"},
        {"title": "Divide & Conquer Mod für Medieval 2 Total War", "category": "game"},
    ]},
    {"username": "sneaker23", "items": [
        {"title": "Night Agent S3", "category": "film_series"},
        {"title": "Karnivool Konzert", "category": "misc"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "The Expanse", "category": "film_series"},
        {"title": "Persona 3 FES", "category": "game"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "A Knight of the Seven Kingdoms", "category": "film_series"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Crimson Desert", "category": "game"},
        {"title": "Sumerian Six", "category": "game"},
    ]},
]

# ── Apr 2026 ────────────────────────────────────────────────────────────────
APR_USER_ITEMS = [
    {"username": "Bruno Lawrie", "items": [
        {"title": "Crimson Desert", "category": "game"},
        {"title": "Resident Evil Requiem", "category": "game"},
        {"title": "Death Stranding 2", "category": "game"},
        {"title": "Stromberg Kinofilm", "category": "film_series"},
        {"title": "Der Astronaut", "category": "film_series"},
    ]},
    {"username": "Alain", "items": [
        {"title": "For All Mankind", "category": "film_series"},
        {"title": "Shrinking", "category": "film_series"},
        {"title": "GameNative", "category": "game"},
    ]},
    {"username": "Q-Bert", "items": [
        {"title": "Xenonauts 2", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Saros", "category": "game"},
        {"title": "Pragmata", "category": "game"},
        {"title": "Samson", "category": "game"},
        {"title": "Beef S2", "category": "film_series"},
        {"title": "From S4", "category": "film_series"},
        {"title": "Project Hail Mary", "category": "film_series"},
        {"title": "Ready or Not - Here I Come", "category": "film_series"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "Slay the Spire 2", "category": "game"},
        {"title": "Super Mario Galaxy Film", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Commandos Origins DLC", "category": "game"},
        {"title": "Der Astronaut", "category": "film_series"},
        {"title": "Crooks S2", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Pragmata", "category": "game"},
    ]},
    {"username": "Flooraimer", "items": [
        {"title": "Xenonauts 2", "category": "game"},
        {"title": "Samson", "category": "game"},
        {"title": "Saros", "category": "game"},
        {"title": "Scrubs Reboot", "category": "film_series"},
        {"title": "Malcolm in the Middle: Life's Still Unfair", "category": "film_series"},
        {"title": "Lee Cronin's The Mummy", "category": "film_series"},
        {"title": "Michael Jackson Biopic", "category": "film_series"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Super Mario Galaxy Film", "category": "film_series"},
        {"title": "Project Hail Mary", "category": "film_series"},
        {"title": "Kill Bill: The Whole Bloody Affair", "category": "film_series"},
        {"title": "Malcolm in the Middle: Life's Still Unfair", "category": "film_series"},
        {"title": "Daredevil: Born Again S2", "category": "film_series"},
        {"title": "Saros", "category": "game"},
    ]},
    {"username": "Berndor", "items": [
        {"title": "Saros", "category": "game"},
        {"title": "Crimson Desert", "category": "game"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Scrubs Reboot", "category": "film_series"},
        {"title": "Stargate SG-1", "category": "film_series"},
    ]},
    {"username": "Enrico Pallazzo", "items": [
        {"title": "A Knight of the Seven Kingdoms", "category": "film_series"},
        {"title": "Watchmen", "category": "film_series"},
        {"title": "Westworld", "category": "film_series"},
        {"title": "Kingdom Come Deliverance 2", "category": "game"},
    ]},
    {"username": "duchess", "items": [
        {"title": "Death Stranding 2", "category": "game"},
        {"title": "Kingdom Come Deliverance 1", "category": "game"},
    ]},
    {"username": "Moe90", "items": [
        {"title": "Pragmata", "category": "game"},
        {"title": "Saros", "category": "game"},
        {"title": "The Pitt S2", "category": "film_series"},
        {"title": "Der Astronaut", "category": "film_series"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Crimson Desert", "category": "game"},
        {"title": "Screamer", "category": "game"},
        {"title": "Slay the Spire 2", "category": "game"},
        {"title": "Mewgenics", "category": "game"},
        {"title": "Saros", "category": "game"},
        {"title": "Red Cliff", "category": "film_series"},
        {"title": "Project Hail Mary", "category": "film_series"},
        {"title": "Super Mario Galaxy Film", "category": "film_series"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "Fallout S2", "category": "film_series"},
        {"title": "Scrubs Reboot", "category": "film_series"},
        {"title": "Super Meat Boy 3D", "category": "game"},
        {"title": "Hades 2", "category": "game"},
        {"title": "Pragmata", "category": "game"},
    ]},
    {"username": "DerBesserwisser", "items": [
        {"title": "Scrubs Reboot", "category": "film_series"},
    ]},
    {"username": "Henmann", "items": [
        {"title": "Project Hail Mary", "category": "film_series"},
        {"title": "Scrubs Reboot", "category": "film_series"},
        {"title": "Malcolm in the Middle: Life's Still Unfair", "category": "film_series"},
    ]},
    {"username": "Danywilde", "items": [
        {"title": "Baudolino", "category": "misc"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Super Mario Galaxy Film", "category": "film_series"},
        {"title": "Der Astronaut", "category": "film_series"},
    ]},
    {"username": "sneaker23", "items": [
        {"title": "Karnivool Konzert", "category": "misc"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "Persona 3 FES", "category": "game"},
        {"title": "Rivers of London", "category": "misc"},
    ]},
    {"username": "Gucky", "items": [
        {"title": "Star Wars: Maul - Shadow Lord", "category": "film_series"},
        {"title": "Spider-Noir", "category": "film_series"},
        {"title": "Super Mario Galaxy Film", "category": "film_series"},
        {"title": "How to Make a Killing", "category": "film_series"},
    ]},
    {"username": "Thomas Schmitz", "items": [
        {"title": "Kingdom Come Deliverance 2", "category": "game"},
        {"title": "Super Mario Galaxy Film", "category": "film_series"},
        {"title": "Kill Bill: The Whole Bloody Affair", "category": "film_series"},
    ]},
    {"username": "KampfPlauze", "items": [
        {"title": "Super Mario Galaxy Film", "category": "film_series"},
        {"title": "Scrubs Reboot", "category": "film_series"},
        {"title": "Malcolm in the Middle: Life's Still Unfair", "category": "film_series"},
    ]},
    {"username": "Klexter", "items": [
        {"title": "The Pitt S2", "category": "film_series"},
    ]},
    {"username": "Maverick", "items": [
        {"title": "Replaced", "category": "game"},
    ]},
]

MONTH_DATA = {
    "2026-02": FEB_USER_ITEMS,
    "2026-03": MAR_USER_ITEMS,
    "2026-04": APR_USER_ITEMS,
}


def compute_stats(editors, user_items):
    stats = {}
    for editor in editors:
        key = "editor:" + re.sub(r"\s+", "_", editor["name"].lower())
        for item in editor["items"]:
            title = item["title"]
            if title not in stats:
                stats[title] = {"count": 0, "category": item["category"], "mentioners": []}
            if key not in stats[title]["mentioners"]:
                stats[title]["mentioners"].append(key)
                stats[title]["count"] += 1
    for user in user_items:
        key = "user:" + user["username"]
        for item in user["items"]:
            title = item["title"]
            if title not in stats:
                stats[title] = {"count": 0, "category": item["category"], "mentioners": []}
            if key not in stats[title]["mentioners"]:
                stats[title]["mentioners"].append(key)
                stats[title]["count"] += 1
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
