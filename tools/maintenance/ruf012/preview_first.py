"""Preview the first safe RUF012 transformation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .rewriter import CandidateRewriter, RewriteError
from .scanner import RepositoryScanner
from .transactions import DryRunTransaction
from .utils.candidates import (
    candidate_attribute_name,
    candidate_class_name,
    candidate_line,
    candidate_path,
)


def _safe_candidates(result: Any) -> list[Any]:
    candidates = getattr(result, "safe_candidates", None)
    if candidates is None:
        raise RuntimeError("Scanner result does not expose safe_candidates.")
    return list(candidates)


def main() -> int:
    root = Path.cwd().resolve()
    candidates = _safe_candidates(RepositoryScanner(root).scan())
    if not candidates:
        print("No safe RUF012 candidates were found.")
        return 0
    candidate = candidates[0]
    try:
        preview = CandidateRewriter(root).preview(candidate)
    except (RewriteError, RuntimeError) as exc:
        print("=" * 72)
        print("Genesis 11 RUF012 Rewrite Preview Failed")
        print("=" * 72)
        print(exc)
        return 1
    transaction = DryRunTransaction().apply(preview)
    print()
    print("=" * 72)
    print("Genesis 11 RUF012 Rewrite Preview")
    print("=" * 72)
    print(f"File           : {candidate_path(candidate)}")
    print(f"Class          : {candidate_class_name(candidate)}")
    print(f"Attribute      : {candidate_attribute_name(candidate)}")
    print(f"Line           : {candidate_line(candidate)}")
    print(f"Transformation : {preview.transformation}")
    print(f"Changed        : {preview.changed}")
    print(f"Validated      : {preview.validated}")
    for note in preview.notes:
        print(f"Note           : {note}")
    print()
    print(preview.diff, end="")
    if not preview.diff.endswith("\n"):
        print()
    print()
    print("=" * 72)
    print("DRY RUN ONLY")
    print(transaction.message)
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
