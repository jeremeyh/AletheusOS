from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class CTFRouteStatus(str, Enum):
    PENDING = "pending"
    ROUTED = "routed"
    COMPLETED = "completed"
    FAILED = "failed"


class CTFPathwayStatus(str, Enum):
    NORMAL = "normal"
    CANDIDATE = "candidate"
    PREFERRED = "preferred"
    EXPRESS = "express"
    CANONICAL = "canonical"
    DORMANT = "dormant"


@dataclass
class CTFRouteRequest:
    """
    A request entering the Cognitive Transit Fabric.

    CTF routes cognition. It does not reason.
    """

    request_id: str
    intent_id: str | None
    route_key: str
    payload: dict[str, Any] = field(default_factory=dict)

    source: str = "runtime"
    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)


@dataclass
class CTFRouteResult:
    """
    Result returned by the Cognitive Transit Fabric.
    """

    request_id: str
    route_key: str
    destination: str | None

    status: CTFRouteStatus
    result: Any = None
    error: str | None = None

    pathway_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    completed_at: str = field(default_factory=utc_now)


@dataclass
class CTFPathway:
    """
    A cognitive pathway records how a request moved
    through AletheusOS.

    v1 records pathways only.
    Future versions may score, promote, retire, or optimize them.
    """

    pathway_id: str
    route_key: str
    nodes: list[str]

    status: CTFPathwayStatus = CTFPathwayStatus.NORMAL
    success_count: int = 0
    failure_count: int = 0

    average_latency_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
