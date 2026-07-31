"""Domain models for governed repository evolution."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

OperationType = Literal["replace_text", "write_file", "move_file"]


@dataclass(frozen=True, slots=True)
class Operation:
    operation: OperationType
    path: str
    expected_sha256: str | None = None
    old: str | None = None
    new: str | None = None
    content: str | None = None
    destination: str | None = None


@dataclass(frozen=True, slots=True)
class ValidationSpec:
    ruff_targets: tuple[str, ...] = ()
    compile_targets: tuple[str, ...] = ()
    pytest_targets: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class EvolutionPlan:
    plan_id: str
    summary: str
    operations: tuple[Operation, ...]
    validation: ValidationSpec = ValidationSpec()


@dataclass(frozen=True, slots=True)
class CommandResult:
    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str


@dataclass(slots=True)
class EvolutionResult:
    plan_id: str
    mode: str
    status: str
    changed_paths: list[str] = field(default_factory=list)
    backup_directory: str | None = None
    rollback_manifest: str | None = None
    commands: list[CommandResult] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
