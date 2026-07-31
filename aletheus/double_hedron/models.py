"""
AletheusOS
Genesis 48.0

Double Hedron Session Memory™

Canonical Memory Models
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def new_memory_id() -> str:
    return f"MEM-{uuid4().hex[:12].upper()}"


class MemoryType(StrEnum):
    SESSION = "SESSION"

    WORKING = "WORKING"

    OBSERVATION = "OBSERVATION"

    EXECUTION = "EXECUTION"

    IDENTITY = "IDENTITY"

    ORGANIZATION = "ORGANIZATION"

    KNOWLEDGE = "KNOWLEDGE"

    EVIDENCE = "EVIDENCE"

    RELATIONSHIP = "RELATIONSHIP"

    CONSTITUTIONAL = "CONSTITUTIONAL"

    EXPERIENCE = "EXPERIENCE"


class MemoryLifecycle(StrEnum):
    CREATED = "CREATED"

    OBSERVED = "OBSERVED"

    REFERENCED = "REFERENCED"

    VALIDATED = "VALIDATED"

    CONSTITUTIONAL = "CONSTITUTIONAL"

    ARCHIVED = "ARCHIVED"


@dataclass(slots=True)
class MemoryReference:
    memory_id: str

    relationship: str

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)


@dataclass(slots=True)
class MemoryObject:
    memory_id: str

    identity: str

    capability: str

    execution: str

    session: str

    memory_type: MemoryType

    lifecycle: MemoryLifecycle

    observation: str

    evidence: list[str] = field(default_factory=list)

    reasoning: list[str] = field(default_factory=list)

    confidence: float = 0.0

    references: list[MemoryReference] = field(default_factory=list)

    provenance: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)

    updated_at: str = field(default_factory=utc_now)

    def add_reference(
        self,
        memory_id: str,
        relationship: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:

        self.references.append(
            MemoryReference(
                memory_id=memory_id,
                relationship=relationship,
                metadata=metadata or {},
            )
        )

        self.updated_at = utc_now()

    def promote(
        self,
        lifecycle: MemoryLifecycle,
    ) -> None:

        self.lifecycle = lifecycle

        self.updated_at = utc_now()

    def to_dict(self) -> dict[str, Any]:

        return {
            "memory_id": self.memory_id,
            "identity": self.identity,
            "capability": self.capability,
            "execution": self.execution,
            "session": self.session,
            "memory_type": self.memory_type.value,
            "lifecycle": self.lifecycle.value,
            "observation": self.observation,
            "evidence": self.evidence,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "references": [reference.to_dict() for reference in self.references],
            "provenance": self.provenance,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
