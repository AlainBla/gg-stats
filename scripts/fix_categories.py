#!/usr/bin/env python3
"""Apply overrides from data/overrides.json to vorfreude.json and recompute item_stats.

overrides.json schema:
  aliases:    { canonical_title: [variant, ...] }  — merge variants into canonical
  categories: { title: category }                  — fix wrong category

Auto-detection:
  Titles that differ only in separator style (` - ` / ` – ` / `-\xa0` / `: `) are
  automatically merged. Colon form preferred as canonical; falls back to plain hyphen.
  Explicit aliases in overrides.json take precedence over auto-detected ones.

Run:
    python3 scripts/fix_categories.py
"""
import json
import re
from pathlib import Path

DATA_FILE      = Path("data/vorfreude.json")
OVERRIDES_FILE = Path("data/overrides.json")

# Matches separator variants: " - ", " – ", " -<NBSP>", " –<NBSP>", ": "
_SEP_RE    = re.compile(r'\s*[-–—]\xa0?\s*|\s*:\s*')
# Detects whether a title actually contains a separator (guards against pure case variants)
_HAS_SEP   = re.compile(r'\s[-–—]\xa0?|:\s|\s[-–—]$')


def _sep_key(title: str) -> str:
    """Normalize separator variants to '::' for grouping (case-insensitive)."""
    return _SEP_RE.sub('::', title.strip()).lower()


def _pick_canonical(titles: list[str]) -> str:
    """Among separator-variant titles, prefer the colon form; fall back to plain hyphen."""
    colon = [t for t in titles if re.search(r':\s', t) and '\xa0' not in t]
    if colon:
        return sorted(colon)[0]
    colon_nbsp = [t for t in titles if re.search(r':\s', t)]
    if colon_nbsp:
        return sorted(colon_nbsp)[0]
    no_nbsp = [t for t in titles if '\xa0' not in t and ' - ' in t]
    if no_nbsp:
        return sorted(no_nbsp)[0]
    return sorted(titles)[0]


def build_auto_aliases(data: list) -> dict:
    """Scan all editors + user_items, return {variant: canonical} for separator duplicates."""
    all_titles: set[str] = set()
    for entry in data:
        for ed in entry.get("editors", []):
            for item in ed["items"]:
                all_titles.add(item["title"])
        for u in entry.get("user_items", []):
            for item in u["items"]:
                all_titles.add(item["title"])

    groups: dict[str, list[str]] = {}
    for t in all_titles:
        groups.setdefault(_sep_key(t), []).append(t)

    auto: dict[str, str] = {}
    for titles in groups.values():
        # Only auto-merge when at least one title contains an actual separator
        # (prevents merging pure case-variants like BioShock / Bioshock)
        if len(titles) > 1 and any(_HAS_SEP.search(t) for t in titles):
            canonical = _pick_canonical(titles)
            for t in titles:
                if t != canonical:
                    auto[t] = canonical
    return auto


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


def strip_staffel_parens(entry) -> bool:
    """Convert 'Title (Staffel N)' → 'Title Staffel N' in editors + user_items."""
    changed = False
    pattern = re.compile(r'\s*\(Staffel\s+(\d+)\)')
    for src in [*entry.get("editors", []), *[{"items": u["items"]} for u in entry.get("user_items", [])]]:
        for item in src["items"]:
            clean = pattern.sub(r' Staffel \1', item["title"]).strip()
            if clean != item["title"]:
                item["title"] = clean
                changed = True
    return changed


def strip_trailing_commas(entry) -> bool:
    """Remove trailing commas from item titles in editors + user_items."""
    changed = False
    for src in [*entry.get("editors", []), *[{"items": u["items"]} for u in entry.get("user_items", [])]]:
        for item in src["items"]:
            clean = item["title"].rstrip(",").rstrip()
            if clean != item["title"]:
                item["title"] = clean
                changed = True
    return changed


def apply_aliases(entry, alias_map):
    """Rename variant titles to canonical in editors + user_items. Returns True if changed."""
    changed = False
    for src in [*entry.get("editors", []), *[{"items": u["items"]} for u in entry.get("user_items", [])]]:
        for item in src["items"]:
            if item["title"] in alias_map:
                item["title"] = alias_map[item["title"]]
                changed = True
    return changed


def apply_categories(entry, cat_fixes):
    """Fix category for named titles in editors + user_items. Returns True if changed."""
    changed = False
    for src in [*entry.get("editors", []), *[{"items": u["items"]} for u in entry.get("user_items", [])]]:
        for item in src["items"]:
            correct = cat_fixes.get(item["title"])
            if correct and item["category"] != correct:
                item["category"] = correct
                changed = True
    return changed


def main():
    overrides   = json.loads(OVERRIDES_FILE.read_text())
    # Explicit aliases from overrides.json
    alias_map: dict[str, str] = {}
    for canonical, variants in overrides.get("aliases", {}).items():
        for v in variants:
            alias_map[v] = canonical
    cat_fixes = overrides.get("categories", {})

    data = json.loads(DATA_FILE.read_text())

    # Auto-detect separator variants; explicit overrides take precedence
    auto = build_auto_aliases(data)
    merged_count = 0
    for variant, canonical in auto.items():
        if variant not in alias_map:
            alias_map[variant] = canonical
            merged_count += 1

    if merged_count:
        print(f"  Auto-detected {merged_count} separator variant(s):")
        shown = {v: c for v, c in auto.items() if v not in overrides.get("aliases", {}).get(auto[v], [])}
        for v, c in sorted(shown.items()):
            print(f"    {repr(v)} → {repr(c)}")

    months_changed = 0
    for entry in data:
        changed  = strip_trailing_commas(entry)
        changed |= apply_aliases(entry, alias_map)
        changed |= strip_staffel_parens(entry)
        changed |= apply_categories(entry, cat_fixes)
        if changed:
            entry["item_stats"] = compute_stats(entry["editors"], entry.get("user_items", []))
            months_changed += 1
            print(f"  {entry['month']}: recomputed item_stats")

    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Done. {months_changed} month(s) updated.")


if __name__ == "__main__":
    main()
