#!/usr/bin/env python3
"""Summarise match results: rates by section, category, and match type.

Usage:
    python scripts/match_summary.py --input match_results.json
"""

import argparse
import json
from collections import Counter, defaultdict


def main():
    parser = argparse.ArgumentParser(description="Summarise external match results")
    parser.add_argument("--input", required=True, help="Path to match results JSON")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    results = data if isinstance(data, list) else data.get("results", data.get("matches", []))

    total = len(results)
    by_type = Counter()
    by_gap = Counter()
    by_section = defaultdict(Counter)
    by_theme = defaultdict(Counter)

    for r in results:
        mt = r.get("match_type", "UNKNOWN")
        by_type[mt] += 1
        if r.get("gap_type"):
            by_gap[r["gap_type"]] += 1

        section = r.get("section", r.get("country", "UNKNOWN"))
        theme = r.get("theme_key", "UNKNOWN")
        by_section[section][mt] += 1
        by_theme[theme][mt] += 1

    matched = by_type.get("EXACT", 0) + by_type.get("PROBABLE", 0)
    match_rate = matched / total * 100 if total else 0

    print(f"=== MATCH SUMMARY ===\n")
    print(f"Total entries: {total}")
    print(f"Match rate: {matched}/{total} ({match_rate:.1f}%)\n")

    print(f"--- By Match Type ---")
    for mt, count in by_type.most_common():
        print(f"  {mt}: {count}")

    if by_gap:
        print(f"\n--- Gap Types (NO_MATCH breakdown) ---")
        for gt, count in by_gap.most_common():
            print(f"  {gt}: {count}")

    print(f"\n--- By Category (match rate) ---")
    for theme in sorted(by_theme.keys()):
        counts = by_theme[theme]
        t = sum(counts.values())
        m = counts.get("EXACT", 0) + counts.get("PROBABLE", 0)
        print(f"  {theme}: {m}/{t} ({m/t*100:.0f}%)")


if __name__ == "__main__":
    main()
