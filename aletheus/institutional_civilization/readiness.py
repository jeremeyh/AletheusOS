"""Civilization readiness models and scoring."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


class ReadinessState(StrEnum):
    READY = "ready"
    DEGRADED = "degraded"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True, slots=True)
class ReadinessCheck:
    name: str
    institution_id: str
    state: ReadinessState
    message: str
    evidence: dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.state in (
            ReadinessState.READY,
            ReadinessState.SKIPPED,
        )

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["state"] = self.state.value
        value["passed"] = self.passed
        return value


@dataclass(slots=True)
class CivilizationReadinessReport:
    bootstrap_id: str = field(
        default_factory=lambda: f"BOOT-{uuid4().hex[:12].upper()}"
    )

    generated_at: str = field(default_factory=_timestamp)

    checks: list[ReadinessCheck] = field(default_factory=list)

    institution_count: int = 0
    platform_component_count: int = 0
    graph_node_count: int = 0
    graph_edge_count: int = 0

    synthetic_harmony: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def ready_count(self) -> int:
        return sum(
            check.state == ReadinessState.READY
            for check in self.checks
        )

    @property
    def skipped_count(self) -> int:
        return sum(
            check.state == ReadinessState.SKIPPED
            for check in self.checks
        )

    @property
    def degraded_count(self) -> int:
        return sum(
            check.state == ReadinessState.DEGRADED
            for check in self.checks
        )

    @property
    def failed_count(self) -> int:
        return sum(
            check.state == ReadinessState.FAILED
            for check in self.checks
        )

    @property
    def status(self) -> str:
        """
        FAILED overrides everything.

        DEGRADED indicates functionality exists but
        is operating below constitutional expectations.

        READY includes healthy SKIPPED institutions.
        """

        if self.failed_count:
            return "failed"

        if self.degraded_count:
            return "degraded"

        return "ready"

    @property
    def passed(self) -> bool:
        return self.failed_count == 0

    def calculate_harmony(self) -> float:
        """
        Synthetic Harmony™

        READY
            Institution executed successfully.

        SKIPPED
            Institution intentionally had nothing to do.
            This is considered a successful constitutional outcome
            and therefore contributes full harmony.

        DEGRADED
            Partial operational capability.

        FAILED
            Operational failure.
        """

        weights = {
            ReadinessState.READY: 1.00,
            ReadinessState.SKIPPED: 1.00,
            ReadinessState.DEGRADED: 0.55,
            ReadinessState.FAILED: 0.00,
        }

        if not self.checks:
            self.synthetic_harmony = 0.0
            return self.synthetic_harmony

        total = sum(
            weights[check.state]
            for check in self.checks
        )

        self.synthetic_harmony = round(
            (total / len(self.checks)) * 100.0,
            2,
        )

        return self.synthetic_harmony

    def to_dict(self) -> dict[str, Any]:
        return {
            "bootstrap_id": self.bootstrap_id,
            "generated_at": self.generated_at,
            "status": self.status,
            "passed": self.passed,
            "institution_count": self.institution_count,
            "platform_component_count": self.platform_component_count,
            "graph_node_count": self.graph_node_count,
            "graph_edge_count": self.graph_edge_count,
            "ready": self.ready_count,
            "skipped": self.skipped_count,
            "degraded": self.degraded_count,
            "failed": self.failed_count,
            "synthetic_harmony": self.synthetic_harmony,
            "checks": [
                check.to_dict()
                for check in self.checks
            ],
            "metadata": self.metadata,
        }
