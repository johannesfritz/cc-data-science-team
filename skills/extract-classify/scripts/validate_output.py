#!/usr/bin/env python3
"""Validate extraction output JSON against the expected structure.

Checks:
- Required top-level fields (project, themes)
- Required entry fields (entry_id, exact_quote, match_strength, description or barrier_description)
- Valid match_strength values
- Unique entry IDs
- Non-empty quotes
- Optional: validates custom fields if --schema is provided

Usage:
    python scripts/validate_output.py --input extractions.json
    python scripts/validate_output.py --input extractions.json --schema output-schema.json

Returns exit code 0 if valid, 1 if errors found.
"""

import argparse
import json
import sys
from collections import Counter


VALID_MATCH_STRENGTHS = {"DIRECT", "STRONG", "MODERATE", "WEAK", "TENUOUS"}

# Minimum required fields — any extraction must have these
REQUIRED_ENTRY_FIELDS_MINIMUM = {"entry_id", "exact_quote", "match_strength"}


def validate(data: dict, schema: dict | None = None) -> list[str]:
    errors = []

    # Project metadata
    if "project" not in data:
        errors.append("Missing top-level 'project' object")

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

                # Required minimum fields
                missing = REQUIRED_ENTRY_FIELDS_MINIMUM - set(entry.keys())
                # Allow barrier_description as alias for description
                if "description" not in entry and "barrier_description" not in entry:
                    missing.add("description (or barrier_description)")
                missing.discard("description")
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

                # Empty quote check
                quote = entry.get("exact_quote", "")
                if not quote or not quote.strip():
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
    parser.add_argument("--schema", default=None, help="Optional JSON schema for additional field validation")
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

    schema = None
    if args.schema:
        with open(args.schema) as f:
            schema = json.load(f)

    errors = validate(data, schema)

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
        sections = len(set(
            country.get("country", "")
            for theme in data.get("themes", [])
            for country in theme.get("countries", [])
        ))
        print(f"VALID — {total} entries across {themes} categories and {sections} sections")
        sys.exit(0)


if __name__ == "__main__":
    main()
