"""
Read-only repository writer for the Genesis 11 RUF012 pipeline.

This writer intentionally performs NO source modifications.
Its responsibility is to summarize the execution stage and provide
the future attachment point for repository rewrites.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tools.maintenance.ruf012.executor.models import ExecutionSummary


@dataclass(frozen=True, slots=True)
class WriteResult:
    """Summary of the write stage."""

    discovered: int
    eligible: int
    modified: int
    skipped: int
    read_only: bool = True


class RepositoryWriter:
    """Read-only writer for the native RUF012 pipeline."""

    def __init__(self, root: Path):
        self.root = Path(root)

    def apply(
        self,
        execution: ExecutionSummary,
    ) -> WriteResult:
        """
        Consume the execution summary.

        This stage intentionally performs no filesystem writes.
        It reports what would have been eligible for rewriting.
        """

        result = WriteResult(
            discovered=execution.total,
            eligible=execution.previewed,
            modified=0,
            skipped=execution.skipped + execution.failed,
        )

        self._print_summary(result)

        return result

    def _print_summary(
        self,
        result: WriteResult,
    ) -> None:
        """Print a deterministic repository summary."""

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
        print("Native execution pipeline connected.")
        print("Repository remains unchanged (preview mode).")
