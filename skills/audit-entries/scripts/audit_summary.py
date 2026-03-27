#!/usr/bin/env python3
"""Generate audit summary statistics from audit results.

Usage:
    python scripts/audit_summary.py --input audit_results.json

Reads audit results and prints decision breakdown.
"""

import argparse
import json
import sys
from collections import Counter


def main():
    parser = argparse.ArgumentParser(description="Summarise audit results")
    parser.add_argument("--input", required=True, help="Path to audit results JSON")
    args = parser.parse_args()

    with open(args.input) as f:
        results = json.load(f)

    if not isinstance(results, list):
        results = results.get("audits", results.get("results", []))

    total = len(results)
    by_strength = Counter()
    by_recommendation = Counter()
    jurisdiction_failures = 0
    liberalisations = 0
    trade_framing_failures = 0

    for r in results:
        by_strength[r.get("match_strength", "UNKNOWN")] += 1
        by_recommendation[r.get("recommendation", "UNKNOWN")] += 1
        if not r.get("jurisdiction_ok", True):
            jurisdiction_failures += 1
        if r.get("is_liberalisation", False):
            liberalisations += 1
        if not r.get("trade_framing_ok", True):
            trade_framing_failures += 1

    print(f"=== AUDIT SUMMARY ===\n")
    print(f"Total entries audited: {total}\n")

    print(f"--- Match Strength ---")
    for s, c in by_strength.most_common():
        print(f"  {s}: {c}")

    print(f"\n--- Recommendations ---")
    for r, c in by_recommendation.most_common():
        print(f"  {r}: {c}")

    print(f"\n--- Flags ---")
    print(f"  Jurisdiction failures: {jurisdiction_failures}")
    print(f"  Liberalisations: {liberalisations}")
    print(f"  Trade framing failures: {trade_framing_failures}")

    removals = by_recommendation.get("REMOVE", 0)
    if removals:
        print(f"\n  ACTION REQUIRED: {removals} entries recommended for removal")


if __name__ == "__main__":
    main()
