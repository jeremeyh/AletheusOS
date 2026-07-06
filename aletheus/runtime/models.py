"""
AletheusOS
Genesis 52.0

Constitutional Runtime™

Runtime Models
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def new_execution_id() -> str:
    return f"EXEC-{uuid4().hex[:12].upper()}"


def new_session_id() -> str:
    return f"SESSION-{uuid4().hex[:12].upper()}"


class RuntimeStatus(StrEnum):

    CREATED = "CREATED"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"


@dataclass(slots=True)
class RuntimeContext:
    """
    Constitutional execution context.

    Every Foundation capability receives
    the same RuntimeContext.

    This object is the constitutional
    execution envelope.
    """

    execution_id: str

    session_id: str

    query: str

    identity: str | None = None

    intent: str | None = None

    memory_ids: list[str] = field(default_factory=list)

    reason_id: str | None = None

    execution_graph_node: str | None = None

    knowledge_ids: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    status: RuntimeStatus = RuntimeStatus.CREATED

    created_at: str = field(default_factory=utc_now)

    updated_at: str = field(default_factory=utc_now)

    def transition(
        self,
        status: RuntimeStatus,
    ) -> None:

        self.status = status

        self.updated_at = utc_now()

    def to_dict(self) -> dict[str, Any]:

        data = asdict(self)

        #
        # Serialize enums cleanly.
        #

        data["status"] = self.status.value

        return data
