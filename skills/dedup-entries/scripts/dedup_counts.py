#!/usr/bin/env python3
"""Recalculate entry counts after deduplication.

Usage:
    python scripts/dedup_counts.py --before extractions.json --after extractions_deduped.json

Compares before/after and reports what changed.
"""

import argparse
import json
from collections import defaultdict


def count_file(path):
    with open(path) as f:
        data = json.load(f)

    total = 0
    by_ct = defaultdict(int)
    named_acts = defaultdict(set)
    unnamed_acts = defaultdict(int)

    for theme in data.get("themes", []):
        tk = theme["theme_key"]
        for country in theme.get("countries", []):
            cn = country["country"]
            ct = f"{cn}__{tk}"
            for entry in country.get("entries", []):
                total += 1
                by_ct[ct] += 1
                for act in entry.get("state_acts", []):
                    if act["type"] == "named":
                        named_acts[ct].add(act["name"])
                    else:
                        unnamed_acts[ct] += 1

    return {
        "total": total,
        "ct_pairs": len(by_ct),
        "by_ct": dict(by_ct),
        "named": {k: len(v) for k, v in named_acts.items()},
        "unnamed": dict(unnamed_acts),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", required=True)
    parser.add_argument("--after", required=True)
    args = parser.parse_args()

    before = count_file(args.before)
    after = count_file(args.after)

    print(f"=== DEDUPLICATION REPORT ===\n")
    print(f"Entries: {before['total']} → {after['total']} (removed {before['total'] - after['total']})")
    print(f"CT pairs: {before['ct_pairs']} → {after['ct_pairs']}\n")

    # Find changed CT pairs
    changed = []
    for ct in sorted(set(list(before["by_ct"].keys()) + list(after["by_ct"].keys()))):
        b = before["by_ct"].get(ct, 0)
        a = after["by_ct"].get(ct, 0)
        if b != a:
            changed.append((ct, b, a))

    if changed:
        print(f"--- Changed CT Pairs ---")
        for ct, b, a in changed:
            print(f"  {ct}: {b} → {a}")
    else:
        print("No changes to CT pair counts.")


if __name__ == "__main__":
    main()
