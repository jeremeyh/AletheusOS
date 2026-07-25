#!/usr/bin/env python3
"""Repository health metrics."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass

from .inventory import InventoryEntry
from .rules import PolicyViolation


@dataclass(frozen=True, slots=True)
class RepositoryMetrics:
    total_files: int
    python_files: int
    shell_files: int
    documentation_files: int
    zero_byte_files: int
    root_files: int
    policy_errors: int
    policy_warnings: int
    health_score: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def calculate_metrics(
    entries: Iterable[InventoryEntry],
    violations: Iterable[PolicyViolation],
) -> RepositoryMetrics:
    file_list = list(entries)
    violation_list = list(violations)

    total = len(file_list)
    python_files = sum(item.suffix == ".py" for item in file_list)
    shell_files = sum(item.suffix == ".sh" for item in file_list)
    documentation_files = sum(
        item.suffix in {".md", ".rst", ".txt"} for item in file_list
    )
    zero_byte_files = sum(item.size == 0 for item in file_list)
    root_files = sum(len(item.relative_path.parts) == 1 for item in file_list)
    errors = sum(item.severity == "error" for item in violation_list)
    warnings = sum(item.severity == "warning" for item in violation_list)

    penalty = (
        errors * 8.0
        + warnings * 2.0
        + zero_byte_files * 0.25
        + max(0, root_files - 20) * 0.25
    )

    health_score = max(0.0, min(100.0, 100.0 - penalty))

    return RepositoryMetrics(
        total_files=total,
        python_files=python_files,
        shell_files=shell_files,
        documentation_files=documentation_files,
        zero_byte_files=zero_byte_files,
        root_files=root_files,
        policy_errors=errors,
        policy_warnings=warnings,
        health_score=round(health_score, 2),
    )
