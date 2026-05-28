#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "vorfreude.json"

OCT2020_USER_ITEMS = [
    {"username": "Vampiro", "items": [{"title": "FIFA 21", "category": "game"}, {"title": "Battle for the Bosporus", "category": "game"}]},
    {"username": "rammmses", "items": [{"title": "Amnesia: Rebirth", "category": "game"}, {"title": "Little Hope", "category": "game"}, {"title": "Song of Horror Konsolenversion", "category": "game"}]},
    {"username": "Maverick", "items": [{"title": "Star Wars: Squadrons", "category": "game"}, {"title": "Star Trek: Discovery Staffel 3", "category": "film_series"}]},
    {"username": "Red Dox", "items": [{"title": "South Park: Pandemic Special", "category": "misc"}, {"title": "Archer Staffel 11", "category": "film_series"}, {"title": "The Mandalorian Staffel 2", "category": "film_series"}, {"title": "Star Trek: Lower Decks", "category": "film_series"}, {"title": "Star Wars: Squadrons", "category": "game"}, {"title": "Total War: Warhammer II DLC", "category": "game"}, {"title": "Stellaris: Necroids", "category": "game"}]},
    {"username": "Olphas", "items": [{"title": "The Legend of Heroes: Trails of Cold Steel IV", "category": "game"}]},
    {"username": "Drapondur", "items": [{"title": "Star Wars: Squadrons", "category": "game"}, {"title": "The Dark Pictures Anthology: Little Hope", "category": "game"}]},
    {"username": "Noodles", "items": [{"title": "Watch Dogs: Legion", "category": "game"}]},
    {"username": "Sokar", "items": [{"title": "Age of Empires III: Definitive Edition", "category": "game"}, {"title": "Doom Eternal DLC", "category": "game"}]},
    {"username": "Funatic", "items": [{"title": "The Mandalorian Staffel 2", "category": "film_series"}]},
    {"username": "Baumkuchen", "items": [{"title": "Star Trek: Discovery Staffel 3", "category": "film_series"}, {"title": "The Mandalorian Staffel 2", "category": "film_series"}]},
    {"username": "doom-o-matic", "items": [{"title": "The Mandalorian Staffel 2", "category": "film_series"}]},
]

NOV2020_USER_ITEMS = [
    {"username": "Drapondur", "items": [{"title": "Assassin's Creed: Valhalla", "category": "game"}, {"title": "TESO: Markarth", "category": "game"}]},
    {"username": "Wunderheiler", "items": [{"title": "Hyrule Warriors: Zeit der Verheerung", "category": "game"}]},
    {"username": "Green Yoshi", "items": [{"title": "Watch Dogs: Legion", "category": "game"}, {"title": "Spider-Man: Miles Morales", "category": "game"}]},
    {"username": "Ganon", "items": [{"title": "iZombie Finale", "category": "film_series"}, {"title": "Borat 2", "category": "film_series"}]},
    {"username": "Slaytanic", "items": [{"title": "Football Manager 2021", "category": "game"}, {"title": "Yakuza: Like a Dragon", "category": "game"}]},
    {"username": "unregistriert", "items": [{"title": "Assassin's Creed: Valhalla", "category": "game"}, {"title": "Demon's Souls Remake", "category": "game"}]},
    {"username": "Jac", "items": [{"title": "The Mandalorian Staffel 2", "category": "film_series"}]},
    {"username": "Necromanus", "items": [{"title": "The Mandalorian Staffel 2", "category": "film_series"}, {"title": "Star Trek: Discovery Staffel 3", "category": "film_series"}]},
    {"username": "Aladan", "items": [{"title": "Spider-Man: Miles Morales", "category": "game"}, {"title": "Demon's Souls Remake", "category": "game"}, {"title": "Assassin's Creed: Valhalla", "category": "game"}, {"title": "Hyrule Warriors: Zeit der Verheerung", "category": "game"}]},
    {"username": "rammmses", "items": [{"title": "Watch Dogs: Legion", "category": "game"}, {"title": "Yakuza: Like a Dragon", "category": "game"}, {"title": "Observer: System Redux", "category": "game"}]},
    {"username": "Danywilde", "items": [{"title": "Demon's Souls Remake", "category": "game"}]},
    {"username": "euph", "items": [{"title": "Spider-Man: Miles Morales", "category": "game"}, {"title": "Star Trek: Discovery Staffel 3", "category": "film_series"}]},
    {"username": "Funatic", "items": [{"title": "The Mandalorian Staffel 2", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "Yakuza: Like a Dragon", "category": "game"}]},
    {"username": "Noodles", "items": [{"title": "Assassin's Creed: Valhalla", "category": "game"}, {"title": "Suburra Staffel 3", "category": "film_series"}]},
]

DEC2020_USER_ITEMS = [
    {"username": "euph", "items": [{"title": "Cyberpunk 2077", "category": "game"}]},
    {"username": "The Real Maulwurfn", "items": [{"title": "Total War: Warhammer II - Twisted & Twilight", "category": "game"}, {"title": "Cyberpunk 2077", "category": "game"}, {"title": "The Mandalorian Staffel 2 Finale", "category": "film_series"}]},
    {"username": "Red Dox", "items": [{"title": "Cyberpunk 2077", "category": "game"}, {"title": "The Mandalorian Staffel 2 Finale", "category": "film_series"}, {"title": "Alien Worlds", "category": "film_series"}]},
    {"username": "Q-Bert", "items": [{"title": "The Mandalorian Staffel 2", "category": "film_series"}, {"title": "Star Trek: Discovery Staffel 3", "category": "film_series"}, {"title": "NeXt", "category": "film_series"}]},
    {"username": "Green Yoshi", "items": [{"title": "Cyberpunk 2077", "category": "game"}, {"title": "Skifliegen Planica", "category": "misc"}]},
    {"username": "funrox", "items": [{"title": "Tell Me Why", "category": "game"}]},
    {"username": "LRod", "items": [{"title": "Cyberpunk 2077", "category": "game"}]},
    {"username": "Faxenmacher", "items": [{"title": "Cyberpunk 2077", "category": "game"}, {"title": "The Last of Us Part II", "category": "game"}]},
    {"username": "MicBass", "items": [{"title": "Cyberpunk 2077", "category": "game"}]},
    {"username": "rammmses", "items": [{"title": "Cyberpunk 2077", "category": "game"}]},
    {"username": "Danywilde", "items": [{"title": "Cyberpunk 2077", "category": "game"}]},
    {"username": "Drapondur", "items": [{"title": "Immortals Fenyx Rising", "category": "game"}, {"title": "Twin Mirror", "category": "game"}]},
    {"username": "Sokar", "items": [{"title": "Cyberpunk 2077", "category": "game"}]},
    {"username": "Harry67", "items": [{"title": "Cyberpunk 2077", "category": "game"}]},
]

FEB2021_USER_ITEMS = [
    {"username": "Green Yoshi", "items": [{"title": "Super Mario 3D World + Bowser's Fury", "category": "game"}, {"title": "Australian Open", "category": "misc"}, {"title": "Skisprung-WM in Oberstdorf", "category": "misc"}]},
    {"username": "Ganon", "items": [{"title": "WandaVision", "category": "film_series"}, {"title": "Castlevania Staffel 3", "category": "film_series"}]},
    {"username": "advfreak", "items": [{"title": "Super Mario 3D World + Bowser's Fury", "category": "game"}]},
    {"username": "Vampiro", "items": [{"title": "Imperator: Rome Update", "category": "game"}, {"title": "Everspace 2", "category": "game"}]},
    {"username": "Sciron", "items": [{"title": "Control Ultimate Edition PS5", "category": "game"}]},
    {"username": "euph", "items": [{"title": "Control PS5", "category": "game"}, {"title": "WandaVision", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "WandaVision", "category": "film_series"}]},
    {"username": "Danywilde", "items": [{"title": "Control", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "Mafia - Definitive Edition", "category": "game"}, {"title": "Twin Mirror", "category": "game"}, {"title": "Super Mario 3D World", "category": "game"}]},
    {"username": "Slaytanic", "items": [{"title": "Little Nightmares 2", "category": "game"}]},
    {"username": "StefanH", "items": [{"title": "Bravely Default II", "category": "game"}]},
    {"username": "Wuslon", "items": [{"title": "Legend of Vox Machina", "category": "film_series"}]},
    {"username": "MicBass", "items": [{"title": "The Expanse Staffel 6", "category": "film_series"}, {"title": "Book of Boba Fett", "category": "film_series"}]},
    {"username": "Funatic", "items": [{"title": "Euphoria", "category": "film_series"}]},
]

MAR2021_USER_ITEMS = [
    {"username": "Green Yoshi", "items": [{"title": "WandaVision Finale", "category": "film_series"}, {"title": "Skifliegen in Planica", "category": "misc"}]},
    {"username": "Markus K.", "items": [{"title": "Ark: Genesis Part 2", "category": "game"}]},
    {"username": "Baumkuchen", "items": [{"title": "Valheim", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "Two Weeks to Live", "category": "film_series"}, {"title": "C.B. Strike Staffel 2", "category": "film_series"}, {"title": "Mafia - Definitive Edition", "category": "game"}, {"title": "Twin Mirror", "category": "game"}]},
    {"username": "DerBesserwisser", "items": [{"title": "Cyber Shadow", "category": "game"}]},
]

APR2021_USER_ITEMS = [
    {"username": "StefanH", "items": [{"title": "Stellaris: Nemesis", "category": "game"}]},
    {"username": "Jac", "items": [{"title": "Outriders", "category": "game"}]},
    {"username": "rammmses", "items": [{"title": "Outriders", "category": "game"}]},
    {"username": "unregistriert", "items": [{"title": "Outriders", "category": "game"}, {"title": "NieR Replicant", "category": "game"}]},
    {"username": "Olphas", "items": [{"title": "Outriders", "category": "game"}, {"title": "The Falcon and the Winter Soldier", "category": "film_series"}]},
    {"username": "Sokar", "items": [{"title": "NieR Replicant Remake", "category": "game"}]},
    {"username": "Danywilde", "items": [{"title": "Days Gone PC", "category": "game"}]},
    {"username": "MicBass", "items": [{"title": "Lupin", "category": "film_series"}, {"title": "Luther neue Staffel", "category": "film_series"}]},
    {"username": "Sciron", "items": [{"title": "Outriders", "category": "game"}, {"title": "Yakuza 5 Remastered", "category": "game"}]},
    {"username": "Vampiro", "items": [{"title": "Stellaris: Nemesis", "category": "game"}, {"title": "Outriders", "category": "game"}]},
    {"username": "John of Gaunt", "items": [{"title": "The Binding of Isaac: Repentance", "category": "game"}]},
    {"username": "Maestro84", "items": [{"title": "Attack on Titan Finale Teil 1", "category": "film_series"}]},
    {"username": "Funatic", "items": [{"title": "Pillars of Eternity II: Deadfire", "category": "game"}, {"title": "Octopath Traveler", "category": "game"}]},
    {"username": "Maverick", "items": [{"title": "Outriders", "category": "game"}]},
]

MAY2021_USER_ITEMS = [
    {"username": "euph", "items": [{"title": "Resident Evil Village", "category": "game"}]},
    {"username": "Danywilde", "items": [{"title": "Resident Evil Village", "category": "game"}]},
    {"username": "Robokopp", "items": [{"title": "Resident Evil Village", "category": "game"}, {"title": "Mass Effect Legendary Edition", "category": "game"}]},
    {"username": "Drapondur", "items": [{"title": "Mass Effect Legendary Edition", "category": "game"}]},
    {"username": "Ganon", "items": [{"title": "Biomutant", "category": "game"}]},
    {"username": "Pro4you", "items": [{"title": "Biomutant", "category": "game"}]},
    {"username": "MachineryJoe", "items": [{"title": "Elite Dangerous: Odyssey", "category": "game"}]},
    {"username": "timeagent", "items": [{"title": "Elite Dangerous: Odyssey", "category": "game"}, {"title": "Mass Effect Legendary Edition", "category": "game"}]},
    {"username": "Bruno Lawrie", "items": [{"title": "Resident Evil Village", "category": "game"}]},
    {"username": "Noodles", "items": [{"title": "Biomutant", "category": "game"}, {"title": "Castlevania Staffel 4", "category": "film_series"}, {"title": "Love, Death & Robots Staffel 2", "category": "film_series"}]},
    {"username": "Red Dox", "items": [{"title": "Army of the Dead", "category": "film_series"}, {"title": "Love, Death & Robots Staffel 2", "category": "film_series"}, {"title": "Mortal Kombat", "category": "film_series"}, {"title": "Lucifer Staffel 5 Teil 2", "category": "film_series"}, {"title": "Subnautica: Below Zero", "category": "game"}, {"title": "Mass Effect Legendary Edition", "category": "game"}]},
    {"username": "Funatic", "items": [{"title": "Biomutant", "category": "game"}, {"title": "Mass Effect Legendary Edition", "category": "game"}]},
    {"username": "StefanH", "items": [{"title": "Shin Megami Tensei III: Nocturne HD Remaster", "category": "game"}]},
    {"username": "Micha", "items": [{"title": "Shin Megami Tensei III: Nocturne HD Remaster", "category": "game"}]},
    {"username": "LRod", "items": [{"title": "Biomutant", "category": "game"}]},
    {"username": "Bantadur", "items": [{"title": "Love, Death & Robots Staffel 2", "category": "film_series"}, {"title": "Mass Effect Legendary Edition", "category": "game"}]},
    {"username": "Pomme", "items": [{"title": "Mythic Quest Staffel 2", "category": "film_series"}]},
    {"username": "Wuslon", "items": [{"title": "Castlevania Staffel 4", "category": "film_series"}]},
    {"username": "funrox", "items": [{"title": "City on a Hill neue Staffel", "category": "film_series"}]},
]

JUN2021_USER_ITEMS = [
    {"username": "unregistriert", "items": [{"title": "Loki", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "Loki", "category": "film_series"}, {"title": "Sweet Tooth", "category": "film_series"}]},
    {"username": "Wuslon", "items": [{"title": "Loki", "category": "film_series"}, {"title": "Bosch Staffel 7", "category": "film_series"}, {"title": "Fußball-EM", "category": "misc"}]},
    {"username": "Keppel", "items": [{"title": "Bosch Staffel 7", "category": "film_series"}, {"title": "Fußball-EM", "category": "misc"}]},
    {"username": "Green Yoshi", "items": [{"title": "French Open", "category": "misc"}, {"title": "Fußball-EM", "category": "misc"}, {"title": "Ratchet & Clank: Rift Apart", "category": "game"}]},
    {"username": "Berndor", "items": [{"title": "Ratchet & Clank: Rift Apart", "category": "game"}]},
    {"username": "Baumkuchen", "items": [{"title": "E3", "category": "misc"}]},
    {"username": "Sciron", "items": [{"title": "E3", "category": "misc"}]},
    {"username": "rammmses", "items": [{"title": "Metro Exodus: Enhanced Edition", "category": "game"}]},
    {"username": "Benjamin Braun", "items": [{"title": "Bosch Staffel 7", "category": "film_series"}]},
    {"username": "euph", "items": [{"title": "Fußball-EM", "category": "misc"}]},
    {"username": "funrox", "items": [{"title": "Lupin Staffel 2", "category": "film_series"}]},
    {"username": "LRod", "items": [{"title": "Lupin Staffel 2", "category": "film_series"}]},
    {"username": "MicBass", "items": [{"title": "Lupin Staffel 2", "category": "film_series"}, {"title": "Bosch Staffel 7", "category": "film_series"}]},
    {"username": "Drapondur", "items": [{"title": "TESO: Blackwood", "category": "game"}]},
]

JUL2021_USER_ITEMS = [
    {"username": "goldetter", "items": [{"title": "Godzilla vs. Kong", "category": "film_series"}, {"title": "Judas and the Black Messiah", "category": "film_series"}]},
    {"username": "Olphas", "items": [{"title": "Black Widow", "category": "film_series"}, {"title": "The Great Ace Attorney Chronicles", "category": "game"}]},
    {"username": "Wuslon", "items": [{"title": "Zelda: Skyward Sword HD", "category": "game"}, {"title": "Masters of the Universe: Revelation", "category": "film_series"}, {"title": "How to Sell Drugs Online (Fast) Staffel 3", "category": "film_series"}]},
    {"username": "The Real Maulwurfn", "items": [{"title": "Microsoft Flight Simulator Xbox", "category": "game"}, {"title": "The Ascent", "category": "game"}]},
    {"username": "rammmses", "items": [{"title": "Microsoft Flight Simulator Xbox", "category": "game"}, {"title": "The Ascent", "category": "game"}]},
    {"username": "timeagent", "items": [{"title": "Elite Dangerous", "category": "game"}, {"title": "Black Widow", "category": "film_series"}]},
    {"username": "Red Dox", "items": [{"title": "Rick & Morty Staffel 5", "category": "film_series"}, {"title": "Tribes of Midgard", "category": "game"}, {"title": "Masters of the Universe: Revelation", "category": "film_series"}]},
    {"username": "Sciron", "items": [{"title": "The Ascent", "category": "game"}]},
    {"username": "StefanH", "items": [{"title": "Zelda: Skyward Sword HD", "category": "game"}]},
    {"username": "Green Yoshi", "items": [{"title": "F1 2021", "category": "game"}]},
    {"username": "schlammonster", "items": [{"title": "Once Upon a Time in Hollywood", "category": "film_series"}]},
    {"username": "Alain", "items": [{"title": "The Morning Show Staffel 1", "category": "film_series"}]},
]

AUG2021_USER_ITEMS = [
    {"username": "Player One", "items": [{"title": "Humankind", "category": "game"}]},
    {"username": "unregistriert", "items": [{"title": "Ghost of Tsushima Director's Cut", "category": "game"}, {"title": "Twelve Minutes", "category": "game"}, {"title": "Psychonauts 2", "category": "game"}]},
    {"username": "Sciron", "items": [{"title": "Hades Xbox", "category": "game"}]},
    {"username": "Micha", "items": [{"title": "Twelve Minutes", "category": "game"}]},
    {"username": "Maestro84", "items": [{"title": "Humankind", "category": "game"}]},
    {"username": "Robokopp", "items": [{"title": "Kena: Bridge of Spirits", "category": "game"}, {"title": "Psychonauts 2", "category": "game"}, {"title": "Ghost of Tsushima Director's Cut", "category": "game"}]},
    {"username": "Olphas", "items": [{"title": "The Great Ace Attorney Chronicles", "category": "game"}, {"title": "The Ascent", "category": "game"}, {"title": "Psychonauts 2", "category": "game"}]},
    {"username": "Danywilde", "items": [{"title": "Ghost of Tsushima Director's Cut", "category": "game"}]},
    {"username": "Noodles", "items": [{"title": "Twelve Minutes", "category": "game"}, {"title": "Psychonauts 2", "category": "game"}]},
    {"username": "Slaytanic", "items": [{"title": "Psychonauts 2", "category": "game"}, {"title": "Humankind", "category": "game"}]},
    {"username": "Funatic", "items": [{"title": "The Green Knight", "category": "film_series"}]},
    {"username": "Maverick", "items": [{"title": "Humankind", "category": "game"}, {"title": "King's Bounty II", "category": "game"}, {"title": "Twelve Minutes", "category": "game"}]},
    {"username": "Green Yoshi", "items": [{"title": "Fabian", "category": "film_series"}, {"title": "Psychonauts 2", "category": "game"}, {"title": "Twelve Minutes", "category": "game"}]},
    {"username": "Akki", "items": [{"title": "Evangelion 3.0+1.01", "category": "film_series"}]},
    {"username": "Drapondur", "items": [{"title": "Ghost of Tsushima Director's Cut", "category": "game"}]},
    {"username": "Sokar", "items": [{"title": "Mythic Quest Staffel 2", "category": "film_series"}, {"title": "Ted Lasso Staffel 2", "category": "film_series"}]},
]

SEP2021_USER_ITEMS = [
    {"username": "Crizzo", "items": [{"title": "Venom 2", "category": "film_series"}, {"title": "No Time to Die", "category": "film_series"}]},
    {"username": "Noodles", "items": [{"title": "Deathloop", "category": "game"}, {"title": "Life is Strange: True Colors", "category": "game"}, {"title": "Kena: Bridge of Spirits", "category": "game"}]},
    {"username": "unregistriert", "items": [{"title": "Deathloop", "category": "game"}, {"title": "Diablo II: Resurrected", "category": "game"}]},
    {"username": "crux", "items": [{"title": "Outer Wilds: Echoes of the Eye", "category": "game"}]},
    {"username": "Olphas", "items": [{"title": "Tales of Arise", "category": "game"}, {"title": "Lost Judgment", "category": "game"}]},
    {"username": "Micha", "items": [{"title": "Pathfinder: Wrath of the Righteous", "category": "game"}, {"title": "Life is Strange: True Colors", "category": "game"}]},
    {"username": "Q-Bert", "items": [{"title": "Pathfinder: Wrath of the Righteous", "category": "game"}]},
    {"username": "el_Matzos", "items": [{"title": "Pathfinder: Wrath of the Righteous", "category": "game"}]},
    {"username": "Slaytanic", "items": [{"title": "Pathfinder: Wrath of the Righteous", "category": "game"}, {"title": "Lost Judgment", "category": "game"}]},
    {"username": "Alain", "items": [{"title": "Haus des Geldes Staffel 5", "category": "film_series"}, {"title": "Psychonauts 2", "category": "game"}]},
    {"username": "funrox", "items": [{"title": "Life is Strange: True Colors", "category": "game"}]},
    {"username": "Robokopp", "items": [{"title": "Kena: Bridge of Spirits", "category": "game"}, {"title": "Deathloop", "category": "game"}, {"title": "Dune", "category": "film_series"}]},
    {"username": "Danywilde", "items": [{"title": "Ghost of Tsushima: Iki Island", "category": "game"}, {"title": "No Time to Die", "category": "film_series"}, {"title": "Dune", "category": "film_series"}]},
    {"username": "Green Yoshi", "items": [{"title": "Life is Strange: True Colors", "category": "game"}, {"title": "Deathloop", "category": "game"}, {"title": "Kena: Bridge of Spirits", "category": "game"}, {"title": "WarioWare: Get It Together!", "category": "game"}]},
    {"username": "Hannes Herrmann", "items": [{"title": "Pathfinder: Wrath of the Righteous", "category": "game"}, {"title": "Tales of Arise", "category": "game"}]},
    {"username": "rammmses", "items": [{"title": "Dune", "category": "film_series"}, {"title": "Lost Judgment", "category": "game"}, {"title": "Life is Strange: True Colors", "category": "game"}]},
    {"username": "Maestro84", "items": [{"title": "Dune", "category": "film_series"}]},
    {"username": "Sokar", "items": [{"title": "Deathloop", "category": "game"}, {"title": "Dune", "category": "film_series"}]},
    {"username": "Shake_s_beer", "items": [{"title": "Kena: Bridge of Spirits", "category": "game"}, {"title": "Deathloop", "category": "game"}, {"title": "Dune", "category": "film_series"}]},
    {"username": "Harry67", "items": [{"title": "Elite Dangerous: Odyssey", "category": "game"}]},
]

OCT2021_USER_ITEMS = [
    {"username": "Crizzo", "items": [{"title": "No Time to Die", "category": "film_series"}, {"title": "Age of Empires IV", "category": "game"}]},
    {"username": "Ganon", "items": [{"title": "Guardians of the Galaxy", "category": "game"}, {"title": "Metroid Dread", "category": "game"}]},
    {"username": "Shake_s_beer", "items": [{"title": "Metroid Dread", "category": "game"}, {"title": "Age of Empires IV", "category": "game"}, {"title": "No Time to Die", "category": "film_series"}, {"title": "Dune", "category": "film_series"}]},
    {"username": "The Real Maulwurfn", "items": [{"title": "Foundation", "category": "film_series"}]},
    {"username": "StefanH", "items": [{"title": "Metroid Dread", "category": "game"}]},
    {"username": "euph", "items": [{"title": "No Time to Die", "category": "film_series"}, {"title": "Free Guy", "category": "film_series"}]},
    {"username": "Drapondur", "items": [{"title": "The Dark Pictures Anthology: House of Ashes", "category": "game"}]},
    {"username": "e5150", "items": [{"title": "Thrash Nightmare Festival", "category": "misc"}]},
    {"username": "unregistriert", "items": [{"title": "Far Cry 6", "category": "game"}, {"title": "Age of Empires IV", "category": "game"}]},
    {"username": "Green Yoshi", "items": [{"title": "Dune", "category": "film_series"}, {"title": "No Time to Die", "category": "film_series"}, {"title": "Deathloop", "category": "game"}, {"title": "Life is Strange: True Colors", "category": "game"}]},
    {"username": "timeagent", "items": [{"title": "Halloween Kills", "category": "film_series"}]},
    {"username": "Bruno Lawrie", "items": [{"title": "The Good Life", "category": "game"}]},
    {"username": "Robokopp", "items": [{"title": "Far Cry 6", "category": "game"}, {"title": "Guardians of the Galaxy", "category": "game"}]},
    {"username": "John of Gaunt", "items": [{"title": "Dune", "category": "film_series"}, {"title": "Homeland Staffel 8", "category": "film_series"}]},
    {"username": "Alain", "items": [{"title": "The Morning Show Staffel 2", "category": "film_series"}]},
    {"username": "Vampiro", "items": [{"title": "Age of Empires IV", "category": "game"}]},
    {"username": "Slaytanic", "items": [{"title": "The Good Life", "category": "game"}]},
]

MONTH_DATA = {
    "2020-10": OCT2020_USER_ITEMS,
    "2020-11": NOV2020_USER_ITEMS,
    "2020-12": DEC2020_USER_ITEMS,
    "2021-02": FEB2021_USER_ITEMS,
    "2021-03": MAR2021_USER_ITEMS,
    "2021-04": APR2021_USER_ITEMS,
    "2021-05": MAY2021_USER_ITEMS,
    "2021-06": JUN2021_USER_ITEMS,
    "2021-07": JUL2021_USER_ITEMS,
    "2021-08": AUG2021_USER_ITEMS,
    "2021-09": SEP2021_USER_ITEMS,
    "2021-10": OCT2021_USER_ITEMS,
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
