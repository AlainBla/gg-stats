#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "vorfreude.json"

MAR_2020 = [
    {"username": "Oranje", "items": [
        {"title": "Yes, Your Grace", "category": "game"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Ori and the Will of the Wisps", "category": "game"},
        {"title": "Onward", "category": "film_series"},
        {"title": "Altered Carbon Staffel 2", "category": "film_series"},
        {"title": "Babylon Berlin", "category": "film_series"},
        {"title": "The Deuce", "category": "film_series"},
        {"title": "The Outsider", "category": "film_series"},
        {"title": "His Dark Materials", "category": "film_series"},
    ]},
    {"username": "Sciron", "items": [
        {"title": "Ori and the Will of the Wisps", "category": "game"},
    ]},
    {"username": "Player One", "items": [
        {"title": "Ori and the Will of the Wisps", "category": "game"},
    ]},
    {"username": "MicBass", "items": [
        {"title": "Half-Life: Alyx", "category": "game"},
        {"title": "Better Call Saul", "category": "film_series"},
        {"title": "Altered Carbon Staffel 2", "category": "film_series"},
    ]},
    {"username": "Labrador Nelson", "items": [
        {"title": "Altered Carbon Staffel 2", "category": "film_series"},
        {"title": "Doom Eternal", "category": "game"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "Doom Eternal", "category": "game"},
        {"title": "Nioh 2", "category": "game"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Persona 5 Royal", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "Ori and the Will of the Wisps", "category": "game"},
        {"title": "Doom Eternal", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Vikings Staffel 6", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Ori and the Will of the Wisps", "category": "game"},
        {"title": "Die Känguru-Chroniken", "category": "film_series"},
        {"title": "The Mandalorian", "category": "film_series"},
    ]},
    {"username": "thhko", "items": [
        {"title": "Star Trek: Picard", "category": "film_series"},
        {"title": "Homeland", "category": "film_series"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "Better Call Saul", "category": "film_series"},
        {"title": "Kingdom Staffel 2", "category": "film_series"},
    ]},
    {"username": "rammmses", "items": [
        {"title": "Altered Carbon Staffel 2", "category": "film_series"},
        {"title": "Parasite", "category": "film_series"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Doom Eternal", "category": "game"},
        {"title": "Ip Man 4", "category": "film_series"},
        {"title": "Bloodshot", "category": "film_series"},
        {"title": "Mulan", "category": "film_series"},
    ]},
    {"username": "Talakos", "items": [
        {"title": "Star Trek: Picard", "category": "film_series"},
        {"title": "Doom Eternal", "category": "game"},
        {"title": "Half-Life: Alyx", "category": "game"},
    ]},
    {"username": "Aladan", "items": [
        {"title": "A Quiet Place 2", "category": "film_series"},
        {"title": "Mulan", "category": "film_series"},
        {"title": "Castlevania", "category": "film_series"},
    ]},
    {"username": "Sokar", "items": [
        {"title": "Doom Eternal", "category": "game"},
    ]},
    {"username": "Mr.Schmerz", "items": [
        {"title": "Animal Crossing: New Horizons", "category": "game"},
        {"title": "Doom Eternal", "category": "game"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "The Mandalorian", "category": "film_series"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Altered Carbon Staffel 2", "category": "film_series"},
        {"title": "Doom Eternal", "category": "game"},
    ]},
]

APR_2020 = [
    {"username": "Alain", "items": [
        {"title": "Red Dead Redemption 2", "category": "game"},
        {"title": "Disco Elysium", "category": "game"},
        {"title": "Watchmen", "category": "film_series"},
        {"title": "The Crown", "category": "film_series"},
        {"title": "Haus des Geldes Staffel 4", "category": "film_series"},
    ]},
    {"username": "Red Dox", "items": [
        {"title": "Harley Quinn Staffel 2", "category": "film_series"},
    ]},
    {"username": "Hannes Herrmann", "items": [
        {"title": "Persona 5 Royal", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Final Fantasy VII Remake", "category": "game"},
        {"title": "The Mandalorian", "category": "film_series"},
    ]},
    {"username": "Player One", "items": [
        {"title": "Final Fantasy VII Remake", "category": "game"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "The Mandalorian", "category": "film_series"},
        {"title": "Better Call Saul", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Haus des Geldes Staffel 2", "category": "film_series"},
        {"title": "The Mandalorian", "category": "film_series"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Westworld Staffel 3", "category": "film_series"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Animal Crossing: New Horizons", "category": "game"},
    ]},
    {"username": "Aladan", "items": [
        {"title": "Final Fantasy VII Remake", "category": "game"},
        {"title": "Trials of Mana", "category": "game"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Animal Crossing: New Horizons", "category": "game"},
        {"title": "Yakuza 3 Remastered", "category": "game"},
        {"title": "Persona 5 Royal", "category": "game"},
    ]},
    {"username": "Ahlon", "items": [
        {"title": "Final Fantasy VII Remake", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Dreams", "category": "game"},
    ]},
]

MAY_2020 = [
    {"username": "Green Yoshi", "items": [
        {"title": "Xenoblade Chronicles", "category": "game"},
        {"title": "Unorthodox", "category": "film_series"},
    ]},
    {"username": "Maverick", "items": [
        {"title": "Someday You'll Return", "category": "game"},
        {"title": "VirtuaVerse", "category": "game"},
        {"title": "The Expanse Staffel 4", "category": "film_series"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "Gears Tactics", "category": "game"},
        {"title": "The Mandalorian", "category": "film_series"},
        {"title": "Bosch", "category": "film_series"},
    ]},
    {"username": "euph", "items": [
        {"title": "Anne with an E", "category": "film_series"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Xenoblade Chronicles", "category": "game"},
    ]},
    {"username": "SupArai", "items": [
        {"title": "The Handmaid's Tale", "category": "film_series"},
        {"title": "The Boys", "category": "film_series"},
    ]},
    {"username": "Jonas S.", "items": [
        {"title": "Snowpiercer", "category": "film_series"},
    ]},
    {"username": "Red Dox", "items": [
        {"title": "Rick & Morty Staffel 4", "category": "film_series"},
        {"title": "Harley Quinn Staffel 2", "category": "film_series"},
    ]},
]

JUN_2020 = [
    {"username": "Danywilde", "items": [
        {"title": "The Last of Us 2", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "Desperados 3", "category": "game"},
        {"title": "The Last of Us 2", "category": "game"},
        {"title": "Anne with an E", "category": "film_series"},
        {"title": "The Last Dance", "category": "film_series"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Desperados 3", "category": "game"},
        {"title": "Dark Staffel 3", "category": "film_series"},
    ]},
    {"username": "John of Gaunt", "items": [
        {"title": "Desperados 3", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "The Last of Us 2", "category": "game"},
        {"title": "Desperados 3", "category": "game"},
    ]},
    {"username": "Sciron", "items": [
        {"title": "Dark Staffel 3", "category": "film_series"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Space Force", "category": "film_series"},
        {"title": "Dark Staffel 3", "category": "film_series"},
    ]},
    {"username": "Graubirne76", "items": [
        {"title": "The Last of Us 2", "category": "game"},
    ]},
    {"username": "Necromanus", "items": [
        {"title": "The Last of Us 2", "category": "game"},
    ]},
    {"username": "Player One", "items": [
        {"title": "The Last of Us 2", "category": "game"},
    ]},
    {"username": "Sh4p3r", "items": [
        {"title": "The Last of Us 2", "category": "game"},
    ]},
    {"username": "Baumkuchen", "items": [
        {"title": "Yakuza Kiwami 2", "category": "game"},
    ]},
]

JUL_2020 = [
    {"username": "Wunderheiler", "items": [
        {"title": "Animal Crossing: New Horizons", "category": "game"},
        {"title": "Catherine: Full Body", "category": "game"},
        {"title": "Paper Mario: The Origami King", "category": "game"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Star Wars: The Clone Wars", "category": "film_series"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Ghost of Tsushima", "category": "game"},
        {"title": "Marvel's Iron Man VR", "category": "game"},
        {"title": "Beyond a Steel Sky", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Beyond a Steel Sky", "category": "game"},
    ]},
    {"username": "Specter", "items": [
        {"title": "Paper Mario: The Origami King", "category": "game"},
        {"title": "Deadly Premonition 2", "category": "game"},
    ]},
    {"username": "Player One", "items": [
        {"title": "Ghost of Tsushima", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Parasite", "category": "film_series"},
    ]},
    {"username": "TheRaffer", "items": [
        {"title": "Titan Quest", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "Desperados 3", "category": "game"},
        {"title": "The Last of Us 2", "category": "game"},
        {"title": "Stranger Things Staffel 3", "category": "film_series"},
    ]},
    {"username": "Marulez", "items": [
        {"title": "Grounded", "category": "game"},
        {"title": "CastleStorm 2", "category": "game"},
    ]},
    {"username": "Zup", "items": [
        {"title": "The Last of Us 2", "category": "game"},
    ]},
    {"username": "Admiral Anger", "items": [
        {"title": "Superliminal", "category": "game"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Dark Staffel 3", "category": "film_series"},
    ]},
    {"username": "Aladan", "items": [
        {"title": "Ghost of Tsushima", "category": "game"},
        {"title": "Fairy Tail", "category": "film_series"},
    ]},
    {"username": "AlexCartman", "items": [
        {"title": "Ghost of Tsushima", "category": "game"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Ghost of Tsushima", "category": "game"},
        {"title": "Der Fall Richard Jewell", "category": "film_series"},
    ]},
    {"username": "Wuslon", "items": [
        {"title": "Umbrella Academy Staffel 2", "category": "film_series"},
    ]},
    {"username": "Bruno Lawrie", "items": [
        {"title": "Ghost of Tsushima", "category": "game"},
        {"title": "Deadly Premonition 2", "category": "game"},
    ]},
]

AUG_2020 = [
    {"username": "The Real Maulwurfn", "items": [
        {"title": "Wasteland 3", "category": "game"},
    ]},
    {"username": "Pro4you", "items": [
        {"title": "Horizon Zero Dawn", "category": "game"},
        {"title": "Divinity: Original Sin 2", "category": "game"},
    ]},
    {"username": "Slaytanic", "items": [
        {"title": "Wasteland 3", "category": "game"},
    ]},
    {"username": "CaptainKidd", "items": [
        {"title": "Wasteland 3", "category": "game"},
        {"title": "Horizon Zero Dawn", "category": "game"},
        {"title": "Total War Saga: Troy", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "The Last of Us 2", "category": "game"},
    ]},
    {"username": "Player One", "items": [
        {"title": "Wasteland 3", "category": "game"},
        {"title": "Microsoft Flight Simulator", "category": "game"},
    ]},
    {"username": "Red Dox", "items": [
        {"title": "Star Trek: Lower Decks", "category": "film_series"},
        {"title": "Doom Patrol Staffel 2", "category": "film_series"},
        {"title": "Horizon Zero Dawn", "category": "game"},
    ]},
    {"username": "Maestro84", "items": [
        {"title": "Horizon Zero Dawn", "category": "game"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "Lucifer", "category": "film_series"},
        {"title": "Total War Saga: Troy", "category": "game"},
        {"title": "Tell Me Why", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Tell Me Why", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Tell Me Why", "category": "game"},
        {"title": "Beyond a Steel Sky", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Tenet", "category": "film_series"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Tell Me Why", "category": "game"},
    ]},
    {"username": "1000dinge", "items": [
        {"title": "Umbrella Academy Staffel 2", "category": "film_series"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "Umbrella Academy Staffel 2", "category": "film_series"},
    ]},
    {"username": "iYork", "items": [
        {"title": "The Last of Us 2", "category": "game"},
    ]},
    {"username": "Mersar", "items": [
        {"title": "Microsoft Flight Simulator", "category": "game"},
    ]},
    {"username": "Vampiro", "items": [
        {"title": "Hearts of Iron IV", "category": "game"},
        {"title": "FIFA 20", "category": "game"},
        {"title": "Battle Brothers", "category": "game"},
        {"title": "Microsoft Flight Simulator", "category": "game"},
    ]},
]

SEP_2020 = [
    {"username": "Marulez", "items": [
        {"title": "Tony Hawk's Pro Skater 1+2", "category": "game"},
        {"title": "Crysis Remastered", "category": "game"},
    ]},
    {"username": "Crizzo", "items": [
        {"title": "Iron Harvest", "category": "game"},
        {"title": "Mafia: Definitive Edition", "category": "game"},
    ]},
    {"username": "Ganon", "items": [
        {"title": "Tony Hawk's Pro Skater 1+2", "category": "game"},
        {"title": "Crysis Remastered", "category": "game"},
        {"title": "Cobra Kai Staffel 2", "category": "film_series"},
        {"title": "Das letzte Wort", "category": "film_series"},
    ]},
    {"username": "Green Yoshi", "items": [
        {"title": "Tony Hawk's Pro Skater 1+2", "category": "game"},
        {"title": "Tell Me Why", "category": "game"},
        {"title": "Mafia: Definitive Edition", "category": "game"},
    ]},
    {"username": "Sciron", "items": [
        {"title": "The Americans", "category": "film_series"},
        {"title": "Spelunky 2", "category": "game"},
        {"title": "Tony Hawk's Pro Skater 1+2", "category": "game"},
    ]},
    {"username": "unregistriert", "items": [
        {"title": "The Boys Staffel 2", "category": "film_series"},
    ]},
    {"username": "Noodles", "items": [
        {"title": "Mafia: Definitive Edition", "category": "game"},
        {"title": "The Boys Staffel 2", "category": "film_series"},
    ]},
    {"username": "Tasmanius", "items": [
        {"title": "Crysis Remastered", "category": "game"},
        {"title": "Mafia: Definitive Edition", "category": "game"},
    ]},
    {"username": "funrox", "items": [
        {"title": "Missing Lisa", "category": "film_series"},
        {"title": "Der junge Wallander", "category": "film_series"},
        {"title": "Beyond a Steel Sky", "category": "game"},
    ]},
    {"username": "euph", "items": [
        {"title": "Tony Hawk's Pro Skater 1+2", "category": "game"},
        {"title": "The Legend of Zelda: Link's Awakening", "category": "game"},
    ]},
    {"username": "Funatic", "items": [
        {"title": "I'm Thinking of Ending Things", "category": "film_series"},
        {"title": "Wasteland 3", "category": "game"},
        {"title": "Tenet", "category": "film_series"},
    ]},
    {"username": "Red Dox", "items": [
        {"title": "Iron Harvest", "category": "game"},
        {"title": "Archer Season 11", "category": "film_series"},
        {"title": "The Boys Staffel 2", "category": "film_series"},
        {"title": "Lovecraft Country", "category": "film_series"},
    ]},
    {"username": "Admiral Anger", "items": [
        {"title": "Tony Hawk's Pro Skater 1+2", "category": "game"},
        {"title": "Mafia: Definitive Edition", "category": "game"},
    ]},
    {"username": "Jonas S.", "items": [
        {"title": "Iron Harvest", "category": "game"},
        {"title": "Crusader Kings III", "category": "game"},
        {"title": "Wasteland 3", "category": "game"},
        {"title": "The Boys Staffel 2", "category": "film_series"},
        {"title": "Deutschland 89", "category": "film_series"},
    ]},
    {"username": "Olphas", "items": [
        {"title": "The Boys Staffel 2", "category": "film_series"},
        {"title": "Crusader Kings III", "category": "game"},
    ]},
    {"username": "Player One", "items": [
        {"title": "Iron Harvest", "category": "game"},
    ]},
    {"username": "Alain", "items": [
        {"title": "Suicide of Rachel Foster", "category": "game"},
        {"title": "Tell Me Why", "category": "game"},
        {"title": "Wasteland 3", "category": "game"},
    ]},
    {"username": "Necromanus", "items": [
        {"title": "Final Fantasy VII Remake", "category": "game"},
    ]},
    {"username": "rammmses", "items": [
        {"title": "Mafia: Definitive Edition", "category": "game"},
        {"title": "Wasteland 3", "category": "game"},
    ]},
    {"username": "Lencer", "items": [
        {"title": "Wasteland 3", "category": "game"},
        {"title": "Port Royale 4", "category": "game"},
        {"title": "Pathfinder: Kingmaker", "category": "game"},
    ]},
    {"username": "PraetorCreech", "items": [
        {"title": "Star Trek: Lower Decks", "category": "film_series"},
    ]},
    {"username": "Robokopp", "items": [
        {"title": "The Boys Staffel 2", "category": "film_series"},
        {"title": "Mass Effect Trilogy", "category": "game"},
    ]},
    {"username": "Desotho", "items": [
        {"title": "Mafia: Definitive Edition", "category": "game"},
        {"title": "Trails of Cold Steel IV", "category": "game"},
    ]},
    {"username": "Prinz Ipp", "items": [
        {"title": "Trails of Cold Steel IV", "category": "game"},
        {"title": "13 Sentinels: Aegis Rim", "category": "game"},
    ]},
]

MONTH_DATA = {
    "2020-03": MAR_2020,
    "2020-04": APR_2020,
    "2020-05": MAY_2020,
    "2020-06": JUN_2020,
    "2020-07": JUL_2020,
    "2020-08": AUG_2020,
    "2020-09": SEP_2020,
}


def compute_stats(editors, user_items):
    stats = {}
    for editor in editors:
        key = "editor:" + re.sub(r"\s+", "_", editor["name"].lower())
        for item in editor.get("items", []):
            title = item["title"]
            if title not in stats:
                stats[title] = {"count": 0, "category": item.get("category", "unknown"), "mentioners": []}
            if key not in stats[title]["mentioners"]:
                stats[title]["count"] += 1
                stats[title]["mentioners"].append(key)
    for user in user_items:
        key = "user:" + user["username"]
        for item in user.get("items", []):
            title = item["title"]
            if title not in stats:
                stats[title] = {"count": 0, "category": item.get("category", "unknown"), "mentioners": []}
            if key not in stats[title]["mentioners"]:
                stats[title]["count"] += 1
                stats[title]["mentioners"].append(key)
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
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Updated {len(MONTH_DATA)} months: {', '.join(sorted(MONTH_DATA.keys()))}")


if __name__ == "__main__":
    main()
