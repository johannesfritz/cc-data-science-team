#!/usr/bin/env python3
"""Verify extracted quotes against source document text.

Five-tier verification:
  EXACT         — normalised passage found verbatim in source
  PHRASE_ALL    — all 3 anchor phrases found (whitespace/encoding diff)
  PHRASE_PARTIAL — 2/3 anchors found
  PHRASE_WEAK   — 1/3 anchors found
  NOT_FOUND     — 0/3 anchors found → action required

Usage:
    python scripts/verify_quotes.py --extractions extractions.json --source data/document.md

Exit code 1 if any NOT_FOUND passages exist.

Ported from NTE-check 70_quote_verification.py.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path


def normalise(text: str) -> str:
    """Collapse all whitespace to single spaces."""
    return re.sub(r"\s+", " ", text).strip()


def extract_anchors(text: str, anchor_len: int = 60) -> list[str]:
    """Extract first, middle, and last anchor phrases from a passage."""
    n = len(text)
    first = text[:anchor_len].strip()
    mid_start = max(0, n // 2 - anchor_len // 2)
    middle = text[mid_start : mid_start + anchor_len].strip()
    last = text[max(0, n - anchor_len) :].strip()
    return [first, middle, last]


def collect_quotes(data: dict) -> list[dict]:
    """Extract all quotes from the extraction JSON structure."""
    quotes = []
    for theme in data.get("themes", []):
        theme_key = theme.get("theme_key", "")
        for country_block in theme.get("countries", []):
            country = country_block.get("country", "")
            for entry in country_block.get("entries", []):
                entry_id = entry.get("entry_id", "")

                # Check passages array (post-dedup format)
                for idx, p in enumerate(entry.get("passages", [])):
                    quotes.append({
                        "entry_id": entry_id,
                        "country": country,
                        "theme_key": theme_key,
                        "text": p.get("text", ""),
                        "source": "passages",
                        "idx": idx,
                    })

                # Also check exact_quote field (pre-dedup format)
                eq = entry.get("exact_quote", "")
                if eq and not entry.get("passages"):
                    quotes.append({
                        "entry_id": entry_id,
                        "country": country,
                        "theme_key": theme_key,
                        "text": eq,
                        "source": "exact_quote",
                        "idx": 0,
                    })
    return quotes


def verify(quotes: list[dict], source_norm: str) -> list[dict]:
    """Run 5-tier verification on each quote."""
    results = []
    for q in quotes:
        text_norm = normalise(q["text"])
        word_count = len(text_norm.split())

        if not text_norm:
            results.append({**q, "word_count": 0, "status": "EMPTY", "anchors": "", "note": "empty quote"})
            continue

        # Tier 1: Exact normalised match
        if text_norm in source_norm:
            results.append({**q, "word_count": word_count, "status": "EXACT", "anchors": "", "note": ""})
            continue

        # Tier 2: Anchor phrase search
        anchors = extract_anchors(text_norm)
        valid = [a for a in anchors if len(a) > 10]
        found = sum(1 for a in valid if a in source_norm)
        n_valid = len(valid)
        anchors_str = f"{found}/{n_valid}"

        if n_valid == 0:
            status = "PHRASE_WEAK"
            note = "passage too short for anchor search"
        elif found == n_valid:
            status = "PHRASE_ALL"
            note = ""
        elif found >= 2:
            status = "PHRASE_PARTIAL"
            note = ""
        elif found == 1:
            status = "PHRASE_WEAK"
            note = ""
        else:
            status = "NOT_FOUND"
            note = text_norm[:120]

        results.append({**q, "word_count": word_count, "status": status, "anchors": anchors_str, "note": note})

    return results


def main():
    parser = argparse.ArgumentParser(description="Verify extracted quotes against source document")
    parser.add_argument("--extractions", required=True, help="Path to extractions JSON")
    parser.add_argument("--source", required=True, help="Path to source document (markdown/text)")
    parser.add_argument("--output", default=None, help="Output CSV path (default: quote_verification.csv)")
    args = parser.parse_args()

    # Load source
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"FAIL: Source file not found — {args.source}")
        sys.exit(1)
    source_norm = normalise(source_path.read_text(encoding="utf-8"))

    # Load extractions
    with open(args.extractions) as f:
        data = json.load(f)

    quotes = collect_quotes(data)
    if not quotes:
        print("No quotes found in extraction file.")
        sys.exit(0)

    results = verify(quotes, source_norm)

    # Write CSV
    out_path = args.output or "quote_verification.csv"
    fieldnames = ["entry_id", "country", "theme_key", "source", "idx", "word_count", "status", "anchors", "note"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    # Summary
    total = len(results)
    statuses = ["EXACT", "PHRASE_ALL", "PHRASE_PARTIAL", "PHRASE_WEAK", "NOT_FOUND", "EMPTY"]
    counts = {s: sum(1 for r in results if r["status"] == s) for s in statuses}

    print(f"\n{'=' * 44}")
    print(f"  QUOTE VERIFICATION SUMMARY")
    print(f"{'=' * 44}")
    print(f"  Total quotes:        {total}")
    for s in statuses:
        c = counts[s]
        if c == 0:
            continue
        pct = c / total * 100
        marker = "  ← ACTION REQUIRED" if s in ("NOT_FOUND", "EMPTY") and c > 0 else ""
        print(f"  {s:<16} {c:>4} ({pct:5.1f}%){marker}")

    # Flagged
    flagged = [r for r in results if r["status"] in ("NOT_FOUND", "PHRASE_WEAK", "EMPTY")]
    if flagged:
        print(f"\n  FLAGGED FOR REVIEW ({len(flagged)}):")
        for r in flagged:
            print(f"    [{r['status']}] {r['entry_id']}")
            if r["note"] and r["note"] != "passage too short for anchor search":
                print(f"      {r['note'][:80]}...")

    not_found = counts["NOT_FOUND"] + counts["EMPTY"]
    if not_found > 0:
        print(f"\nFAIL: {not_found} quote(s) could not be verified.")
        sys.exit(1)
    else:
        print(f"\nPASS: All {total} quotes verified against source.")
        sys.exit(0)


if __name__ == "__main__":
    main()
