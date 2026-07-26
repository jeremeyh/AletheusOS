"""Execution models for repository-scale preview execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class ExecutionStatus(StrEnum):
    """Execution outcome."""

    PREVIEWED = "previewed"
    SKIPPED = "skipped"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """Result of one preview execution."""

    path: Path
    candidate_name: str
    status: ExecutionStatus
    message: str
    validated: bool

    def as_dict(self) -> dict[str, object]:
        """Serialize."""

        return {
            "path": self.path.as_posix(),
            "candidate_name": self.candidate_name,
            "status": self.status.value,
            "message": self.message,
            "validated": self.validated,
        }


@dataclass(frozen=True, slots=True)
class ExecutionSummary:
    """Aggregate execution results."""

    results: tuple[ExecutionResult, ...]

    @property
    def previewed(self) -> int:
        return sum(
            result.status is ExecutionStatus.PREVIEWED
            for result in self.results
        )

    @property
    def skipped(self) -> int:
        return sum(
            result.status is ExecutionStatus.SKIPPED
            for result in self.results
        )

    @property
    def failed(self) -> int:
        return sum(
            result.status is ExecutionStatus.FAILED
            for result in self.results
        )

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def successful(self) -> bool:
        return self.failed == 0

    def as_dict(self) -> dict[str, object]:
        """Serialize."""

        return {
            "total": self.total,
            "previewed": self.previewed,
            "skipped": self.skipped,
            "failed": self.failed,
            "successful": self.successful,
            "results": [
                result.as_dict()
                for result in self.results
            ],
        }
