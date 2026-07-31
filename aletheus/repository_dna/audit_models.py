from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class SubsystemStatus(str, Enum):
    CANONICAL = "canonical"
    ACTIVE = "active"
    TRANSITIONAL = "transitional"
    EXPERIMENTAL = "experimental"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SubsystemRecord:
    name: str
    path: str
    python_files: int
    family: str = "Unclassified"
    status: SubsystemStatus = SubsystemStatus.UNKNOWN
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CollisionCandidate:
    cluster: str
    members: list[str]
    reason: str
    severity: str = "review"


@dataclass
class RepositoryDNAAuditReport:
    root: str
    subsystem_count: int
    python_file_count: int
    subsystems: list[SubsystemRecord]
    collision_candidates: list[CollisionCandidate]
    generated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_markdown(self) -> str:
        lines = [
            "# Repository DNA Audit Report",
            "",
            f"Generated: {self.generated_at}",
            f"Root: `{self.root}`",
            "",
            "## Metrics",
            "",
            f"- Top-level subsystems: **{self.subsystem_count}**",
            f"- Python files: **{self.python_file_count}**",
            "",
            "## Collision Candidates",
            "",
        ]

        if not self.collision_candidates:
            lines.append("- None detected.")
        else:
            for c in self.collision_candidates:
                lines.append(
                    f"- **{c.cluster}** ({c.severity}): {', '.join(c.members)} — {c.reason}"
                )

        lines.extend(["", "## Subsystems", ""])
        for s in self.subsystems:
            lines.append(
                f"- `{s.name}` — family: **{s.family}**, files: **{s.python_files}**, status: **{s.status.value}**"
            )

        return "\n".join(lines) + "\n"
