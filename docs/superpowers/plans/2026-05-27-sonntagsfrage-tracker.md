# Sonntagsfrage Active-User Tracker Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scrape GG Sonntagsfrage vote counts into a versioned JSON file and visualise participation over time as a GitHub Pages site, updated each Monday via GitHub Actions.

**Architecture:** Python scraper writes `data/polls.json` (initial full crawl + weekly 2-poll incremental); `index.html` reads JSON via `fetch()` and renders a Chart.js bar+trend chart with year-filter buttons; GitHub Actions commits updated JSON and GitHub Pages serves the static site.

**Tech Stack:** Python 3.12, requests, BeautifulSoup4, pytest; Chart.js 4 (CDN); GitHub Actions; GitHub Pages (main branch root)

---

## File Map

| Path | Purpose |
|---|---|
| `scripts/requirements.txt` | Python deps |
| `scripts/scrape.py` | Scraper: parsing + run logic |
| `tests/test_scrape.py` | Unit tests (no network) |
| `data/polls.json` | Scraped data (committed to repo) |
| `.github/workflows/update.yml` | Monday cron |
| `index.html` | Chart.js frontend |
| `.gitignore` | Ignore venv / pycache |

---

## Task 1: Project Scaffolding

**Files:**
- Create: `scripts/requirements.txt`
- Create: `data/polls.json`
- Create: `.gitignore`

- [ ] **Step 1: Create `scripts/requirements.txt`**

```
requests==2.32.3
beautifulsoup4==4.12.3
```

- [ ] **Step 2: Create `data/polls.json` (empty array)**

```json
[]
```

- [ ] **Step 3: Create `.gitignore`**

```
__pycache__/
*.pyc
.venv/
venv/
```

- [ ] **Step 4: Install deps and verify**

```bash
pip install -r scripts/requirements.txt
python -c "import requests, bs4; print('ok')"
```

Expected output: `ok`

- [ ] **Step 5: Commit**

```bash
git add scripts/requirements.txt data/polls.json .gitignore
git commit -m "chore: scaffold project dependencies and data file"
```

---

## Task 2: Scraper – Parsing Functions (TDD)

**Files:**
- Create: `scripts/scrape.py`
- Create: `tests/test_scrape.py`

### Step 1: Write failing tests for archive page parser

- [ ] Create `tests/test_scrape.py`:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import json, pytest
from scrape import parse_archive_page, parse_poll_page

ARCHIVE_HTML = """
<div class="view-content">
  <div class="views-row">
    <h3 class="title"><a href="/news/100/sonntagsfrage-foo-ergebnis">Sonntagsfrage: Foo? [Ergebnis]</a></h3>
  </div>
  <div class="views-row">
    <h3 class="title"><a href="/news/101/sonntagsfrage-bar">Sonntagsfrage: Bar?</a></h3>
  </div>
</div>
<ul class="pager"><li class="pager-next"><a href="?page=2">weiter ›</a></li></ul>
"""

ARCHIVE_HTML_LAST = """
<div class="view-content">
  <div class="views-row">
    <h3 class="title"><a href="/news/1/sonntagsfrage-old-ergebnis">Sonntagsfrage: Old? [Ergebnis]</a></h3>
  </div>
</div>
"""

POLL_HTML = """
<h1 class="title">Sonntagsfrage: Foo? [Ergebnis]<div class="node-serien-info">Teil der Exklusiv-Serie <a href="/exklusiv/sonntagsfrage">Sonntagsfrage</a></div></h1>
<div class="voll-wer-wann">
  <div class="picture">x</div>
  24. Mai 2026 - 9:00
  <span>— vor 1 Tag zuletzt aktualisiert</span>
</div>
<div class="total">
  Gesamte Stimmenzahl: 481
</div>
"""

POLL_HTML_ZERO = """
<h1 class="title">Sonntagsfrage: Baz?</h1>
<div class="voll-wer-wann">3. Januar 2016 - 9:00</div>
<div class="total">Gesamte Stimmenzahl: 0</div>
"""


def test_parse_archive_returns_polls():
    polls, has_next = parse_archive_page(ARCHIVE_HTML)
    assert len(polls) == 2
    assert polls[0]["url"] == "/news/100/sonntagsfrage-foo-ergebnis"
    assert polls[0]["title"] == "Sonntagsfrage: Foo? [Ergebnis]"
    assert polls[1]["url"] == "/news/101/sonntagsfrage-bar"


def test_parse_archive_has_next():
    _, has_next = parse_archive_page(ARCHIVE_HTML)
    assert has_next is True


def test_parse_archive_no_next():
    _, has_next = parse_archive_page(ARCHIVE_HTML_LAST)
    assert has_next is False


def test_parse_poll_votes():
    r = parse_poll_page(POLL_HTML)
    assert r["votes"] == 481


def test_parse_poll_date():
    r = parse_poll_page(POLL_HTML)
    assert r["date"] == "2026-05-24"


def test_parse_poll_date_januar():
    r = parse_poll_page(POLL_HTML_ZERO)
    assert r["date"] == "2016-01-03"


def test_parse_poll_title_strips_series_info():
    r = parse_poll_page(POLL_HTML)
    assert r["title"] == "Sonntagsfrage: Foo? [Ergebnis]"
    assert "Exklusiv-Serie" not in r["title"]


def test_parse_poll_zero_votes():
    r = parse_poll_page(POLL_HTML_ZERO)
    assert r["votes"] == 0
```

- [ ] **Step 2: Run tests — verify they all fail**

```bash
cd /home/alain/repos/gg-stats && python -m pytest tests/test_scrape.py -v 2>&1 | head -20
```

Expected: `ImportError` or `ModuleNotFoundError` (scrape.py doesn't exist yet)

- [ ] **Step 3: Create `scripts/scrape.py` with parsing functions**

```python
import json
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.gamersglobal.de"
DATA_PATH = Path(__file__).parent.parent / "data" / "polls.json"

_MONTHS_DE = {
    "Januar": 1, "Februar": 2, "März": 3, "April": 4,
    "Mai": 5, "Juni": 6, "Juli": 7, "August": 8,
    "September": 9, "Oktober": 10, "November": 11, "Dezember": 12,
}


def parse_archive_page(html: str) -> tuple[list[dict], bool]:
    """Return (polls, has_next). polls = [{"url": str, "title": str}]."""
    soup = BeautifulSoup(html, "html.parser")
    polls = []
    for h3 in soup.select("h3.title"):
        a = h3.find("a")
        if a and a.get("href"):
            polls.append({"url": a["href"], "title": a.get_text(strip=True)})
    has_next = bool(soup.select_one("li.pager-next a"))
    return polls, has_next


def parse_poll_page(html: str) -> dict:
    """Return {"title": str, "votes": int, "date": str|None}."""
    soup = BeautifulSoup(html, "html.parser")

    # Title — strip embedded series-info div
    h1 = soup.select_one("h1.title")
    title = ""
    if h1:
        for tag in h1.select(".node-serien-info"):
            tag.decompose()
        title = h1.get_text(strip=True)

    # Votes
    votes = 0
    total_div = soup.select_one("div.total")
    if total_div:
        m = re.search(r"(\d+)", total_div.get_text())
        if m:
            votes = int(m.group(1))

    # Date — "24. Mai 2026 - 9:00" in div.voll-wer-wann
    date = None
    wer_wann = soup.select_one("div.voll-wer-wann")
    if wer_wann:
        text = wer_wann.get_text(" ", strip=True)
        m = re.search(r"(\d{1,2})\.\s+(\w+)\s+(\d{4})", text)
        if m:
            day, month_str, year = int(m.group(1)), m.group(2), int(m.group(3))
            month = _MONTHS_DE.get(month_str, 0)
            if month:
                date = f"{year:04d}-{month:02d}-{day:02d}"

    return {"title": title, "votes": votes, "date": date}
```

- [ ] **Step 4: Run tests — verify parsing tests pass**

```bash
cd /home/alain/repos/gg-stats && python -m pytest tests/test_scrape.py -v -k "parse"
```

Expected: all 8 `parse_*` tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/scrape.py tests/test_scrape.py
git commit -m "feat: add archive and poll page parsers with tests"
```

---

## Task 3: Scraper – Run Logic (TDD)

**Files:**
- Modify: `scripts/scrape.py` (add `fetch_html`, `run_initial`, `run_incremental`, `main`)
- Modify: `tests/test_scrape.py` (add run logic tests)

- [ ] **Step 1: Add run-logic tests to `tests/test_scrape.py`**

Append to the existing file:

```python
# ── run logic tests ────────────────────────────────────────────────────────

from scrape import run_incremental

ARCHIVE_BOTH_FINAL = """
<div class="view-content">
  <div class="views-row">
    <h3 class="title"><a href="/news/101/sonntagsfrage-bar-ergebnis">Sonntagsfrage: Bar? [Ergebnis]</a></h3>
  </div>
  <div class="views-row">
    <h3 class="title"><a href="/news/100/sonntagsfrage-foo-ergebnis">Sonntagsfrage: Foo? [Ergebnis]</a></h3>
  </div>
</div>
"""

ARCHIVE_ONE_PENDING = """
<div class="view-content">
  <div class="views-row">
    <h3 class="title"><a href="/news/102/sonntagsfrage-new">Sonntagsfrage: New?</a></h3>
  </div>
  <div class="views-row">
    <h3 class="title"><a href="/news/101/sonntagsfrage-bar-ergebnis">Sonntagsfrage: Bar? [Ergebnis]</a></h3>
  </div>
</div>
"""

POLL_HTML_NEW = """
<h1 class="title">Sonntagsfrage: New?</h1>
<div class="voll-wer-wann">1. Juni 2026 - 9:00</div>
<div class="total">Gesamte Stimmenzahl: 350</div>
"""

POLL_HTML_BAR_FINAL = """
<h1 class="title">Sonntagsfrage: Bar? [Ergebnis]</h1>
<div class="voll-wer-wann">25. Mai 2026 - 9:00</div>
<div class="total">Gesamte Stimmenzahl: 400</div>
"""


def _make_db(tmp_path, polls):
    p = tmp_path / "polls.json"
    p.write_text(json.dumps(polls, ensure_ascii=False))
    return str(p)


def test_incremental_skips_both_final(tmp_path, monkeypatch):
    """If both top-2 are already [Ergebnis] and known, no network calls beyond archive."""
    polls = [
        {"url": "/news/100/sonntagsfrage-foo-ergebnis", "title": "Sonntagsfrage: Foo? [Ergebnis]", "votes": 481, "date": "2026-05-17"},
        {"url": "/news/101/sonntagsfrage-bar-ergebnis", "title": "Sonntagsfrage: Bar? [Ergebnis]", "votes": 400, "date": "2026-05-24"},
    ]
    data_path = _make_db(tmp_path, polls)
    calls = []

    def mock_fetch(url):
        calls.append(url)
        return ARCHIVE_BOTH_FINAL

    import scrape
    monkeypatch.setattr(scrape, "fetch_html", mock_fetch)
    changed = run_incremental(data_path)

    assert changed is False
    assert len(calls) == 1  # only archive page, no detail fetches


def test_incremental_adds_new_poll(tmp_path, monkeypatch):
    """New poll (not in DB yet) gets fetched and added."""
    polls = [
        {"url": "/news/101/sonntagsfrage-bar-ergebnis", "title": "Sonntagsfrage: Bar? [Ergebnis]", "votes": 400, "date": "2026-05-24"},
    ]
    data_path = _make_db(tmp_path, polls)

    def mock_fetch(url):
        if "sonntagsfrage?page" in url:
            return ARCHIVE_ONE_PENDING
        if "/news/102/" in url:
            return POLL_HTML_NEW
        return POLL_HTML_BAR_FINAL

    import scrape
    monkeypatch.setattr(scrape, "fetch_html", mock_fetch)
    changed = run_incremental(data_path)

    assert changed is True
    result = json.loads(Path(data_path).read_text())
    urls = [p["url"] for p in result]
    assert "/news/102/sonntagsfrage-new" in urls
    new = next(p for p in result if p["url"] == "/news/102/sonntagsfrage-new")
    assert new["votes"] == 350
    assert new["date"] == "2026-06-01"


def test_incremental_updates_pending_poll(tmp_path, monkeypatch):
    """Poll in DB without [Ergebnis] gets votes + title refreshed."""
    polls = [
        {"url": "/news/102/sonntagsfrage-new", "title": "Sonntagsfrage: New?", "votes": 200, "date": "2026-06-01"},
        {"url": "/news/101/sonntagsfrage-bar-ergebnis", "title": "Sonntagsfrage: Bar? [Ergebnis]", "votes": 400, "date": "2026-05-24"},
    ]
    data_path = _make_db(tmp_path, polls)

    ARCHIVE_NEW_NOW_FINAL = """
    <div class="view-content">
      <div class="views-row">
        <h3 class="title"><a href="/news/102/sonntagsfrage-new-ergebnis">Sonntagsfrage: New? [Ergebnis]</a></h3>
      </div>
      <div class="views-row">
        <h3 class="title"><a href="/news/101/sonntagsfrage-bar-ergebnis">Sonntagsfrage: Bar? [Ergebnis]</a></h3>
      </div>
    </div>
    """
    POLL_HTML_NEW_FINAL = """
    <h1 class="title">Sonntagsfrage: New? [Ergebnis]</h1>
    <div class="voll-wer-wann">1. Juni 2026 - 9:00</div>
    <div class="total">Gesamte Stimmenzahl: 350</div>
    """

    def mock_fetch(url):
        if "sonntagsfrage?page" in url:
            return ARCHIVE_NEW_NOW_FINAL
        return POLL_HTML_NEW_FINAL

    import scrape
    monkeypatch.setattr(scrape, "fetch_html", mock_fetch)
    changed = run_incremental(data_path)

    assert changed is True
    result = json.loads(Path(data_path).read_text())
    updated = next(p for p in result if "new" in p["url"])
    assert updated["votes"] == 350
    assert "[Ergebnis]" in updated["title"]
```

- [ ] **Step 2: Run new tests — verify they fail**

```bash
cd /home/alain/repos/gg-stats && python -m pytest tests/test_scrape.py -v -k "incremental" 2>&1 | head -15
```

Expected: `ImportError: cannot import name 'run_incremental'`

- [ ] **Step 3: Add `fetch_html`, `run_incremental`, `run_initial`, `main` to `scripts/scrape.py`**

Append after the existing `parse_poll_page` function:

```python

def fetch_html(url: str) -> str:
    time.sleep(0.5)
    r = requests.get(
        BASE_URL + url,
        headers={"User-Agent": "Mozilla/5.0 (gg-stats-bot/1.0)"},
        timeout=30,
    )
    r.raise_for_status()
    return r.text


def run_initial(data_path: str = str(DATA_PATH)) -> list[dict]:
    """Full crawl — scrapes every page of the archive."""
    all_polls: list[dict] = []
    page = 0
    while True:
        html = fetch_html(f"/exklusiv/sonntagsfrage?page={page}")
        entries, has_next = parse_archive_page(html)
        for e in entries:
            detail = parse_poll_page(fetch_html(e["url"]))
            all_polls.append({
                "date": detail["date"],
                "title": detail["title"],
                "votes": detail["votes"],
                "url": e["url"],
            })
            print(f"  scraped {e['url']} ({detail['votes']} votes)", flush=True)
        print(f"page {page} done ({len(entries)} polls)", flush=True)
        if not has_next:
            break
        page += 1

    all_polls.sort(key=lambda x: x["date"] or "")
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(all_polls, f, indent=2, ensure_ascii=False)
    print(f"wrote {len(all_polls)} polls to {data_path}")
    return all_polls


def run_incremental(data_path: str = str(DATA_PATH)) -> bool:
    """Check the 2 most recent polls; update votes/title if not yet [Ergebnis]."""
    with open(data_path, encoding="utf-8") as f:
        polls: list[dict] = json.load(f)

    existing = {p["url"]: p for p in polls}

    html = fetch_html("/exklusiv/sonntagsfrage?page=0")
    latest, _ = parse_archive_page(html)
    candidates = latest[:2]

    changed = False
    for c in candidates:
        if "[Ergebnis]" in c["title"] and c["url"] in existing:
            continue  # already final and known — skip

        detail = parse_poll_page(fetch_html(c["url"]))

        if c["url"] in existing:
            p = existing[c["url"]]
            p["title"] = detail["title"]
            p["votes"] = detail["votes"]
            changed = True
        else:
            polls.append({
                "date": detail["date"],
                "title": detail["title"],
                "votes": detail["votes"],
                "url": c["url"],
            })
            polls.sort(key=lambda x: x["date"] or "")
            changed = True

    if changed:
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(polls, f, indent=2, ensure_ascii=False)

    return changed


def main() -> None:
    with open(DATA_PATH, encoding="utf-8") as f:
        existing = json.load(f)

    if not existing:
        print("No data found — running initial full crawl …")
        run_initial()
    else:
        print("Existing data found — running incremental update …")
        changed = run_incremental()
        print("Changed:" if changed else "No changes.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run all tests**

```bash
cd /home/alain/repos/gg-stats && python -m pytest tests/test_scrape.py -v
```

Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/scrape.py tests/test_scrape.py
git commit -m "feat: add scraper run logic (initial + incremental) with tests"
```

---

## Task 4: GitHub Actions Workflow

**Files:**
- Create: `.github/workflows/update.yml`

- [ ] **Step 1: Create `.github/workflows/update.yml`**

```yaml
name: Update Sonntagsfrage Data

on:
  schedule:
    - cron: '5 9 * * 1'  # Montag 09:05 UTC (Umfragen schließen 09:00)
  workflow_dispatch:       # Manuell auslösbar für den Initiallauf

jobs:
  update:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip
          cache-dependency-path: scripts/requirements.txt

      - name: Install dependencies
        run: pip install -r scripts/requirements.txt

      - name: Run scraper
        run: python scripts/scrape.py

      - name: Commit updated data
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data/polls.json
          git diff --cached --exit-code && echo "No changes." || \
            git commit -m "data: update Sonntagsfrage polls [skip ci]" && git push
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/update.yml
git commit -m "ci: add Monday 09:05 UTC scraper workflow"
```

---

## Task 5: Frontend

**Files:**
- Create: `index.html`

- [ ] **Step 1: Create `index.html`**

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GG Sonntagsfrage – Aktive Nutzer</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; }
    body {
      font-family: system-ui, sans-serif;
      background: #111;
      color: #eee;
      margin: 0;
      padding: 1.5rem;
    }
    h1 { font-size: 1.2rem; margin-bottom: 1rem; }
    #year-filter { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
    .year-btn {
      padding: 0.3rem 0.8rem;
      border: 1px solid #555;
      border-radius: 4px;
      background: #222;
      color: #ccc;
      cursor: pointer;
      font-size: 0.85rem;
    }
    .year-btn.active {
      background: #e8a000;
      border-color: #e8a000;
      color: #111;
      font-weight: bold;
    }
    #chart-container { position: relative; max-width: 960px; }
    canvas { width: 100% !important; }
  </style>
</head>
<body>
  <h1>GamersGlobal Sonntagsfrage – Abstimmungsbeteiligung</h1>
  <div id="year-filter"></div>
  <div id="chart-container">
    <canvas id="chart"></canvas>
  </div>

  <script>
    const WINDOW = 4;

    function rollingAvg(values, w) {
      return values.map((_, i) => {
        const slice = values.slice(Math.max(0, i - w + 1), i + 1);
        return slice.reduce((a, b) => a + b, 0) / slice.length;
      });
    }

    function formatDate(iso) {
      const [y, m, d] = iso.split('-');
      return `${d}.${m}.${y}`;
    }

    let chartInstance = null;

    function renderChart(polls, year) {
      const currentYear = new Date().getFullYear().toString();
      const filtered = year === 'YtD'
        ? polls.filter(p => p.date && p.date.startsWith(currentYear))
        : polls.filter(p => p.date && p.date.startsWith(year));

      const labels = filtered.map(p => formatDate(p.date));
      const votes  = filtered.map(p => p.votes);
      const trend  = rollingAvg(votes, WINDOW);

      const data = {
        labels,
        datasets: [
          {
            type: 'bar',
            label: 'Stimmen',
            data: votes,
            backgroundColor: 'rgba(232,160,0,0.55)',
            borderColor: 'rgba(232,160,0,0.9)',
            borderWidth: 1,
            order: 2,
          },
          {
            type: 'line',
            label: `${WINDOW}-Wochen-Schnitt`,
            data: trend,
            borderColor: '#4fc3f7',
            backgroundColor: 'transparent',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.3,
            order: 1,
          },
        ],
      };

      const options = {
        responsive: true,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { labels: { color: '#ccc' } },
          tooltip: {
            callbacks: {
              title: (items) => {
                const idx = items[0].dataIndex;
                return `${filtered[idx].date} – ${filtered[idx].title}`;
              },
            },
          },
        },
        scales: {
          x: {
            ticks: { color: '#999', maxRotation: 45, autoSkip: true, maxTicksLimit: 20 },
            grid: { color: '#333' },
          },
          y: {
            ticks: { color: '#999' },
            grid: { color: '#333' },
            title: { display: true, text: 'Abstimmungen', color: '#999' },
          },
        },
      };

      if (chartInstance) chartInstance.destroy();
      chartInstance = new Chart(document.getElementById('chart'), { type: 'bar', data, options });
    }

    async function main() {
      const polls = await fetch('data/polls.json').then(r => r.json());

      const years = [...new Set(
        polls.filter(p => p.date).map(p => p.date.slice(0, 4))
      )].sort();

      const currentYear = new Date().getFullYear().toString();
      let activeYear = years.includes(currentYear) ? 'YtD' : years[years.length - 1];

      const container = document.getElementById('year-filter');
      ['YtD', ...years].forEach(y => {
        const btn = document.createElement('button');
        btn.className = 'year-btn' + (y === activeYear ? ' active' : '');
        btn.textContent = y;
        btn.addEventListener('click', () => {
          document.querySelectorAll('.year-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          activeYear = y;
          renderChart(polls, activeYear);
        });
        container.appendChild(btn);
      });

      renderChart(polls, activeYear);
    }

    main();
  </script>
</body>
</html>
```

- [ ] **Step 2: Verify JS logic — open in browser**

Start a local server and open the page:

```bash
cd /home/alain/repos/gg-stats && python -m http.server 8080
```

Open http://localhost:8080 — should show "Abstimmungsbeteiligung" heading and year buttons (no chart data yet since `data/polls.json` is empty `[]`). No console errors.

- [ ] **Step 3: Test with sample data**

Temporarily write sample data to verify the chart renders:

```bash
cat > /tmp/test_polls.json << 'EOF'
[
  {"date":"2026-01-05","title":"Sonntagsfrage: Test A? [Ergebnis]","votes":420,"url":"/news/1/a"},
  {"date":"2026-01-12","title":"Sonntagsfrage: Test B? [Ergebnis]","votes":380,"url":"/news/2/b"},
  {"date":"2026-01-19","title":"Sonntagsfrage: Test C? [Ergebnis]","votes":510,"url":"/news/3/c"},
  {"date":"2026-01-26","title":"Sonntagsfrage: Test D? [Ergebnis]","votes":460,"url":"/news/4/d"},
  {"date":"2026-02-02","title":"Sonntagsfrage: Test E? [Ergebnis]","votes":490,"url":"/news/5/e"}
]
EOF
cp /tmp/test_polls.json data/polls.json
```

Reload http://localhost:8080 — should show bars + trend line for 2026 (YtD active), year buttons "YtD" and "2026". Hover over a bar — tooltip shows title.

- [ ] **Step 4: Restore empty data**

```bash
echo '[]' > data/polls.json
```

- [ ] **Step 5: Commit**

```bash
git add index.html data/polls.json
git commit -m "feat: add Chart.js frontend with year filter and rolling average"
```

---

## Task 6: GitHub Pages + Initial Data

**Files:** No new files — configure repo settings + run scraper.

- [ ] **Step 1: Enable GitHub Pages**

In GitHub repo settings: Settings → Pages → Source: `Deploy from a branch` → Branch: `main`, folder: `/ (root)` → Save.

- [ ] **Step 2: Push everything to GitHub**

```bash
git push -u origin main
```

- [ ] **Step 3: Run initial scrape locally**

This will take ~10–15 minutes (500+ HTTP requests at 0.5s delay):

```bash
cd /home/alain/repos/gg-stats && python scripts/scrape.py
```

Expected: console output showing each scraped URL, final message `wrote NNN polls to data/polls.json`

- [ ] **Step 4: Verify data**

```bash
python -c "
import json
polls = json.load(open('data/polls.json'))
print(f'{len(polls)} polls')
print('oldest:', polls[0]['date'], polls[0]['title'][:60])
print('newest:', polls[-1]['date'], polls[-1]['title'][:60])
print('sample votes:', polls[-1]['votes'])
"
```

Expected: 450+ polls, oldest ~2013-2015, newest current week.

- [ ] **Step 5: Test frontend with real data**

```bash
python -m http.server 8080
```

Open http://localhost:8080 — chart should display correctly with all years available.

- [ ] **Step 6: Commit and push data**

```bash
git add data/polls.json
git commit -m "data: initial full scrape of Sonntagsfrage archive"
git push
```

GitHub Pages will serve the site at `https://alainbla.github.io/gg-stats/` within ~2 minutes.

---

## Self-Review Checklist

**Spec coverage:**
- ✅ Full archive scrape (initial run)
- ✅ Incremental: only last 2 polls checked
- ✅ `[Ergebnis]` = final, never re-scraped
- ✅ YtD default, year buttons for history
- ✅ Bar + 4-week rolling average line
- ✅ Monday 09:05 UTC cron
- ✅ GitHub Pages deployment
- ✅ `data/polls.json` committed to repo

**Placeholders:** None.

**Type consistency:** `parse_archive_page` → `list[dict]` with `url`/`title` keys. `parse_poll_page` → `dict` with `title`/`votes`/`date`. `run_incremental` → `bool`. All consistent across tasks.
