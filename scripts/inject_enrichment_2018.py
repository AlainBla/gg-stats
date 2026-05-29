#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "vorfreude.json"

JAN2018_USER_ITEMS = [
    {"username": "unregistriert", "items": [{"title": "NFL Playoffs", "category": "misc"}, {"title": "Final Fantasy XIV", "category": "game"}]},
    {"username": "euph", "items": [{"title": "Stranger Things", "category": "film_series"}, {"title": "Star Trek: Discovery", "category": "film_series"}]},
    {"username": "TSH-Lightning", "items": [{"title": "Die dunkelste Stunde", "category": "film_series"}]},
    {"username": "Maestro84", "items": [{"title": "Assassin's Creed: Origins", "category": "game"}]},
    {"username": "Drapondur", "items": [{"title": "Star Wars: Die letzten Jedi", "category": "film_series"}]},
    {"username": "Jac", "items": [{"title": "Pastewka Staffel 8", "category": "film_series"}]},
    {"username": "Mike H.", "items": [{"title": "Pastewka Staffel 8", "category": "film_series"}]},
    {"username": "Vampiro", "items": [{"title": "Elementary Staffel 4", "category": "film_series"}]},
    {"username": "Sciron", "items": [{"title": "Cuphead", "category": "game"}, {"title": "Wrestle Kingdom 12", "category": "misc"}]},
    {"username": "Green Yoshi", "items": [{"title": "Die dunkelste Stunde", "category": "film_series"}, {"title": "Life is Strange: Before the Storm", "category": "game"}, {"title": "Assassin's Creed: Origins", "category": "game"}]},
    {"username": "Revolver_Ocelot", "items": [{"title": "Dragon Ball FighterZ", "category": "game"}, {"title": "Kingdom Come: Deliverance", "category": "game"}, {"title": "Yakuza 6", "category": "game"}]},
    {"username": "Maverick", "items": [{"title": "Wolfenstein 2: The New Colossus", "category": "game"}, {"title": "Elex", "category": "game"}]},
    {"username": "Funatic", "items": [{"title": "Super Mario Odyssey", "category": "game"}, {"title": "Black Sails", "category": "film_series"}]},
    {"username": "SaRaHk", "items": [{"title": "Pokémon Kristall-Edition", "category": "game"}]},
    {"username": "T-Bone", "items": [{"title": "The Witcher 3", "category": "game"}]},
    {"username": "Bruno Lawrie", "items": [{"title": "Kingdom Come: Deliverance", "category": "game"}, {"title": "Ni No Kuni 2", "category": "game"}, {"title": "Shadow of the Colossus Remake", "category": "game"}, {"title": "Far Cry 5", "category": "game"}]},
]

FEB2018_USER_ITEMS = [
    {"username": "Jonas S.", "items": [{"title": "Kingdom Come: Deliverance", "category": "game"}]},
    {"username": "ChrisIkari", "items": [{"title": "Final Fantasy XII PC", "category": "game"}, {"title": "Secret of Mana Remake", "category": "game"}]},
    {"username": "Aladan", "items": [{"title": "Black Panther", "category": "film_series"}, {"title": "Altered Carbon", "category": "film_series"}, {"title": "Kingdom Come: Deliverance", "category": "game"}]},
    {"username": "unregistriert", "items": [{"title": "Altered Carbon", "category": "film_series"}]},
    {"username": "kurosawa", "items": [{"title": "Mute", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "Mute", "category": "film_series"}, {"title": "Shadow of the Colossus Remake", "category": "game"}]},
    {"username": "euph", "items": [{"title": "Star Trek: Discovery Staffel 1", "category": "film_series"}, {"title": "Kingdom Come: Deliverance", "category": "game"}]},
    {"username": "Grohal", "items": [{"title": "Stellaris DLC", "category": "game"}]},
    {"username": "Welat", "items": [{"title": "Star Trek: Discovery", "category": "film_series"}, {"title": "Stellaris: Apocalypse", "category": "game"}]},
    {"username": "Slaytanic", "items": [{"title": "Kingdom Come: Deliverance", "category": "game"}, {"title": "Civ 6: Rise and Fall", "category": "game"}]},
    {"username": "Hannes Herrmann", "items": [{"title": "Bayonetta 2 Switch", "category": "game"}, {"title": "Civ 6: Rise and Fall", "category": "game"}]},
    {"username": "Ganon", "items": [{"title": "Black Panther", "category": "film_series"}, {"title": "Shape of Water", "category": "film_series"}]},
]

MAR2018_USER_ITEMS = [
    {"username": "Aladan", "items": [{"title": "Final Fantasy XV PC", "category": "game"}, {"title": "Ni No Kuni 2", "category": "game"}, {"title": "Warhammer: Vermintide 2", "category": "game"}, {"title": "Auslöschung", "category": "film_series"}, {"title": "Pacific Rim: Uprising", "category": "film_series"}, {"title": "Tomb Raider", "category": "film_series"}]},
    {"username": "unregistriert", "items": [{"title": "Stranger Things Staffel 2", "category": "film_series"}, {"title": "Banshee", "category": "film_series"}]},
    {"username": "funrox", "items": [{"title": "Akte X neue Staffel", "category": "film_series"}, {"title": "Life is Strange: Before the Storm Bonus Episode", "category": "game"}]},
    {"username": "Olphas", "items": [{"title": "Ni No Kuni 2", "category": "game"}]},
    {"username": "Jonas S.", "items": [{"title": "Kingdom Come: Deliverance", "category": "game"}, {"title": "Love neue Staffel", "category": "film_series"}, {"title": "Santa Clarita Diet Staffel 2", "category": "film_series"}]},
    {"username": "Alain", "items": [{"title": "Bad Banks", "category": "film_series"}, {"title": "Preacher Staffel 2", "category": "film_series"}]},
    {"username": "euph", "items": [{"title": "Kingdom Come: Deliverance", "category": "game"}, {"title": "Stranger Things Staffel 2", "category": "film_series"}, {"title": "Narcos", "category": "film_series"}]},
    {"username": "Harry67", "items": [{"title": "Elite Dangerous", "category": "game"}]},
    {"username": "Drapondur", "items": [{"title": "Shroud of the Avatar", "category": "game"}]},
    {"username": "Sausi", "items": [{"title": "Life is Strange: Before the Storm", "category": "game"}]},
]

APR2018_USER_ITEMS = [
    {"username": "Olphas", "items": [{"title": "Avengers: Infinity War", "category": "film_series"}, {"title": "The Expanse Staffel 3", "category": "film_series"}]},
    {"username": "Aladan", "items": [{"title": "God of War", "category": "game"}, {"title": "Battletech", "category": "game"}, {"title": "Ready Player One", "category": "film_series"}, {"title": "Avengers: Infinity War", "category": "film_series"}]},
    {"username": "Ganon", "items": [{"title": "Deadpool 2", "category": "film_series"}]},
    {"username": "Slaytanic", "items": [{"title": "Battletech", "category": "game"}]},
    {"username": "Q-Bert", "items": [{"title": "Battletech", "category": "game"}, {"title": "Timeless Staffel 2", "category": "film_series"}]},
    {"username": "Kinukawa", "items": [{"title": "Battletech", "category": "game"}]},
    {"username": "Maverick", "items": [{"title": "Battletech", "category": "game"}]},
    {"username": "ganga", "items": [{"title": "Bosch Staffel 4", "category": "film_series"}]},
    {"username": "Jonas S.", "items": [{"title": "Ready Player One", "category": "film_series"}]},
    {"username": "Tasmanius", "items": [{"title": "The Terror", "category": "film_series"}]},
    {"username": "Extrapanzer", "items": [{"title": "The Terror", "category": "film_series"}, {"title": "The Expanse Staffel 3", "category": "film_series"}]},
    {"username": "Maestro84", "items": [{"title": "Ni No Kuni 2", "category": "game"}, {"title": "Magnum P.I. Staffel 2", "category": "film_series"}]},
    {"username": "funrox", "items": [{"title": "Akte X neue Staffel", "category": "film_series"}]},
    {"username": "g3rr0r", "items": [{"title": "God of War", "category": "game"}, {"title": "Avengers: Infinity War", "category": "film_series"}]},
    {"username": "unregistriert", "items": [{"title": "Ready Player One", "category": "film_series"}]},
]

MAY2018_USER_ITEMS = [
    {"username": "unregistriert", "items": [{"title": "Detroit: Become Human", "category": "game"}]},
    {"username": "euph", "items": [{"title": "God of War", "category": "game"}, {"title": "Detroit: Become Human", "category": "game"}, {"title": "NHL Playoffs", "category": "misc"}]},
    {"username": "Desotho", "items": [{"title": "Persona 3: Dancing Moon Night", "category": "game"}, {"title": "Persona 5: Dancing Star Night", "category": "game"}]},
    {"username": "Der Marian", "items": [{"title": "Yakuza 6", "category": "game"}]},
    {"username": "Sven Gellersen", "items": [{"title": "Detroit: Become Human", "category": "game"}]},
    {"username": "Slaytanic", "items": [{"title": "Pillars of Eternity II: Deadfire", "category": "game"}]},
    {"username": "Drapondur", "items": [{"title": "Detroit: Become Human", "category": "game"}, {"title": "Pillars of Eternity II: Deadfire", "category": "game"}]},
    {"username": "Ganon", "items": [{"title": "Deadpool 2", "category": "film_series"}, {"title": "Solo: A Star Wars Story", "category": "film_series"}]},
    {"username": "Aladan", "items": [{"title": "Detroit: Become Human", "category": "game"}, {"title": "Hyrule Warriors: Definitive Edition", "category": "game"}, {"title": "Deadpool 2", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "Destiny 2: Warmind", "category": "game"}, {"title": "Ni No Kuni 2", "category": "game"}]},
    {"username": "Maestro84", "items": [{"title": "Life is Strange: Before the Storm", "category": "game"}, {"title": "Ni No Kuni 2", "category": "game"}]},
    {"username": "Funatic", "items": [{"title": "Pillars of Eternity II: Deadfire", "category": "game"}]},
    {"username": "Chucky13", "items": [{"title": "Dark Souls Remastered", "category": "game"}, {"title": "Agony", "category": "game"}]},
    {"username": "Flammuss", "items": [{"title": "Detroit: Become Human", "category": "game"}, {"title": "Westworld Staffel 2", "category": "film_series"}]},
    {"username": "Berthold", "items": [{"title": "Detroit: Become Human", "category": "game"}]},
    {"username": "knallfix", "items": [{"title": "Pillars of Eternity II: Deadfire", "category": "game"}]},
    {"username": "Akki", "items": [{"title": "Deadpool 2", "category": "film_series"}]},
]

JUN2018_USER_ITEMS = [
    {"username": "unregistriert", "items": [{"title": "Jurassic World Evolution", "category": "game"}]},
    {"username": "Noodles", "items": [{"title": "Vampyr", "category": "game"}, {"title": "E3", "category": "misc"}]},
    {"username": "Slaytanic", "items": [{"title": "Vampyr", "category": "game"}]},
    {"username": "Triton", "items": [{"title": "Jurassic World Evolution", "category": "game"}, {"title": "Fußball-WM", "category": "misc"}]},
    {"username": "euph", "items": [{"title": "Detroit: Become Human", "category": "game"}]},
    {"username": "The HooD", "items": [{"title": "Vampyr", "category": "game"}, {"title": "Jurassic World Evolution", "category": "game"}]},
]

JUL2018_USER_ITEMS = [
    {"username": "Aladan", "items": [{"title": "Octopath Traveler", "category": "game"}, {"title": "Ys VIII: Lacrimosa of DANA", "category": "game"}, {"title": "Ant-Man and The Wasp", "category": "film_series"}]},
    {"username": "Ganon", "items": [{"title": "Ant-Man and The Wasp", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "Ant-Man and The Wasp", "category": "film_series"}]},
    {"username": "Dukuu", "items": [{"title": "Shining Resonance Refrain", "category": "game"}, {"title": "Octopath Traveler", "category": "game"}]},
    {"username": "Wunderheiler", "items": [{"title": "Octopath Traveler", "category": "game"}]},
    {"username": "Evoli", "items": [{"title": "Octopath Traveler", "category": "game"}]},
    {"username": "Desotho", "items": [{"title": "Octopath Traveler", "category": "game"}, {"title": "Shining Resonance Refrain", "category": "game"}]},
    {"username": "Wuslon", "items": [{"title": "Octopath Traveler", "category": "game"}]},
    {"username": "Q-Bert", "items": [{"title": "Wynonna Earp Staffel 3", "category": "film_series"}]},
    {"username": "John of Gaunt", "items": [{"title": "Westworld", "category": "film_series"}]},
    {"username": "Xalloc", "items": [{"title": "Tacoma", "category": "game"}, {"title": "The Red Strings Club", "category": "game"}]},
]

AUG2018_USER_ITEMS = [
    {"username": "Aladan", "items": [{"title": "Yakuza 0", "category": "game"}, {"title": "Monster Hunter World PC", "category": "game"}, {"title": "Octopath Traveler", "category": "game"}]},
    {"username": "Olphas", "items": [{"title": "Yakuza Kiwami 2", "category": "game"}, {"title": "Destiny 2", "category": "game"}]},
    {"username": "Desotho", "items": [{"title": "Yakuza Kiwami 2", "category": "game"}]},
    {"username": "Green Yoshi", "items": [{"title": "Gamescom", "category": "misc"}]},
    {"username": "Q-Bert", "items": [{"title": "Phantom Doctrine", "category": "game"}, {"title": "Cloak & Dagger", "category": "film_series"}]},
    {"username": "GeneralGonzo", "items": [{"title": "Phantom Doctrine", "category": "game"}]},
    {"username": "Triton", "items": [{"title": "Phantom Doctrine", "category": "game"}]},
    {"username": "Slaytanic", "items": [{"title": "Phantom Doctrine", "category": "game"}]},
    {"username": "Maestro84", "items": [{"title": "The Last of Us PS4", "category": "game"}, {"title": "WoW: Battle for Azeroth", "category": "game"}]},
    {"username": "Janosch", "items": [{"title": "Better Call Saul", "category": "film_series"}]},
]

SEP2018_USER_ITEMS = [
    {"username": "euph", "items": [{"title": "Spider-Man PS4", "category": "game"}, {"title": "Hollow Knight Switch", "category": "game"}]},
    {"username": "Slaytanic", "items": [{"title": "Pathfinder: Kingmaker", "category": "game"}, {"title": "The Bard's Tale 4", "category": "game"}]},
    {"username": "unregistriert", "items": [{"title": "Shadow of the Tomb Raider", "category": "game"}]},
    {"username": "Evoli", "items": [{"title": "Shadow of the Tomb Raider", "category": "game"}]},
    {"username": "Desotho", "items": [{"title": "Dragon Quest XI", "category": "game"}, {"title": "Valkyria Chronicles 4", "category": "game"}]},
    {"username": "Q-Bert", "items": [{"title": "Valkyria Chronicles 4", "category": "game"}, {"title": "Pathfinder: Kingmaker", "category": "game"}, {"title": "The Bard's Tale 4", "category": "game"}]},
    {"username": "Aladan", "items": [{"title": "Dragon Quest XI", "category": "game"}, {"title": "Spider-Man PS4", "category": "game"}, {"title": "Die Unglaublichen 2", "category": "film_series"}]},
    {"username": "Green Yoshi", "items": [{"title": "Spider-Man PS4", "category": "game"}]},
    {"username": "Olphas", "items": [{"title": "Spider-Man PS4", "category": "game"}, {"title": "Destiny 2: Forsaken", "category": "game"}, {"title": "Life is Strange 2", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "Life is Strange 2", "category": "game"}]},
    {"username": "Noodles", "items": [{"title": "Life is Strange 2", "category": "game"}]},
    {"username": "timeagent", "items": [{"title": "The Bard's Tale 4", "category": "game"}]},
    {"username": "Funatic", "items": [{"title": "Spider-Man PS4", "category": "game"}, {"title": "The Expanse Staffel 3", "category": "film_series"}]},
    {"username": "Maestro84", "items": [{"title": "Shadow of the Tomb Raider", "category": "game"}]},
    {"username": "spooky74", "items": [{"title": "Shadow of the Tomb Raider", "category": "game"}, {"title": "Jack Ryan", "category": "film_series"}]},
    {"username": "MachineryJoe", "items": [{"title": "Destiny 2: Forsaken", "category": "game"}]},
    {"username": "Graubirne76", "items": [{"title": "Shadow of the Tomb Raider", "category": "game"}]},
    {"username": "Drapondur", "items": [{"title": "Pathfinder: Kingmaker", "category": "game"}, {"title": "The Bard's Tale 4", "category": "game"}]},
    {"username": "Necromanus", "items": [{"title": "The Bard's Tale 4", "category": "game"}, {"title": "Shadow of the Tomb Raider", "category": "game"}]},
    {"username": "TheRaffer", "items": [{"title": "Shadow of the Tomb Raider", "category": "game"}]},
    {"username": "John of Gaunt", "items": [{"title": "Better Call Saul", "category": "film_series"}]},
    {"username": "Crazycommander", "items": [{"title": "Divinity: Original Sin 2 PS4", "category": "game"}, {"title": "Better Call Saul", "category": "film_series"}, {"title": "Iron Fist Staffel 2", "category": "film_series"}]},
]

OCT2018_USER_ITEMS = [
    {"username": "Slaytanic", "items": [{"title": "Red Dead Redemption 2", "category": "game"}, {"title": "Call of Cthulhu", "category": "game"}]},
    {"username": "Pro4you", "items": [{"title": "Red Dead Redemption 2", "category": "game"}]},
    {"username": "unregistriert", "items": [{"title": "Assassin's Creed: Odyssey", "category": "game"}, {"title": "Red Dead Redemption 2", "category": "game"}]},
    {"username": "Aladan", "items": [{"title": "Assassin's Creed: Odyssey", "category": "game"}, {"title": "Super Mario Party", "category": "game"}, {"title": "The World Ends With You: Final Remix", "category": "game"}, {"title": "Bohemian Rhapsody", "category": "film_series"}]},
    {"username": "euph", "items": [{"title": "Red Dead Redemption 2", "category": "game"}]},
    {"username": "timeagent", "items": [{"title": "XCOM 2: War of the Chosen - Tactical Legacy Pack", "category": "game"}, {"title": "Venom", "category": "film_series"}]},
    {"username": "Ganon", "items": [{"title": "Deutschland 86", "category": "film_series"}, {"title": "Babylon Berlin", "category": "film_series"}]},
    {"username": "Jonas S.", "items": [{"title": "Babylon Berlin", "category": "film_series"}]},
    {"username": "Wunderheiler", "items": [{"title": "The World Ends With You: Final Remix", "category": "game"}]},
    {"username": "Olphas", "items": [{"title": "Assassin's Creed: Odyssey", "category": "game"}]},
    {"username": "hex00", "items": [{"title": "Predator", "category": "film_series"}]},
    {"username": "Green Yoshi", "items": [{"title": "Babylon Berlin", "category": "film_series"}]},
    {"username": "funrox", "items": [{"title": "Halloween", "category": "film_series"}, {"title": "Versailles", "category": "film_series"}]},
    {"username": "Rumi", "items": [{"title": "The Man in the High Castle Staffel 3", "category": "film_series"}, {"title": "Call of Cthulhu", "category": "game"}]},
    {"username": "Sciron", "items": [{"title": "Call of Duty: Black Ops 4", "category": "game"}]},
]

NOV2018_USER_ITEMS = [
    {"username": "Aladan", "items": [{"title": "Diablo 3 Switch", "category": "game"}, {"title": "Darksiders 3", "category": "game"}, {"title": "Phantastische Tierwesen 2", "category": "film_series"}]},
    {"username": "Noodles", "items": [{"title": "Darksiders 3", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "House of Cards", "category": "film_series"}, {"title": "Versailles Staffelende", "category": "film_series"}]},
    {"username": "Crizzo", "items": [{"title": "Hitman 2", "category": "game"}]},
    {"username": "rammmses", "items": [{"title": "Assassin's Creed: Odyssey", "category": "game"}, {"title": "Red Dead Redemption 2", "category": "game"}, {"title": "Call of Cthulhu", "category": "game"}, {"title": "Hitman 2", "category": "game"}]},
    {"username": "Drapondur", "items": [{"title": "Underworld Ascendant", "category": "game"}]},
    {"username": "timeagent", "items": [{"title": "Battletech Linux", "category": "game"}]},
]

DEC2018_USER_ITEMS = [
    {"username": "Aladan", "items": [{"title": "Super Smash Bros. Ultimate", "category": "game"}, {"title": "Mutant Year Zero: Road to Eden", "category": "game"}, {"title": "Aquaman", "category": "film_series"}, {"title": "Mary Poppins Returns", "category": "film_series"}, {"title": "Spider-Man: Into the Spider-Verse", "category": "film_series"}]},
    {"username": "euph", "items": [{"title": "Deutschland 86", "category": "film_series"}, {"title": "Vikings", "category": "film_series"}]},
    {"username": "Slaytanic", "items": [{"title": "Mutant Year Zero: Road to Eden", "category": "game"}]},
    {"username": "timeagent", "items": [{"title": "The Bard's Tale 4 Linux", "category": "game"}]},
    {"username": "Green Yoshi", "items": [{"title": "Quantum Break", "category": "game"}, {"title": "Sunset Overdrive", "category": "game"}, {"title": "Forza Horizon 4", "category": "game"}, {"title": "Red Dead Redemption 2", "category": "game"}, {"title": "Game Awards", "category": "misc"}]},
    {"username": "Red Dox", "items": [{"title": "Stellaris: MegaCorp", "category": "game"}, {"title": "Nightflyers", "category": "film_series"}]},
    {"username": "Ganon", "items": [{"title": "The Christmas Chronicles", "category": "film_series"}, {"title": "Aquaman", "category": "film_series"}, {"title": "Spider-Man: Into the Spider-Verse", "category": "film_series"}]},
    {"username": "Mike H.", "items": [{"title": "The Orville Staffel 2", "category": "film_series"}]},
    {"username": "Harry67", "items": [{"title": "The Orville Staffel 2", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "GRIS", "category": "game"}]},
    {"username": "Desotho", "items": [{"title": "GRIS", "category": "game"}, {"title": "Atelier Arland Trilogy Switch", "category": "game"}]},
    {"username": "Crizzo", "items": [{"title": "Tatortreiniger", "category": "film_series"}]},
    {"username": "funrox", "items": [{"title": "Vikings Staffel 5", "category": "film_series"}]},
    {"username": "Janosch", "items": [{"title": "Tatortreiniger", "category": "film_series"}]},
]

MONTH_DATA = {
    "2018-01": JAN2018_USER_ITEMS,
    "2018-02": FEB2018_USER_ITEMS,
    "2018-03": MAR2018_USER_ITEMS,
    "2018-04": APR2018_USER_ITEMS,
    "2018-05": MAY2018_USER_ITEMS,
    "2018-06": JUN2018_USER_ITEMS,
    "2018-07": JUL2018_USER_ITEMS,
    "2018-08": AUG2018_USER_ITEMS,
    "2018-09": SEP2018_USER_ITEMS,
    "2018-10": OCT2018_USER_ITEMS,
    "2018-11": NOV2018_USER_ITEMS,
    "2018-12": DEC2018_USER_ITEMS,
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
