"""
AletheusOS
Genesis 46.1

Cognitive Kernel™

Canonical Models
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def new_kernel_record_id() -> str:
    return f"CK-{uuid4().hex[:12].upper()}"


@dataclass(slots=True)
class CognitiveExecutionStep:
    """
    Represents a single governed step executed by the Cognitive Kernel.
    """

    order: int
    stage: str
    engine: str
    status: str
    timestamp: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CognitiveKernelRecord:
    """
    Canonical execution record produced by the Cognitive Kernel.

    Every execution entering the Foundation eventually produces one of
    these records.

    This becomes part of Double Hedron Session Memory.
    """

    kernel_record_id: str

    identity: str
    application: str

    query: str

    intent: dict[str, Any]

    capability_resolution: dict[str, Any]

    execution_plan: dict[str, Any] | None

    constitutional_articles: list[str] = field(default_factory=list)

    execution_steps: list[CognitiveExecutionStep] = field(default_factory=list)

    status: str = "CREATED"

    confidence: float = 1.0

    created_at: str = field(default_factory=utc_now)

    completed_at: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def add_step(
        self,
        *,
        stage: str,
        engine: str,
        status: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:

        self.execution_steps.append(
            CognitiveExecutionStep(
                order=len(self.execution_steps) + 1,
                stage=stage,
                engine=engine,
                status=status,
                metadata=metadata or {},
            )
        )

    def mark_completed(self) -> None:

        self.status = "COMPLETED"
        self.completed_at = utc_now()

    def mark_failed(self) -> None:

        self.status = "FAILED"
        self.completed_at = utc_now()

    def to_dict(self) -> dict[str, Any]:

        return {
            "kernel_record_id": self.kernel_record_id,
            "identity": self.identity,
            "application": self.application,
            "query": self.query,
            "intent": self.intent,
            "capability_resolution": self.capability_resolution,
            "execution_plan": self.execution_plan,
            "constitutional_articles": self.constitutional_articles,
            "execution_steps": [
                step.to_dict()
                for step in self.execution_steps
            ],
            "status": self.status,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "metadata": self.metadata,
        }
