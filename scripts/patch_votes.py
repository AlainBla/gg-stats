"""
Patch vote counts for polls whose results aren't visible without JS/login.

Usage:
    python scripts/patch_votes.py <url_fragment> <votes> [<url_fragment> <votes> ...]

Example:
    python scripts/patch_votes.py \
        /news/312697/sonntagsfrage-vermisst 390 \
        /news/302382/sonntagsfrage-auf-welches-spiel-im-4-quartal 456
"""
import json
import sys
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "polls.json"


def patch(patches: list[tuple[str, int]]) -> None:
    with open(DATA_PATH, encoding="utf-8") as f:
        polls = json.load(f)

    url_map = {p["url"]: p for p in polls}
    changed = 0

    for fragment, votes in patches:
        matches = [url for url in url_map if fragment in url]
        if not matches:
            print(f"NOT FOUND: {fragment!r}")
            continue
        if len(matches) > 1:
            print(f"AMBIGUOUS {fragment!r}: {matches}")
            continue
        url = matches[0]
        old = url_map[url]["votes"]
        url_map[url]["votes"] = votes
        print(f"  {url}: {old} → {votes}")
        changed += 1

    if changed:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(polls, f, indent=2, ensure_ascii=False)
        print(f"Saved {changed} change(s) to {DATA_PATH}")
    else:
        print("No changes.")


def main() -> None:
    args = sys.argv[1:]
    if not args or len(args) % 2 != 0:
        print(__doc__)
        sys.exit(1)

    patches = [(args[i], int(args[i + 1])) for i in range(0, len(args), 2)]
    patch(patches)


if __name__ == "__main__":
    main()
