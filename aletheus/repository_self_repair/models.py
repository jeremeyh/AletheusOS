from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class FileClass(StrEnum):
    SOURCE = "source"
    DOCUMENTATION = "documentation"
    CONFIGURATION = "configuration"
    TEST = "test"
    GENERATED = "generated"
    CACHE = "cache"
    BACKUP = "backup"
    REPORT = "report"
    ARCHIVE = "archive"
    UNKNOWN = "unknown"


class ActionKind(StrEnum):
    KEEP = "keep"
    COPY = "copy"
    CONFLICT = "conflict"
    QUARANTINE = "quarantine"
    DELETE = "delete"
    ARCHIVE = "archive"
    SKIP = "skip"


@dataclass(frozen=True, slots=True)
class FileRecord:
    relative_path: str
    size: int
    sha256: str
    modified_ns: int
    file_class: FileClass

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ScanManifest:
    root: str
    generated_at: str
    records: dict[str, FileRecord] = field(default_factory=dict)
    ignored: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "generated_at": self.generated_at,
            "records": {key: value.to_dict() for key, value in self.records.items()},
            "ignored": self.ignored,
            "errors": self.errors,
        }


@dataclass(frozen=True, slots=True)
class Action:
    kind: ActionKind
    relative_path: str
    reason: str
    source_sha256: str | None = None
    target_sha256: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class RepairPlan:
    source_root: str | None
    target_root: str
    generated_at: str
    actions: list[Action] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def counts(self) -> dict[str, int]:
        counts = {kind.value: 0 for kind in ActionKind}
        for action in self.actions:
            counts[action.kind.value] += 1
        return counts

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_root": self.source_root,
            "target_root": self.target_root,
            "generated_at": self.generated_at,
            "counts": self.counts(),
            "actions": [action.to_dict() for action in self.actions],
            "warnings": self.warnings,
        }


@dataclass(slots=True)
class ExecutionResult:
    started_at: str
    completed_at: str
    dry_run: bool
    applied: list[dict[str, Any]] = field(default_factory=list)
    failed: list[dict[str, Any]] = field(default_factory=list)
    archive_path: str | None = None
    source_removed: bool = False

    @property
    def success(self) -> bool:
        return not self.failed

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["success"] = self.success
        return result
