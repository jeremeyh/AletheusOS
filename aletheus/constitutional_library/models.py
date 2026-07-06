"""
AletheusOS
Genesis 51.0

Constitutional Library™

Canonical Knowledge Models
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def new_knowledge_id() -> str:
    return f"KNOW-{uuid4().hex[:12].upper()}"


class KnowledgeStatus(StrEnum):

    DRAFT = "DRAFT"

    VALIDATED = "VALIDATED"

    CANONICAL = "CANONICAL"

    SUPERSEDED = "SUPERSEDED"

    ARCHIVED = "ARCHIVED"


class KnowledgeType(StrEnum):

    PRINCIPLE = "PRINCIPLE"

    POLICY = "POLICY"

    FACT = "FACT"

    OBSERVATION = "OBSERVATION"

    PATTERN = "PATTERN"

    DECISION = "DECISION"

    PROCEDURE = "PROCEDURE"

    DEFINITION = "DEFINITION"

    THEORY = "THEORY"


@dataclass(slots=True)
class KnowledgeObject:
    """
    Canonical institutional knowledge.

    Knowledge is not merely stored.

    Knowledge is governed.
    """

    knowledge_id: str

    title: str

    statement: str

    knowledge_type: KnowledgeType

    status: KnowledgeStatus = KnowledgeStatus.DRAFT

    confidence: float = 0.0

    constitutional_articles: list[str] = field(default_factory=list)

    supporting_evidence: list[str] = field(default_factory=list)

    related_identities: list[str] = field(default_factory=list)

    related_memories: list[str] = field(default_factory=list)

    related_reasons: list[str] = field(default_factory=list)

    execution_graph_nodes: list[str] = field(default_factory=list)

    provenance: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    version: int = 1

    created_at: str = field(default_factory=utc_now)

    updated_at: str = field(default_factory=utc_now)

    def set_status(
        self,
        status: KnowledgeStatus,
    ) -> None:

        self.status = status

        self.updated_at = utc_now()

    def set_confidence(
        self,
        confidence: float,
    ) -> None:

        self.confidence = max(
            0.0,
            min(1.0, confidence),
        )

        self.updated_at = utc_now()

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)
