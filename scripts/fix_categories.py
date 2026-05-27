#!/usr/bin/env python3
"""Reclassify item categories in vorfreude.json and recompute item_stats.

Add entries to FIXES below, then run:
    python3 scripts/fix_categories.py
"""
import json
import re
from pathlib import Path

DATA = Path("data/vorfreude.json")

# title → correct category ("game", "film_series", "misc", "unknown")
FIXES = {
    "Pragmata": "game",
}


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


def main():
    data = json.loads(DATA.read_text())
    total = 0

    for entry in data:
        changed = False
        sources = [
            *[{"items": ed["items"]} for ed in entry.get("editors", [])],
            *[{"items": u["items"]} for u in entry.get("user_items", [])],
        ]
        for src in sources:
            for item in src["items"]:
                correct = FIXES.get(item["title"])
                if correct and item["category"] != correct:
                    item["category"] = correct
                    total += 1
                    changed = True

        if changed:
            entry["item_stats"] = compute_stats(entry["editors"], entry.get("user_items", []))
            print(f"  {entry['month']}: recomputed item_stats")

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Done. {total} item(s) reclassified.")


if __name__ == "__main__":
    main()
