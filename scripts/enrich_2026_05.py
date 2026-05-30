#!/usr/bin/env python3
"""One-shot: enrich 2026-05 user comments via Claude Haiku and recompute item_stats."""
import json
import os
import re
import sys
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "vorfreude.json"
MONTH = "2026-05"


def compute_stats(editors, user_items):
    stats = {}

    def add_item(title, category, mentioner):
        if title not in stats:
            stats[title] = {"count": 0, "category": category, "mentioners": []}
        if mentioner not in stats[title]["mentioners"]:
            stats[title]["mentioners"].append(mentioner)
            stats[title]["count"] += 1
        if category and category != "unknown":
            stats[title]["category"] = category

    for ed in editors:
        for item in ed.get("items", []):
            add_item(item["title"], item.get("category", "unknown"), f"editor:{ed['name']}")

    for u in user_items:
        for item in u.get("items", []):
            add_item(item["title"], item.get("category", "unknown"), f"user:{u['username']}")

    return stats


def enrich(comments, editor_items, api_key):
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    seed_lines = []
    for ed in editor_items:
        for item in ed.get("items", []):
            seed_lines.append(f"- {item['title']} ({item['category']})")
    seed_context = "\n".join(seed_lines) if seed_lines else "(no editor items)"

    system_text = (
        "You are a structured-data extractor for a German gaming website.\n"
        "Users comment on a monthly article where editors share what they are looking"
        " forward to (games, films/series, miscellaneous).\n\n"
        "Known items already mentioned by editors:\n"
        f"{seed_context}\n\n"
        "Your task: Given a user comment, extract any items the user is looking forward"
        " to. Return ONLY a JSON array of objects with keys 'title' (string) and"
        " 'category' (one of: game, film_series, misc, unknown).\n"
        "If no items are found, return an empty array [].\n"
        "Respond only with the JSON array, no other text."
    )

    results = []
    for comment in comments:
        username = comment.get("username", "")
        text = comment.get("text", "").strip()
        if len(text) < 20:
            continue
        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=512,
                system=[{"type": "text", "text": system_text, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": text}],
            )
            raw = response.content[0].text.strip()
            raw = re.sub(r'^```[a-z]*\n?|\n?```$', '', raw).strip()
            items = json.loads(raw)
            if not isinstance(items, list):
                items = []
        except Exception as exc:
            print(f"  [warn] {username}: {exc}", flush=True)
            items = []
        if items:
            print(f"  {username}: {[i['title'] for i in items]}")
            results.append({"username": username, "items": items})

    return results


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    data = json.loads(DATA_FILE.read_text())
    entry = next((e for e in data if e["month"] == MONTH), None)
    if not entry:
        print(f"Error: {MONTH} not found", file=sys.stderr)
        sys.exit(1)

    if entry.get("user_items"):
        print(f"{MONTH} already has {len(entry['user_items'])} user_items — aborting (use --force to override)")
        sys.exit(0)

    comments_raw = entry.get("comments_raw", [])
    editors = entry.get("editors", [])
    print(f"Enriching {len(comments_raw)} comments for {MONTH} …")

    user_items = enrich(comments_raw, editors, api_key)
    print(f"Extracted items from {len(user_items)} users")

    entry["user_items"] = user_items
    entry["item_stats"] = compute_stats(editors, user_items)

    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print("Done.")


if __name__ == "__main__":
    main()
