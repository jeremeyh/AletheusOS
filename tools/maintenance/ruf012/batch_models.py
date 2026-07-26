"""Data models for repository-wide RUF012 batch previews."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any


class BatchItemStatus(StrEnum):
    """Outcome assigned to one batch-preview candidate."""

    VALIDATED = "validated"
    SKIPPED = "skipped"
    UNSUPPORTED = "unsupported"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class BatchPreviewItem:
    """Result of previewing one candidate."""

    path: Path
    class_name: str
    attribute_name: str
    line_number: int
    classification: str
    transformation: str | None
    status: BatchItemStatus
    changed: bool = False
    validated: bool = False
    diff: str = ""
    notes: tuple[str, ...] = ()
    error: str | None = None

    @property
    def candidate_name(self) -> str:
        """Return a stable human-readable candidate identifier."""

        return f"{self.class_name}.{self.attribute_name}"

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation."""

        return {
            "path": self.path.as_posix(),
            "class_name": self.class_name,
            "attribute_name": self.attribute_name,
            "candidate_name": self.candidate_name,
            "line_number": self.line_number,
            "classification": self.classification,
            "transformation": self.transformation,
            "status": self.status.value,
            "changed": self.changed,
            "validated": self.validated,
            "diff": self.diff,
            "notes": list(self.notes),
            "error": self.error,
        }


@dataclass(frozen=True, slots=True)
class BatchPreviewSummary:
    """Aggregate result of a repository-wide dry-run preview."""

    repository_root: Path
    files_scanned: int
    candidates_discovered: int
    items: tuple[BatchPreviewItem, ...] = field(default_factory=tuple)
    repository_modified: bool = False

    @property
    def validated_count(self) -> int:
        """Return the number of validated candidate previews."""

        return self._status_count(BatchItemStatus.VALIDATED)

    @property
    def skipped_count(self) -> int:
        """Return the number of skipped candidates."""

        return self._status_count(BatchItemStatus.SKIPPED)

    @property
    def unsupported_count(self) -> int:
        """Return the number of unsupported candidates."""

        return self._status_count(BatchItemStatus.UNSUPPORTED)

    @property
    def failed_count(self) -> int:
        """Return the number of failed candidate previews."""

        return self._status_count(BatchItemStatus.FAILED)

    @property
    def changed_count(self) -> int:
        """Return the number of previews containing source changes."""

        return sum(item.changed for item in self.items)

    @property
    def successful(self) -> bool:
        """Return whether the batch completed without candidate failures."""

        return self.failed_count == 0 and not self.repository_modified

    def _status_count(self, status: BatchItemStatus) -> int:
        return sum(item.status is status for item in self.items)

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation."""

        return {
            "repository_root": self.repository_root.as_posix(),
            "files_scanned": self.files_scanned,
            "candidates_discovered": self.candidates_discovered,
            "validated": self.validated_count,
            "changed": self.changed_count,
            "skipped": self.skipped_count,
            "unsupported": self.unsupported_count,
            "failed": self.failed_count,
            "repository_modified": self.repository_modified,
            "successful": self.successful,
            "items": [item.as_dict() for item in self.items],
        }
