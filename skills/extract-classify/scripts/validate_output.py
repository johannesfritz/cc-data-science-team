#!/usr/bin/env python3
"""Validate extraction output JSON against the expected schema.

Usage:
    python scripts/validate_output.py --input extractions.json

Returns exit code 0 if valid, 1 if errors found.
Prints a summary of issues to stdout.
"""

import argparse
import json
import sys
from collections import Counter


REQUIRED_PROJECT_FIELDS = {"name", "source_document", "extraction_date"}
REQUIRED_ENTRY_FIELDS = {"entry_id", "barrier_description", "exact_quote", "state_acts", "match_strength"}
VALID_MATCH_STRENGTHS = {"DIRECT", "STRONG", "MODERATE", "WEAK", "TENUOUS"}
VALID_ACT_TYPES = {"named", "unnamed"}
VALID_MAST = {"A", "B", "D", "E", "F", "G", "H", "I", "L", "M", "N", "P", "FDI", "Tariff"}
VALID_CONFIDENCE = {"HIGH", "MEDIUM"}


def validate(data: dict) -> list[str]:
    errors = []

    # Project metadata
    if "project" not in data:
        errors.append("Missing top-level 'project' object")
    else:
        missing = REQUIRED_PROJECT_FIELDS - set(data["project"].keys())
        if missing:
            errors.append(f"Project missing fields: {missing}")

    # Themes array
    if "themes" not in data:
        errors.append("Missing top-level 'themes' array")
        return errors

    entry_ids = []
    for ti, theme in enumerate(data["themes"]):
        if "theme_key" not in theme:
            errors.append(f"Theme [{ti}] missing 'theme_key'")
        if "countries" not in theme:
            errors.append(f"Theme [{ti}] missing 'countries'")
            continue

        for ci, country in enumerate(theme.get("countries", [])):
            if "country" not in country:
                errors.append(f"Theme [{ti}] country [{ci}] missing 'country'")
            if "entries" not in country:
                errors.append(f"Theme [{ti}] country [{ci}] missing 'entries'")
                continue

            for ei, entry in enumerate(country["entries"]):
                loc = f"Theme '{theme.get('theme_key', '?')}' / {country.get('country', '?')} / entry [{ei}]"

                # Required fields
                missing = REQUIRED_ENTRY_FIELDS - set(entry.keys())
                if missing:
                    errors.append(f"{loc}: missing fields {missing}")

                # Entry ID uniqueness
                eid = entry.get("entry_id", "")
                if eid:
                    entry_ids.append(eid)

                # Match strength
                ms = entry.get("match_strength", "")
                if ms and ms not in VALID_MATCH_STRENGTHS:
                    errors.append(f"{loc}: invalid match_strength '{ms}'")

                # State acts
                for ai, act in enumerate(entry.get("state_acts", [])):
                    if "name" not in act or "type" not in act:
                        errors.append(f"{loc}: state_act [{ai}] missing name or type")
                    elif act["type"] not in VALID_ACT_TYPES:
                        errors.append(f"{loc}: state_act [{ai}] invalid type '{act['type']}'")

                # Intervention types
                for ii, it in enumerate(entry.get("intervention_types", [])):
                    if "mast" not in it:
                        errors.append(f"{loc}: intervention_type [{ii}] missing 'mast'")
                    elif it["mast"] not in VALID_MAST:
                        errors.append(f"{loc}: intervention_type [{ii}] invalid mast '{it['mast']}'")
                    if it.get("confidence") and it["confidence"] not in VALID_CONFIDENCE:
                        errors.append(f"{loc}: intervention_type [{ii}] invalid confidence")

                # Empty quote check
                if not entry.get("exact_quote", "").strip():
                    errors.append(f"{loc}: exact_quote is empty")

    # Duplicate entry IDs
    id_counts = Counter(entry_ids)
    dupes = {k: v for k, v in id_counts.items() if v > 1}
    if dupes:
        errors.append(f"Duplicate entry_ids: {dupes}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate extraction output JSON")
    parser.add_argument("--input", required=True, help="Path to extractions.json")
    args = parser.parse_args()

    try:
        with open(args.input) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FAIL: Invalid JSON — {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"FAIL: File not found — {args.input}")
        sys.exit(1)

    errors = validate(data)

    if errors:
        print(f"VALIDATION FAILED — {len(errors)} error(s):\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        # Count entries
        total = sum(
            len(entry_list)
            for theme in data.get("themes", [])
            for country in theme.get("countries", [])
            for entry_list in [country.get("entries", [])]
        )
        themes = len(data.get("themes", []))
        countries = len(set(
            country.get("country", "")
            for theme in data.get("themes", [])
            for country in theme.get("countries", [])
        ))
        print(f"VALID — {total} entries across {themes} themes and {countries} countries")
        sys.exit(0)


if __name__ == "__main__":
    main()
