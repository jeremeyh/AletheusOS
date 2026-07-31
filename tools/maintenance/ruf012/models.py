"""Shared models for the Genesis 11 RUF012 preview engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RewritePreview:
    candidate: Any
    path: Path
    original_source: str
    rewritten_source: str
    diff: str
    changed: bool
    validated: bool
    transformation: str
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RewriteFailure:
    candidate: Any
    reason: str


@dataclass
class RewriteStatistics:
    discovered: int = 0
    supported: int = 0
    previewed: int = 0
    changed: int = 0
    validated: int = 0
    skipped: int = 0
    failed: int = 0
    failures: list[RewriteFailure] = field(default_factory=list)

    def record_failure(self, candidate: Any, reason: str) -> None:
        self.failed += 1
        self.failures.append(RewriteFailure(candidate=candidate, reason=reason))
