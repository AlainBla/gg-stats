# Design: Vorfreude-Scraper

**Date:** 2026-05-27  
**Status:** Approved

## Problem

GamersGlobal veröffentlicht jeden Monat einen Artikel "Darauf freut sich die Redaktion im [Monat]". Redakteure listen Filme/Serien, Spiele/Brettspiele und Sonstiges auf, worauf sie sich freuen (als `<strong>`/`<em>` formatiert). User nennen in Kommentaren ebenfalls Items — als Plaintext ohne Formatierung. Bisher gibt es keine aggregierte Statistik, welche Titel wie oft genannt werden.

## Goal

Pro Monat: Welche Items werden wie oft von wie vielen unterschiedlichen Personen (Redakteure + User) genannt? Visualisiert im bestehenden Chart.js-Frontend.

## Architecture

```
GamersGlobal HTML
    ↓ requests + BeautifulSoup4
scrape_freude.py
    ├── discover_articles()   — bekannte URLs + Suche /suche?q=darauf+freut+sich+die+redaktion
    ├── parse_article(url)    — Editor-Items via <strong>/<em> + [KATEGORIE]-Label-Parsing
    ├── parse_comments(soup)  — Raw comment text + username pro Kommentar
    └── enrich_comments()     — Claude Haiku (claude-haiku-4-5) → strukturierte Items
         ↓
data/vorfreude.json   (git-committed, master data)
data/vorfreude.csv    (derived export)
         ↓
index.html            (neuer "Vorfreude"-Abschnitt, Chart.js)
```

### Two Modes

| Flag | Beschreibung | Läuft in |
|------|-------------|----------|
| `--no-enrich` (default) | HTML-only: Editor-Items + raw comments. Committed wenn comment_count geändert. | GitHub Actions (täglich) |
| `--enrich` | Liest `comments_raw`, schickt an Claude Haiku, füllt `user_items`. Manuell commiten. | Lokal mit `ANTHROPIC_API_KEY` |

## Data Model (`data/vorfreude.json`)

```json
[
  {
    "month": "2026-05",
    "url": "https://www.gamersglobal.de/news/343659/...",
    "title": "Darauf freut sich die Redaktion im Mai 2026",
    "last_updated": "2026-05-27T10:00:00Z",
    "comment_count": 87,
    "editors": [
      {
        "name": "Jörg Langer",
        "items": [
          {"title": "007 Dying Light", "category": "game"},
          {"title": "The Boroughs",   "category": "film_series"},
          {"title": "Sommerurlaub",   "category": "misc"}
        ]
      }
    ],
    "comments_raw": [
      {"username": "user123", "text": "Ich freue mich sehr auf Elden Ring DLC..."}
    ],
    "user_items": [
      {
        "username": "user123",
        "items": [{"title": "Elden Ring DLC", "category": "game"}]
      }
    ],
    "item_stats": {
      "Elden Ring DLC": {
        "count": 5,
        "category": "game",
        "mentioners": ["editor:joerg", "user:user123", "user:user456"]
      }
    }
  }
]
```

**Notes:**
- `comments_raw` ermöglicht Re-Enrichment ohne Re-Scraping
- `item_stats` wird bei jedem Lauf aus `editors` + `user_items` neu berechnet (nicht manuell editieren)
- Pro User/Redakteur darf ein Item nur einmal in `item_stats.count` gezählt werden
- Kategorie-Werte: `"game"`, `"film_series"`, `"misc"`, `"unknown"`

## Scraping Logic

### Editor-Item Extraction

Artikel-Body: `<div class="node node-news">`. Ablauf:
1. Suche `<strong>` mit Großbuchstaben-only-Text → Redakteur-Name
2. Lies nachfolgende Paragraphen bis zum nächsten Redakteur-Namen
3. Erkenne Kategorie aus inline-Texten `[FILME/SERIEN]`, `[SPIELE/BRETTSPIELE]`, `[SONSTIGES]`
4. Extrahiere `<strong>` und `<em>` innerhalb dieser Sektionen als Items

### Comment Extraction

Container: `<div class="comment" id="comment-[id]">`. Pro Kommentar:
- Username aus `<div class="submitted">`
- Text aus `<div class="content">`
- Nur ein Eintrag pro Username in `comments_raw`

### LLM Enrichment Prompt (Claude Haiku)

```
System: Du extrahierst aus einem deutschen Kommentar alle Medientitel/Spiele/Produkte,
auf die sich der User freut. Antworte ausschließlich als JSON-Array:
[{"title": "...", "category": "game|film_series|misc|unknown"}]
Leeres Array wenn nichts erkennbar.

User: <Kommentartext>
```

Prompt-Caching via `cache_control: ephemeral` auf dem System-Prompt (viele Kommentare).

## Article Discovery

1. **Known-URL seed**: Letzte bekannte URL aus `vorfreude.json` + inkrementeller Monat
2. **Search fallback**: `https://www.gamersglobal.de/suche?q=darauf+freut+sich+die+redaktion` → parse Ergebnisliste
3. Neue Artikel werden nur hinzugefügt (nie gelöscht)

## CI Integration (`.github/workflows/update.yml`)

Neuer Job `update-vorfreude`, täglich 08:00 UTC:
```yaml
- run: pip install -r scripts/requirements.txt
- run: python scripts/scrape_freude.py --no-enrich
```
Commit nur wenn `vorfreude.json` sich geändert hat (diff-check vor commit).

## Frontend (`index.html`)

Neuer Abschnitt "Vorfreude" nach bestehendem Polls-Abschnitt:
- Monats-Dropdown (basierend auf `vorfreude.json` Daten)
- Bar-Chart: Top-15 Items, Balken farbcodiert (game=blau, film_series=rot, misc=grün)
- Toggle-Buttons: Alle / Nur Redakteure / Nur User
- Tooltip on hover: Liste der Mentioners
- Link zu `data/vorfreude.csv`

## CSV Export (`data/vorfreude.csv`)

Columns: `month, item_title, category, count, editor_count, user_count`  
Wird bei jedem Lauf aus `vorfreude.json` regeneriert.

## Dependencies

Keine neuen Pip-Pakete für `--no-enrich`. Für `--enrich`:
- `anthropic` (Claude Haiku API)

## Verification

1. `python scripts/scrape_freude.py --no-enrich` → `data/vorfreude.json` existiert, enthält Mai 2026 Artikel mit Editor-Items und `comments_raw`
2. `python scripts/scrape_freude.py --enrich` → `user_items` + `item_stats` gefüllt
3. `data/vorfreude.csv` existiert mit korrekten Counts
4. `index.html` im Browser öffnen → Vorfreude-Abschnitt zeigt Bar-Chart für aktuellen Monat
5. Toggle Redakteure-only / User-only funktioniert
6. CI-Job laut `update.yml` läuft durch (dry-run lokal mit `act` oder push)
