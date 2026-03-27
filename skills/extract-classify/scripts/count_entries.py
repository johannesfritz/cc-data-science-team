#!/usr/bin/env python3
"""Report extraction statistics: entries by theme, by country, named/unnamed counts.

Usage:
    python scripts/count_entries.py --input extractions.json

Prints a summary table to stdout.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict


def main():
    parser = argparse.ArgumentParser(description="Count extraction entries")
    parser.add_argument("--input", required=True, help="Path to extractions.json")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    total_entries = 0
    by_theme = Counter()
    by_country = Counter()
    by_strength = Counter()
    total_named = 0
    total_unnamed = 0
    ct_pairs = defaultdict(lambda: {"named": set(), "unnamed": 0, "entries": 0})

    for theme in data.get("themes", []):
        tk = theme["theme_key"]
        for country in theme.get("countries", []):
            cn = country["country"]
            for entry in country.get("entries", []):
                total_entries += 1
                by_theme[tk] += 1
                by_country[cn] += 1
                by_strength[entry.get("match_strength", "UNKNOWN")] += 1

                ct_key = f"{cn}__{tk}"
                ct_pairs[ct_key]["entries"] += 1

                for act in entry.get("state_acts", []):
                    if act["type"] == "named":
                        total_named += 1
                        ct_pairs[ct_key]["named"].add(act["name"])
                    else:
                        total_unnamed += 1
                        ct_pairs[ct_key]["unnamed"] += 1

    # Deduplicated named count
    unique_named = sum(len(v["named"]) for v in ct_pairs.values())

    print(f"=== EXTRACTION SUMMARY ===\n")
    print(f"Total entries: {total_entries}")
    print(f"Country-theme pairs: {len(ct_pairs)}")
    print(f"State acts: {unique_named} named (deduplicated) + {total_unnamed} unnamed = {unique_named + total_unnamed} total\n")

    print(f"--- By Theme ---")
    for theme, count in by_theme.most_common():
        print(f"  {theme}: {count}")

    print(f"\n--- By Country (top 15) ---")
    for country, count in by_country.most_common(15):
        print(f"  {country}: {count}")

    print(f"\n--- By Match Strength ---")
    for strength, count in by_strength.most_common():
        print(f"  {strength}: {count}")


if __name__ == "__main__":
    main()
