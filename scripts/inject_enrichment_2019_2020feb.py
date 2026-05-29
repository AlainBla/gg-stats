#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "vorfreude.json"

USER_ITEMS_2019_02 = [
    {"username": "unregistriert", "items": [{"title": "Metro Exodus", "category": "game"}]},
    {"username": "Markus K.", "items": [{"title": "Metro Exodus", "category": "game"}, {"title": "Civilization VI: Gathering Storm", "category": "game"}]},
    {"username": "Maestro84", "items": [{"title": "Civilization VI: Gathering Storm", "category": "game"}]},
    {"username": "Sokar", "items": [{"title": "Wargroove", "category": "game"}]},
    {"username": "PraetorCreech", "items": [{"title": "Star Trek: Discovery", "category": "film_series"}, {"title": "Alita: Battle Angel", "category": "film_series"}]},
    {"username": "rammmses", "items": [{"title": "Metro Exodus", "category": "game"}]},
    {"username": "Aladan", "items": [{"title": "Anthem", "category": "game"}, {"title": "Metro Exodus", "category": "game"}, {"title": "Alita: Battle Angel", "category": "film_series"}]},
    {"username": "Kinukawa", "items": [{"title": "Alita: Battle Angel", "category": "film_series"}]},
    {"username": "SaRaHk", "items": [{"title": "Etrian Odyssey Nexus", "category": "game"}]},
    {"username": "Der Marian", "items": [{"title": "Dirt Rally 2.0", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "Bordertown Staffel 2", "category": "film_series"}, {"title": "True Detective Staffel 3", "category": "film_series"}]},
    {"username": "Slaytanic", "items": [{"title": "Civilization VI: Gathering Storm", "category": "game"}]},
    {"username": "Claus", "items": [{"title": "The Americans finale Staffel", "category": "film_series"}]},
    {"username": "Bruno Lawrie", "items": [{"title": "Star Trek: Discovery", "category": "film_series"}, {"title": "The Orville Staffel 2", "category": "film_series"}]},
    {"username": "Wuslon", "items": [{"title": "Star Trek: Discovery", "category": "film_series"}]},
    {"username": "Harry67", "items": [{"title": "Anthem", "category": "game"}]},
    {"username": "wolverine", "items": [{"title": "Anthem", "category": "game"}]},
    {"username": "euph", "items": [{"title": "Resident Evil 2 Remake", "category": "game"}]},
]

USER_ITEMS_2019_03 = [
    {"username": "Flammuss", "items": [{"title": "The Division 2", "category": "game"}]},
    {"username": "Xalloc", "items": [{"title": "Trüberbrook", "category": "game"}, {"title": "Baba is You", "category": "game"}]},
    {"username": "Slaytanic", "items": [{"title": "Trüberbrook", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "Trüberbrook", "category": "game"}, {"title": "True Detective Staffel 3 Finale", "category": "film_series"}, {"title": "8 Tage", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "Devil May Cry 5", "category": "game"}]},
    {"username": "Aladan", "items": [{"title": "Captain Marvel", "category": "film_series"}, {"title": "The Division 2", "category": "game"}, {"title": "Devil May Cry 5", "category": "game"}]},
    {"username": "Sciron", "items": [{"title": "Devil May Cry 5", "category": "game"}]},
    {"username": "BigBS", "items": [{"title": "Devil May Cry 5", "category": "game"}, {"title": "Sekiro", "category": "game"}]},
    {"username": "Green Yoshi", "items": [{"title": "Skifliegen in Vikersund und Planica", "category": "misc"}, {"title": "Formel-1-Saison", "category": "misc"}]},
    {"username": "euph", "items": [{"title": "Vikings letzte Staffel", "category": "film_series"}]},
    {"username": "Maestro84", "items": [{"title": "Anno 1800", "category": "game"}, {"title": "Captain Marvel", "category": "film_series"}]},
    {"username": "Funatic", "items": [{"title": "Star Trek: Discovery neue Folgen", "category": "film_series"}]},
    {"username": "Sausi", "items": [{"title": "Trüberbrook", "category": "game"}, {"title": "The Expanse Staffel 3", "category": "film_series"}]},
    {"username": "jguillemont", "items": [{"title": "The Division 2", "category": "game"}]},
    {"username": "Bastro", "items": [{"title": "Trüberbrook", "category": "game"}]},
    {"username": "Connor", "items": [{"title": "Sekiro", "category": "game"}]},
    {"username": "John of Gaunt", "items": [{"title": "Game of Thrones Staffel 8", "category": "film_series"}]},
    {"username": "Ganon", "items": [{"title": "Captain Marvel", "category": "film_series"}, {"title": "Iron Sky 2", "category": "film_series"}]},
]

USER_ITEMS_2019_04 = [
    {"username": "Aladan", "items": [{"title": "Shazam", "category": "film_series"}, {"title": "Avengers: Endgame", "category": "film_series"}, {"title": "One Punch Man Staffel 2", "category": "film_series"}, {"title": "Anno 1800", "category": "game"}, {"title": "Days Gone", "category": "game"}]},
    {"username": "Sokar", "items": [{"title": "Anno 1800", "category": "game"}, {"title": "Game of Thrones", "category": "film_series"}]},
    {"username": "Jonas S.", "items": [{"title": "Game of Thrones", "category": "film_series"}]},
    {"username": "Red Dox", "items": [{"title": "Avengers: Endgame", "category": "film_series"}, {"title": "Game of Thrones", "category": "film_series"}, {"title": "Cobra Kai Staffel 2", "category": "film_series"}]},
    {"username": "Noodles", "items": [{"title": "Game of Thrones", "category": "film_series"}]},
    {"username": "John of Gaunt", "items": [{"title": "Avengers: Endgame", "category": "film_series"}, {"title": "Game of Thrones", "category": "film_series"}, {"title": "Anno 1800", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "Game of Thrones", "category": "film_series"}, {"title": "Last Kingdom", "category": "film_series"}]},
    {"username": "unregistriert", "items": [{"title": "Days Gone", "category": "game"}]},
    {"username": "Sciron", "items": [{"title": "Game of Thrones", "category": "film_series"}, {"title": "Love, Death + Robots", "category": "film_series"}]},
    {"username": "Ganon", "items": [{"title": "Avengers: Endgame", "category": "film_series"}, {"title": "Shazam", "category": "film_series"}, {"title": "Hellboy", "category": "film_series"}]},
    {"username": "Funatic", "items": [{"title": "Game of Thrones", "category": "film_series"}, {"title": "Bosch Staffel 5", "category": "film_series"}, {"title": "Hellboy", "category": "film_series"}, {"title": "Avengers: Endgame", "category": "film_series"}]},
    {"username": "euph", "items": [{"title": "Game of Thrones", "category": "film_series"}, {"title": "Days Gone", "category": "game"}]},
    {"username": "TheRaffer", "items": [{"title": "Game of Thrones", "category": "film_series"}]},
    {"username": "Maestro84", "items": [{"title": "Anno 1800", "category": "game"}, {"title": "Avengers: Endgame", "category": "film_series"}, {"title": "Game of Thrones", "category": "film_series"}]},
]

USER_ITEMS_2019_05 = [
    {"username": "unregistriert", "items": [{"title": "Rage 2", "category": "game"}, {"title": "A Plague Tale: Innocence", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "Game of Thrones", "category": "film_series"}, {"title": "Life is Strange 2 Episode 3", "category": "game"}]},
    {"username": "Aladan", "items": [{"title": "Detektiv Pikachu", "category": "film_series"}, {"title": "John Wick 3", "category": "film_series"}, {"title": "Godzilla: King of Monsters", "category": "film_series"}, {"title": "Days Gone", "category": "game"}]},
    {"username": "Zaroth", "items": [{"title": "John Wick 3", "category": "film_series"}]},
    {"username": "Slaytanic", "items": [{"title": "Amon Amarth neues Album", "category": "misc"}, {"title": "Rammstein neues Album", "category": "misc"}]},
    {"username": "Maestro84", "items": [{"title": "Avengers: Endgame", "category": "film_series"}, {"title": "John Wick 3", "category": "film_series"}]},
    {"username": "Noodles", "items": [{"title": "Rage 2", "category": "game"}, {"title": "A Plague Tale: Innocence", "category": "game"}]},
    {"username": "Marulez", "items": [{"title": "Rage 2", "category": "game"}]},
    {"username": "Wuslon", "items": [{"title": "John Wick 3", "category": "film_series"}, {"title": "Godzilla: King of Monsters", "category": "film_series"}]},
    {"username": "Red Dox", "items": [{"title": "Game of Thrones", "category": "film_series"}, {"title": "Archer Staffel 10", "category": "film_series"}, {"title": "Godzilla: King of Monsters", "category": "film_series"}]},
    {"username": "Sokar", "items": [{"title": "Game of Thrones", "category": "film_series"}, {"title": "Rage 2", "category": "game"}]},
    {"username": "thhko", "items": [{"title": "Good Omens", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "Life is Strange 2 Episode 3", "category": "game"}]},
    {"username": "Desotho", "items": [{"title": "Trails of Cold Steel 2 PS4", "category": "game"}]},
    {"username": "Der feine Herr", "items": [{"title": "John Wick 3", "category": "film_series"}]},
]

USER_ITEMS_2019_06 = [
    {"username": "Red Dox", "items": [{"title": "Stellaris: Ancient Relics DLC", "category": "game"}, {"title": "Battletech: Urban Warfare DLC", "category": "game"}, {"title": "Archer Staffel 10", "category": "film_series"}, {"title": "Final Space Staffel 2", "category": "film_series"}, {"title": "Jessica Jones Staffel 3", "category": "film_series"}, {"title": "E3", "category": "misc"}]},
    {"username": "Olphas", "items": [{"title": "Jessica Jones Staffel 3", "category": "film_series"}, {"title": "Trails of Cold Steel 2", "category": "game"}, {"title": "Judgment", "category": "game"}]},
    {"username": "Aladan", "items": [{"title": "Super Mario Maker 2", "category": "game"}, {"title": "Bloodstained: Ritual of the Night", "category": "game"}, {"title": "The Sinking City", "category": "game"}, {"title": "Final Fantasy XIV: Shadowbringers", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "Heavy Rain PC", "category": "game"}]},
    {"username": "Desotho", "items": [{"title": "Trails of Cold Steel 2", "category": "game"}, {"title": "Judgment", "category": "game"}]},
    {"username": "Hannes Herrmann", "items": [{"title": "Archer Staffel 10", "category": "film_series"}, {"title": "Final Space Staffel 2", "category": "film_series"}]},
    {"username": "Bastro", "items": [{"title": "A Plague Tale: Innocence", "category": "game"}]},
    {"username": "Graubirne76", "items": [{"title": "The Sinking City", "category": "game"}]},
    {"username": "Kainar", "items": [{"title": "Chernobyl", "category": "film_series"}, {"title": "Dark", "category": "film_series"}, {"title": "How to Sell Drugs Online (Fast)", "category": "film_series"}]},
]

USER_ITEMS_2019_07 = [
    {"username": "Aladan", "items": [{"title": "Spider-Man: Far from Home", "category": "film_series"}, {"title": "König der Löwen", "category": "film_series"}, {"title": "Stranger Things Staffel 3", "category": "film_series"}, {"title": "Fire Emblem: Three Houses", "category": "game"}, {"title": "Final Fantasy XIV: Shadowbringers", "category": "game"}]},
    {"username": "Noodles", "items": [{"title": "Stranger Things Staffel 3", "category": "film_series"}, {"title": "Haus des Geldes Staffel 3", "category": "film_series"}]},
    {"username": "Maverick", "items": [{"title": "Stranger Things Staffel 3", "category": "film_series"}]},
    {"username": "Jonas S.", "items": [{"title": "Stranger Things Staffel 3", "category": "film_series"}, {"title": "Orange is the New Black", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "Spider-Man: Far from Home", "category": "film_series"}, {"title": "Fire Emblem: Three Houses", "category": "game"}]},
    {"username": "timeagent", "items": [{"title": "Spider-Man: Far from Home", "category": "film_series"}]},
    {"username": "funrox", "items": [{"title": "Chernobyl", "category": "film_series"}]},
]

USER_ITEMS_2019_08 = [
    {"username": "euph", "items": [{"title": "Bloodstained: Ritual of the Night", "category": "game"}]},
    {"username": "Noodles", "items": [{"title": "Once Upon a Time in Hollywood", "category": "film_series"}, {"title": "Toy Story 4", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "Fire Emblem: Three Houses", "category": "game"}, {"title": "Der dunkle Kristall", "category": "film_series"}]},
    {"username": "Wunderheiler", "items": [{"title": "Fire Emblem: Three Houses", "category": "game"}, {"title": "Astral Chain", "category": "game"}]},
    {"username": "Specter", "items": [{"title": "Astral Chain", "category": "game"}]},
    {"username": "timeagent", "items": [{"title": "The Bard's Tale 4 Director's Cut", "category": "game"}]},
    {"username": "Aladan", "items": [{"title": "Astral Chain", "category": "game"}]},
    {"username": "Green Yoshi", "items": [{"title": "Astral Chain", "category": "game"}, {"title": "Control", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "Once Upon a Time in Hollywood", "category": "film_series"}, {"title": "City on a Hill", "category": "film_series"}]},
    {"username": "Maestro84", "items": [{"title": "Spider-Man PS4", "category": "game"}]},
    {"username": "Hannes Herrmann", "items": [{"title": "Fire Emblem: Three Houses", "category": "game"}]},
    {"username": "Harry67", "items": [{"title": "Fire Emblem: Three Houses", "category": "game"}]},
]

USER_ITEMS_2019_09 = [
    {"username": "Aladan", "items": [{"title": "Es Kapitel 2", "category": "film_series"}, {"title": "Ad Astra", "category": "film_series"}, {"title": "Greedfall", "category": "game"}, {"title": "The Surge 2", "category": "game"}, {"title": "Link's Awakening", "category": "game"}]},
    {"username": "Talakos", "items": [{"title": "The Surge 2", "category": "game"}]},
    {"username": "euph", "items": [{"title": "Link's Awakening", "category": "game"}]},
    {"username": "Olphas", "items": [{"title": "Es Kapitel 2", "category": "film_series"}]},
    {"username": "John of Gaunt", "items": [{"title": "Es Kapitel 2", "category": "film_series"}]},
    {"username": "Noodles", "items": [{"title": "The Surge 2", "category": "game"}]},
    {"username": "Hannes Herrmann", "items": [{"title": "Astral Chain", "category": "game"}, {"title": "The Surge 2", "category": "game"}, {"title": "Disenchantment Staffel 2", "category": "film_series"}]},
    {"username": "Green Yoshi", "items": [{"title": "Astral Chain", "category": "game"}, {"title": "Gears 5", "category": "game"}, {"title": "Control", "category": "game"}]},
    {"username": "Sokar", "items": [{"title": "Borderlands 3", "category": "game"}]},
    {"username": "Desotho", "items": [{"title": "Catherine: Full Body", "category": "game"}, {"title": "Daemon X Machina", "category": "game"}, {"title": "AI: The Somnium Files", "category": "game"}, {"title": "Final Fantasy VIII Remastered", "category": "game"}]},
    {"username": "Rialdar", "items": [{"title": "Fantasy General 2", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "City on a Hill Staffelende", "category": "film_series"}]},
    {"username": "Drapondur", "items": [{"title": "Greedfall", "category": "game"}]},
    {"username": "Alain", "items": [{"title": "Dark Staffel 3", "category": "film_series"}, {"title": "Haus des Geldes Staffel 3", "category": "film_series"}, {"title": "Stranger Things Staffel 3", "category": "film_series"}, {"title": "Disenchantment Staffel 2", "category": "film_series"}]},
    {"username": "Ganon", "items": [{"title": "Disenchantment Staffel 2", "category": "film_series"}]},
]

USER_ITEMS_2019_10 = [
    {"username": "Aladan", "items": [{"title": "Terminator: Dark Fate", "category": "film_series"}, {"title": "The Outer Worlds", "category": "game"}, {"title": "Luigi's Mansion 3", "category": "game"}]},
    {"username": "Janosch", "items": [{"title": "The Irishman", "category": "film_series"}, {"title": "Joker", "category": "film_series"}, {"title": "The Outer Worlds", "category": "game"}]},
    {"username": "Red Dox", "items": [{"title": "El Camino", "category": "film_series"}, {"title": "South Park Staffel 23", "category": "film_series"}]},
    {"username": "John of Gaunt", "items": [{"title": "El Camino", "category": "film_series"}, {"title": "Joker", "category": "film_series"}, {"title": "The Outer Worlds", "category": "game"}]},
    {"username": "Jonas S.", "items": [{"title": "The Walking Dead neue Staffel", "category": "film_series"}, {"title": "Joker", "category": "film_series"}, {"title": "El Camino", "category": "film_series"}, {"title": "The Outer Worlds", "category": "game"}]},
    {"username": "euph", "items": [{"title": "Joker", "category": "film_series"}, {"title": "Downton Abbey Film", "category": "film_series"}]},
    {"username": "AlexCartman", "items": [{"title": "Destiny 2: Shadowkeep", "category": "game"}]},
    {"username": "Ganon", "items": [{"title": "Gemini Man", "category": "film_series"}]},
    {"username": "Noodles", "items": [{"title": "The Outer Worlds", "category": "game"}]},
    {"username": "Bruno Lawrie", "items": [{"title": "Trine 4", "category": "game"}]},
    {"username": "Jac", "items": [{"title": "Jack Ryan Staffel 2", "category": "film_series"}]},
    {"username": "skybird", "items": [{"title": "Carnival Row", "category": "film_series"}]},
    {"username": "ganga", "items": [{"title": "Jack Ryan Staffel 2", "category": "film_series"}]},
]

USER_ITEMS_2019_11 = [
    {"username": "Aladan", "items": [{"title": "Death Stranding", "category": "game"}, {"title": "Star Wars Jedi: Fallen Order", "category": "game"}]},
    {"username": "Noodles", "items": [{"title": "Red Dead Redemption 2 PC", "category": "game"}, {"title": "Planet Zoo", "category": "game"}]},
    {"username": "Slaytanic", "items": [{"title": "Football Manager 2020", "category": "game"}, {"title": "Lost Ember", "category": "game"}]},
    {"username": "advfreak", "items": [{"title": "Blacksad: Under the Skin", "category": "game"}]},
    {"username": "rammmses", "items": [{"title": "Death Stranding", "category": "game"}]},
    {"username": "Lorion", "items": [{"title": "Death Stranding", "category": "game"}, {"title": "Star Wars Jedi: Fallen Order", "category": "game"}]},
    {"username": "Bruno Lawrie", "items": [{"title": "Death Stranding", "category": "game"}]},
    {"username": "Maestro84", "items": [{"title": "Star Wars Jedi: Fallen Order", "category": "game"}]},
    {"username": "Drapondur", "items": [{"title": "Death Stranding", "category": "game"}]},
    {"username": "John of Gaunt", "items": [{"title": "The Outer Worlds", "category": "game"}, {"title": "4 Blocks", "category": "film_series"}]},
    {"username": "Desotho", "items": [{"title": "Trails of Cold Steel 3", "category": "game"}]},
    {"username": "xan", "items": [{"title": "Blacksad: Under the Skin", "category": "game"}]},
    {"username": "TheLastToKnow", "items": [{"title": "Rick & Morty neue Folgen", "category": "film_series"}]},
    {"username": "Thomas Schmitz", "items": [{"title": "Judgment", "category": "game"}]},
]

USER_ITEMS_2019_12 = [
    {"username": "Maverick", "items": [{"title": "The Witcher", "category": "film_series"}, {"title": "The Expanse Staffel 4", "category": "film_series"}, {"title": "Lost in Space Staffel 2", "category": "film_series"}]},
    {"username": "Aladan", "items": [{"title": "Darksiders Genesis", "category": "game"}, {"title": "The Witcher", "category": "film_series"}, {"title": "Star Wars Episode 9", "category": "film_series"}]},
    {"username": "funrox", "items": [{"title": "Life is Strange 2 letzte Episode", "category": "game"}, {"title": "Vikings letzte Staffel", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "Darksiders Genesis", "category": "game"}, {"title": "Life is Strange 2 letzte Episode", "category": "game"}]},
    {"username": "Desotho", "items": [{"title": "Trails of Cold Steel 3", "category": "game"}, {"title": "Life is Strange 2", "category": "game"}]},
    {"username": "Slaytanic", "items": [{"title": "Life is Strange 2", "category": "game"}]},
    {"username": "thhko", "items": [{"title": "Star Wars Episode 9", "category": "film_series"}, {"title": "The Expanse Staffel 4", "category": "film_series"}]},
    {"username": "Red Dox", "items": [{"title": "The Mandalorian", "category": "film_series"}, {"title": "Total War: Warhammer II neues Update", "category": "game"}]},
    {"username": "GeneralGonzo", "items": [{"title": "Phoenix Point", "category": "game"}]},
    {"username": "antares", "items": [{"title": "MechWarrior 5", "category": "game"}]},
    {"username": "Kinukawa", "items": [{"title": "MechWarrior 5", "category": "game"}]},
    {"username": "Cura", "items": [{"title": "Transport Fever 2", "category": "game"}]},
    {"username": "Sokar", "items": [{"title": "Control", "category": "game"}]},
    {"username": "Drapondur", "items": [{"title": "Star Wars Episode 9", "category": "film_series"}, {"title": "Star Wars Jedi: Fallen Order", "category": "game"}]},
    {"username": "TheRaffer", "items": [{"title": "The Witcher 3", "category": "game"}]},
]

USER_ITEMS_2020_02 = [
    {"username": "Green Yoshi", "items": [{"title": "Dreams", "category": "game"}]},
    {"username": "euph", "items": [{"title": "Star Trek: Picard", "category": "film_series"}, {"title": "Jack Ryan Staffel 2", "category": "film_series"}, {"title": "Vikings letzte Staffel", "category": "film_series"}]},
    {"username": "xan", "items": [{"title": "Star Trek: Picard", "category": "film_series"}]},
    {"username": "Aladan", "items": [{"title": "Darksiders Genesis PS4", "category": "game"}, {"title": "Birds of Prey", "category": "film_series"}, {"title": "Star Trek: Picard", "category": "film_series"}]},
    {"username": "funrox", "items": [{"title": "Babylon Berlin Staffel 3", "category": "film_series"}]},
    {"username": "unregistriert", "items": [{"title": "Star Trek: Picard", "category": "film_series"}]},
    {"username": "TheLastToKnow", "items": [{"title": "Better Call Saul", "category": "film_series"}, {"title": "Brooklyn Nine-Nine neue Staffel", "category": "film_series"}]},
    {"username": "John of Gaunt", "items": [{"title": "Better Call Saul", "category": "film_series"}]},
    {"username": "TSH-Lightning", "items": [{"title": "Narcos: Mexico", "category": "film_series"}, {"title": "Altered Carbon Staffel 2", "category": "film_series"}, {"title": "The Expanse Staffel 4", "category": "film_series"}]},
    {"username": "Jonas S.", "items": [{"title": "A Plague Tale: Innocence", "category": "game"}]},
    {"username": "Desotho", "items": [{"title": "Tokyo Mirage #FE Encore", "category": "game"}, {"title": "Fire Emblem: Three Houses", "category": "game"}, {"title": "Yakuza 3", "category": "game"}]},
    {"username": "DerBesserwisser", "items": [{"title": "Altered Carbon Staffel 2", "category": "film_series"}]},
    {"username": "Maestro84", "items": [{"title": "Civilization VI Switch", "category": "game"}]},
]

MONTH_DATA = {
    "2019-02": USER_ITEMS_2019_02,
    "2019-03": USER_ITEMS_2019_03,
    "2019-04": USER_ITEMS_2019_04,
    "2019-05": USER_ITEMS_2019_05,
    "2019-06": USER_ITEMS_2019_06,
    "2019-07": USER_ITEMS_2019_07,
    "2019-08": USER_ITEMS_2019_08,
    "2019-09": USER_ITEMS_2019_09,
    "2019-10": USER_ITEMS_2019_10,
    "2019-11": USER_ITEMS_2019_11,
    "2019-12": USER_ITEMS_2019_12,
    "2020-02": USER_ITEMS_2020_02,
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
