"""
AletheusOS
Genesis 49.0

Reason Engine™

Canonical Reasoning Models
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def new_reason_id() -> str:
    return f"REASON-{uuid4().hex[:12].upper()}"


class ReasonStatus(StrEnum):

    CREATED = "CREATED"

    INFERRED = "INFERRED"

    JUSTIFIED = "JUSTIFIED"

    EVALUATED = "EVALUATED"

    REJECTED = "REJECTED"

    COMPLETED = "COMPLETED"


class ReasonConfidence(StrEnum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    VERY_HIGH = "VERY_HIGH"


@dataclass(slots=True)
class ReasonStep:

    order: int

    statement: str

    support: list[str] = field(default_factory=list)

    confidence: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)


@dataclass(slots=True)
class ReasonObject:

    reason_id: str

    intent: str

    identity: str

    query: str

    conclusion: str

    status: ReasonStatus = ReasonStatus.CREATED

    confidence: float = 0.0

    confidence_label: ReasonConfidence = ReasonConfidence.LOW

    evidence: list[str] = field(default_factory=list)

    memories_used: list[str] = field(default_factory=list)

    alternatives_considered: list[str] = field(default_factory=list)

    constitutional_articles: list[str] = field(default_factory=list)

    reason_chain: list[ReasonStep] = field(default_factory=list)

    provenance: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)

    updated_at: str = field(default_factory=utc_now)

    def add_step(
        self,
        statement: str,
        support: list[str] | None = None,
        confidence: float = 0.0,
        metadata: dict[str, Any] | None = None,
    ) -> None:

        self.reason_chain.append(
            ReasonStep(
                order=len(self.reason_chain) + 1,
                statement=statement,
                support=support or [],
                confidence=confidence,
                metadata=metadata or {},
            )
        )

        self.updated_at = utc_now()

    def set_status(
        self,
        status: ReasonStatus,
    ) -> None:

        self.status = status

        self.updated_at = utc_now()

    def set_confidence(
        self,
        confidence: float,
    ) -> None:

        self.confidence = confidence

        if confidence >= 0.9:
            self.confidence_label = ReasonConfidence.VERY_HIGH

        elif confidence >= 0.75:
            self.confidence_label = ReasonConfidence.HIGH

        elif confidence >= 0.5:
            self.confidence_label = ReasonConfidence.MEDIUM

        else:
            self.confidence_label = ReasonConfidence.LOW

        self.updated_at = utc_now()

    def to_dict(self) -> dict[str, Any]:

        return {
            "reason_id": self.reason_id,
            "intent": self.intent,
            "identity": self.identity,
            "query": self.query,
            "conclusion": self.conclusion,
            "status": self.status.value,
            "confidence": self.confidence,
            "confidence_label": self.confidence_label.value,
            "evidence": self.evidence,
            "memories_used": self.memories_used,
            "alternatives_considered": self.alternatives_considered,
            "constitutional_articles": self.constitutional_articles,
            "reason_chain": [
                step.to_dict()
                for step in self.reason_chain
            ],
            "provenance": self.provenance,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
