"""
Preview the first safe RUF012 rewrite.

This command never writes source files.
"""

from __future__ import annotations

from pathlib import Path

from .rewriter import CandidateRewriter
from .scanner import RepositoryScanner


def main() -> int:
    root = Path.cwd().resolve()

    scan_result = RepositoryScanner(root).scan()

    if not scan_result.safe_candidates:
        print("No safe RUF012 candidates were found.")
        return 0

    candidate = scan_result.safe_candidates[0]

    preview = CandidateRewriter(root).preview(candidate)

    print("=" * 72)
    print("Genesis 11 RUF012 Rewrite Preview")
    print("=" * 72)
    print(f"File       : {candidate.path}")
    print(f"Class      : {candidate.class_name}")
    print(f"Attribute  : {candidate.attribute_name}")
    print(f"Line       : {candidate.line}")
    print(f"Import added: {preview.import_added}")
    print()
    print(preview.diff, end="")

    print()
    print("=" * 72)
    print("DRY RUN ONLY")
    print("No source files were modified.")
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
