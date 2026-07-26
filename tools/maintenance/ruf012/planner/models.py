"""Planner domain models for repository-scale RUF012 execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class PlanStatus(StrEnum):
    """Planning state."""

    READY = "ready"
    SKIPPED = "skipped"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class PlannedRewrite:
    """One deterministic rewrite plan."""

    path: Path
    class_name: str
    attribute_name: str
    line_number: int
    status: PlanStatus
    reason: str

    @property
    def candidate_name(self) -> str:
        """Return Class.Attribute."""

        return f"{self.class_name}.{self.attribute_name}"

    def as_dict(self) -> dict[str, object]:
        """Serialize."""

        return {
            "path": self.path.as_posix(),
            "class_name": self.class_name,
            "attribute_name": self.attribute_name,
            "candidate_name": self.candidate_name,
            "line_number": self.line_number,
            "status": self.status.value,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class PlannerSummary:
    """Repository planning summary."""

    rewrites: tuple[PlannedRewrite, ...]

    @property
    def ready(self) -> int:
        return sum(
            rewrite.status is PlanStatus.READY
            for rewrite in self.rewrites
        )

    @property
    def skipped(self) -> int:
        return sum(
            rewrite.status is PlanStatus.SKIPPED
            for rewrite in self.rewrites
        )

    @property
    def failed(self) -> int:
        return sum(
            rewrite.status is PlanStatus.FAILED
            for rewrite in self.rewrites
        )

    @property
    def total(self) -> int:
        return len(self.rewrites)

    @property
    def successful(self) -> bool:
        return self.failed == 0

    def as_dict(self) -> dict[str, object]:
        """Serialize."""

        return {
            "total": self.total,
            "ready": self.ready,
            "skipped": self.skipped,
            "failed": self.failed,
            "successful": self.successful,
            "rewrites": [
                rewrite.as_dict()
                for rewrite in self.rewrites
            ],
        }
