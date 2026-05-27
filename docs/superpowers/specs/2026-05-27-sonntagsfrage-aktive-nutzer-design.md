# Design: GG Sonntagsfrage – Aktive Nutzer über die Zeit

**Datum:** 2026-05-27

## Ziel

Visualisierung der aktiven GamerGlobal-Nutzer über die Zeit, gemessen an den Abstimmungen der wöchentlichen Sonntagsfrage. Quelle: https://www.gamersglobal.de/exklusiv/sonntagsfrage

## Repo-Struktur

```
gg-stats/
├── .github/workflows/update.yml   # Montags 09:05 UTC Cron
├── scripts/scrape.py              # Scraper (Python, stdlib + requests/BeautifulSoup)
├── data/polls.json                # Gescrapter Datensatz (versioniert im Repo)
└── index.html                     # Visualisierung (Chart.js via CDN, kein Build-System)
```

## Datenschema

`data/polls.json` – Array, chronologisch aufsteigend:

```json
[
  {
    "date": "2026-05-24",
    "title": "Sonntagsfrage: Braucht es die Gegenwartsebene in Assassin's Creed? [Ergebnis]",
    "votes": 481,
    "url": "/news/345516/sonntagsfrage-braucht-es-die-gegenwartsebene-in-assassins-creed-ergebnis"
  }
]
```

- `date`: Erscheinungsdatum der Umfrage (YYYY-MM-DD)
- `title`: Seitentitel inkl. `[Ergebnis]`-Suffix wenn abgeschlossen
- `votes`: Gesamtzahl der Abstimmungen
- `url`: Relativer Pfad (ohne Domain)

## Scraper (`scripts/scrape.py`)

### Initiallauf

1. Paginiert durch `/exklusiv/sonntagsfrage?page=N` (10 Einträge/Seite) bis keine „weiter"-Navigation mehr vorhanden
2. Pro Eintrag: folgt dem Link, liest Stimmenzahl aus dem Poll-Widget
3. Schreibt alle Einträge in `data/polls.json`

### Wöchentlicher Lauf (nach Initiallauf)

1. Lädt Archiv-Seite 1 (`?page=0`)
2. Extrahiert die ersten 2 URLs
3. Prüft für jede URL, ob diese bereits in `polls.json` enthalten ist
   - Ja, Titel enthält `[Ergebnis]`: kein Update nötig
   - Ja, Titel enthält noch kein `[Ergebnis]`: Votes und Titel aktualisieren
   - Nein (neue Umfrage): hinzufügen
4. Schreibt `polls.json` nur wenn Änderungen vorhanden

Alle Einträge außer den letzten 2 werden nach dem Initiallauf nie wieder angefragt.

## GitHub Actions (`.github/workflows/update.yml`)

```yaml
schedule:
  - cron: '5 9 * * 1'   # Montag 09:05 UTC
```

- Führt `scripts/scrape.py` aus
- Committed `data/polls.json` wenn Änderungen vorhanden (`git diff --exit-code`)
- Deployed via `gh-pages` Branch (GitHub Pages)

## Frontend (`index.html`)

- Lädt `data/polls.json` via `fetch()`
- **Jahr-Filter:** Button-Gruppe mit allen verfügbaren Jahren + „YtD" (Standard beim Laden)
- **Chart.js (CDN):** kombiniertes Chart
  - Balken: Votes pro Umfrage
  - Linie: 4-Wochen-gleitender Durchschnitt (rolling mean über 4 Datenpunkte)
- **Tooltip:** zeigt Titel + Datum + Votes
- **X-Achse:** Datum der Umfrage
- **Y-Achse:** Abstimmungen (absolut)
- Kein Build-System, kein Framework – reines HTML/JS/CSS

## Deployment

- `main` Branch enthält Quellcode inkl. `data/polls.json`
- GitHub Pages bedient direkt aus `main` (Root)
- Kein separater Build-Schritt nötig

## Nicht im Scope

- Kommentarzahlen als Metrik
- Vergleich verschiedener Umfrage-Typen
- Backend / Datenbank
