#!/usr/bin/env python3
"""Apply overrides from data/overrides.json to vorfreude.json and recompute item_stats.

overrides.json schema:
  aliases:    { canonical_title: [variant, ...] }  — merge variants into canonical
  categories: { title: category }                  — fix wrong category

Run:
    python3 scripts/fix_categories.py
"""
import json
import re
from pathlib import Path

DATA_FILE      = Path("data/vorfreude.json")
OVERRIDES_FILE = Path("data/overrides.json")


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
    alias_map   = {}  # variant → canonical
    for canonical, variants in overrides.get("aliases", {}).items():
        for v in variants:
            alias_map[v] = canonical
    cat_fixes = overrides.get("categories", {})

    data = json.loads(DATA_FILE.read_text())
    months_changed = 0

    for entry in data:
        changed  = apply_aliases(entry, alias_map)
        changed |= apply_categories(entry, cat_fixes)
        if changed:
            entry["item_stats"] = compute_stats(entry["editors"], entry.get("user_items", []))
            months_changed += 1
            print(f"  {entry['month']}: recomputed item_stats")

    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Done. {months_changed} month(s) updated.")


if __name__ == "__main__":
    main()
