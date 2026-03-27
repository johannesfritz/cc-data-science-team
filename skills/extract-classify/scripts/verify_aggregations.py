#!/usr/bin/env python3
"""Verify aggregation integrity across extraction hierarchy levels.

Checks that counts are consistent: entry → country-theme → country → theme → total.

Usage:
    python scripts/verify_aggregations.py --input extractions.json

Exit code 1 if any check fails.
"""

import argparse
import json
import sys
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser(description="Verify aggregation integrity")
    parser.add_argument("--input", required=True, help="Path to extractions JSON")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    errors = []
    checks = 0

    # Collect counts at each level
    total_entries = 0
    by_theme = defaultdict(int)
    by_country = defaultdict(int)
    by_ct = defaultdict(int)
    named_by_ct = defaultdict(set)
    unnamed_by_ct = defaultdict(int)

    for theme in data.get("themes", []):
        tk = theme["theme_key"]
        theme_entries = 0

        for country in theme.get("countries", []):
            cn = country["country"]
            ct = f"{cn}__{tk}"
            ct_entries = len(country.get("entries", []))

            total_entries += ct_entries
            theme_entries += ct_entries
            by_country[cn] += ct_entries
            by_ct[ct] = ct_entries

            for entry in country.get("entries", []):
                for act in entry.get("state_acts", []):
                    if act["type"] == "named":
                        named_by_ct[ct].add(act["name"])
                    else:
                        unnamed_by_ct[ct] += 1

        by_theme[tk] = theme_entries

    # Check 1: Theme totals sum to grand total
    checks += 1
    theme_sum = sum(by_theme.values())
    if theme_sum != total_entries:
        errors.append(f"Theme totals ({theme_sum}) != grand total ({total_entries})")

    # Check 2: Country totals sum to grand total
    checks += 1
    country_sum = sum(by_country.values())
    if country_sum != total_entries:
        errors.append(f"Country totals ({country_sum}) != grand total ({total_entries})")

    # Check 3: CT pair totals sum to grand total
    checks += 1
    ct_sum = sum(by_ct.values())
    if ct_sum != total_entries:
        errors.append(f"CT pair totals ({ct_sum}) != grand total ({total_entries})")

    # Check 4: No empty CT pairs (entries list exists but is empty)
    checks += 1
    empty_cts = [ct for ct, count in by_ct.items() if count == 0]
    if empty_cts:
        errors.append(f"Empty CT pairs (0 entries): {empty_cts}")

    # Check 5: Named acts are deduplicated within CT pairs
    checks += 1
    for ct, names in named_by_ct.items():
        # Check for case-insensitive duplicates
        lower_names = [n.lower().strip() for n in names]
        if len(lower_names) != len(set(lower_names)):
            dupes = [n for n in lower_names if lower_names.count(n) > 1]
            errors.append(f"Case-insensitive named act duplicates in {ct}: {set(dupes)}")

    # Check 6: State act counts are positive where entries exist
    checks += 1
    for ct, count in by_ct.items():
        named_count = len(named_by_ct.get(ct, set()))
        unnamed_count = unnamed_by_ct.get(ct, 0)
        if count > 0 and named_count + unnamed_count == 0:
            errors.append(f"CT pair {ct} has {count} entries but 0 state acts")

    # Check 7: No duplicate entry IDs
    checks += 1
    all_ids = []
    for theme in data.get("themes", []):
        for country in theme.get("countries", []):
            for entry in country.get("entries", []):
                all_ids.append(entry.get("entry_id", ""))
    id_dupes = [eid for eid in set(all_ids) if all_ids.count(eid) > 1]
    if id_dupes:
        errors.append(f"Duplicate entry IDs: {id_dupes}")

    # Report
    print(f"=== AGGREGATION INTEGRITY ===\n")
    print(f"Checks run: {checks}")
    print(f"Total entries: {total_entries}")
    print(f"Themes: {len(by_theme)}")
    print(f"Countries: {len(by_country)}")
    print(f"CT pairs: {len(by_ct)}")

    if errors:
        print(f"\nFAIL — {len(errors)} error(s):\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"\nPASS — all {checks} checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
