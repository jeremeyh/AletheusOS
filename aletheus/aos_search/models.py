from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def _timestamp():
    return datetime.now(UTC).isoformat()


def new_query_id():
    return f"query.{uuid4().hex[:12]}"


@dataclass(slots=True)
class SearchRequest:
    query_id: str
    query: str

    identity: str = ""
    application: str = ""
    organization: str = ""

    created_at: str = field(default_factory=_timestamp)

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):

        return {
            "query_id": self.query_id,
            "query": self.query,
            "identity": self.identity,
            "application": self.application,
            "organization": self.organization,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class SearchResponse:
    query_id: str

    answer: str = ""

    confidence: float = 0.0

    sources: list[str] = field(default_factory=list)

    execution_plan: list[str] = field(default_factory=list)

    constitutional_articles: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):

        return {
            "query_id": self.query_id,
            "answer": self.answer,
            "confidence": self.confidence,
            "sources": self.sources,
            "execution_plan": self.execution_plan,
            "constitutional_articles": self.constitutional_articles,
            "metadata": self.metadata,
        }
