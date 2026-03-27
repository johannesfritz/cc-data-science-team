#!/usr/bin/env python3
"""Validate markdown document structure for classification readiness.

Usage:
    python scripts/check_structure.py --input data/document.md

Checks heading hierarchy, paragraph breaks, and reports statistics.
"""

import argparse
import re
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to markdown file")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        text = f.read()

    lines = text.split("\n")
    total_lines = len(lines)
    total_words = len(text.split())

    # Count headings by level
    h3 = [l for l in lines if re.match(r"^### ", l)]
    h4 = [l for l in lines if re.match(r"^#### ", l)]
    h5 = [l for l in lines if re.match(r"^##### ", l)]

    # Check for bold country/section names
    bold_h3 = [l for l in h3 if "**" in l]

    # Check for page markers
    page_markers = [l for l in lines if "<!-- page" in l]

    # Check for empty sections (heading followed immediately by another heading)
    empty_sections = 0
    for i in range(len(lines) - 1):
        if re.match(r"^#{3,6} ", lines[i]) and re.match(r"^#{3,6} ", lines[i + 1]):
            empty_sections += 1

    # Report
    print(f"=== DOCUMENT STRUCTURE ===\n")
    print(f"Total lines: {total_lines:,}")
    print(f"Total words: {total_words:,}")
    print(f"Top-level sections (###): {len(h3)}")
    print(f"  - with bold names: {len(bold_h3)}")
    print(f"Sub-sections (####): {len(h4)}")
    print(f"Sub-sub-sections (#####): {len(h5)}")
    print(f"Page markers: {len(page_markers)}")

    # Warnings
    warnings = []
    if len(h3) == 0:
        warnings.append("No ### headings found — document may not be structured for section-by-section processing")
    if len(bold_h3) < len(h3) * 0.8:
        warnings.append(f"Only {len(bold_h3)}/{len(h3)} top-level headings use **bold** — extract-classify relies on bold names for boundary detection")
    if empty_sections > 0:
        warnings.append(f"{empty_sections} empty sections (heading followed by heading with no content)")
    if total_words < 1000:
        warnings.append("Document seems very short — verify full content was extracted")

    if warnings:
        print(f"\n--- Warnings ---")
        for w in warnings:
            print(f"  ⚠ {w}")
        sys.exit(1)
    else:
        print(f"\nStructure OK — ready for extract-classify")
        sys.exit(0)


if __name__ == "__main__":
    main()
