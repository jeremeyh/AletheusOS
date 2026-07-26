"""
Read-only writer for the Genesis 11 RUF012 package.

This implementation intentionally performs NO source modifications.
It simply validates the safe candidates produced by the scanner.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class WriteResult:
    discovered: int
    eligible: int
    modified: int
    skipped: int
    read_only: bool = True


class RepositoryWriter:
    SAFE_CLASSIFICATION = "safe-classvar"

    def __init__(self, root: Path):
        self.root = Path(root)

    def apply(self, candidates: Iterable[Any]) -> WriteResult:
        candidates = list(candidates)

        eligible = [
            c
            for c in candidates
            if getattr(c, "classification", None)
            == self.SAFE_CLASSIFICATION
        ]

        result = WriteResult(
            discovered=len(candidates),
            eligible=len(eligible),
            modified=0,
            skipped=len(candidates) - len(eligible),
        )

        print()
        print("=" * 72)
        print("Genesis 11 RUF012 Writer")
        print("=" * 72)
        print("Mode                : READ ONLY")
        print(f"Repository          : {self.root}")
        print(f"Candidates received : {result.discovered}")
        print(f"Eligible            : {result.eligible}")
        print(f"Skipped             : {result.skipped}")
        print(f"Files modified      : {result.modified}")
        print()
        print("Rewrite engine not connected.")
        print("No source files were modified.")

        return result
