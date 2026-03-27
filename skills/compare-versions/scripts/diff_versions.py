#!/usr/bin/env python3
"""Diff two extraction JSONs to find NEW, REMOVED, CHANGED, UNCHANGED entries.

Usage:
    python scripts/diff_versions.py --v1 v1_extractions.json --v2 v2_extractions.json [--output diff_results.json]

Produces a JSON diff table and prints summary statistics.
"""

import argparse
import hashlib
import json
import re
import sys
from collections import Counter


def normalise_key(section: str, theme_key: str, description: str) -> str:
    """Build a normalisation key for entry alignment."""
    section_norm = re.sub(r"\s+", " ", section.upper().strip())
    desc_norm = re.sub(r"\s+", " ", description.strip().lower())[:100]
    raw = f"{section_norm}|{theme_key}|{desc_norm}"
    return hashlib.md5(raw.encode()).hexdigest()


def extract_entries(data: dict) -> dict[str, dict]:
    """Extract all entries keyed by normalisation hash."""
    entries = {}
    for theme in data.get("themes", []):
        tk = theme["theme_key"]
        for country in theme.get("countries", []):
            section = country.get("country", "")
            for entry in country.get("entries", []):
                desc = entry.get("description", entry.get("barrier_description", ""))
                key = normalise_key(section, tk, desc)
                entries[key] = {
                    "entry_id": entry.get("entry_id", ""),
                    "section": section,
                    "theme_key": tk,
                    "description": desc,
                    "exact_quote": entry.get("exact_quote", "")[:200],
                    "match_strength": entry.get("match_strength", ""),
                }
    return entries


def main():
    parser = argparse.ArgumentParser(description="Diff two extraction versions")
    parser.add_argument("--v1", required=True, help="Earlier version JSON")
    parser.add_argument("--v2", required=True, help="Later version JSON")
    parser.add_argument("--output", default="diff_results.json", help="Output path")
    args = parser.parse_args()

    with open(args.v1) as f:
        data_v1 = json.load(f)
    with open(args.v2) as f:
        data_v2 = json.load(f)

    entries_v1 = extract_entries(data_v1)
    entries_v2 = extract_entries(data_v2)

    keys_v1 = set(entries_v1.keys())
    keys_v2 = set(entries_v2.keys())

    results = []

    # NEW entries (in v2 only)
    for key in sorted(keys_v2 - keys_v1):
        e = entries_v2[key]
        results.append({**e, "status": "NEW", "version": "v2"})

    # REMOVED entries (in v1 only)
    for key in sorted(keys_v1 - keys_v2):
        e = entries_v1[key]
        results.append({**e, "status": "REMOVED", "version": "v1"})

    # Common keys: CHANGED or UNCHANGED
    for key in sorted(keys_v1 & keys_v2):
        e1 = entries_v1[key]
        e2 = entries_v2[key]
        if e1["exact_quote"] == e2["exact_quote"] and e1["match_strength"] == e2["match_strength"]:
            results.append({**e2, "status": "UNCHANGED", "version": "both"})
        else:
            results.append({
                **e2,
                "status": "CHANGED",
                "version": "both",
                "v1_quote": e1["exact_quote"],
                "v1_strength": e1["match_strength"],
            })

    # Summary
    status_counts = Counter(r["status"] for r in results)
    by_theme = {}
    for r in results:
        tk = r["theme_key"]
        if tk not in by_theme:
            by_theme[tk] = Counter()
        by_theme[tk][r["status"]] += 1

    output = {
        "summary": {
            "v1_entries": len(entries_v1),
            "v2_entries": len(entries_v2),
            "new": status_counts.get("NEW", 0),
            "removed": status_counts.get("REMOVED", 0),
            "changed": status_counts.get("CHANGED", 0),
            "unchanged": status_counts.get("UNCHANGED", 0),
        },
        "by_theme": {tk: dict(counts) for tk, counts in sorted(by_theme.items())},
        "entries": results,
    }

    with open(args.output, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Print summary
    s = output["summary"]
    print(f"=== VERSION DIFF ===\n")
    print(f"v1: {s['v1_entries']} entries")
    print(f"v2: {s['v2_entries']} entries")
    print(f"Change: {s['v2_entries'] - s['v1_entries']:+d}\n")
    print(f"NEW:       {s['new']}")
    print(f"REMOVED:   {s['removed']}")
    print(f"CHANGED:   {s['changed']}")
    print(f"UNCHANGED: {s['unchanged']}")

    if by_theme:
        print(f"\n--- By Category ---")
        for tk, counts in sorted(by_theme.items()):
            parts = [f"{status}={count}" for status, count in counts.most_common()]
            print(f"  {tk}: {', '.join(parts)}")


if __name__ == "__main__":
    main()
