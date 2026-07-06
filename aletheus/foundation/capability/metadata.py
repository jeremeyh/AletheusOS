"""
AletheusOS
Genesis 47.5

Foundation Capability Base™

Capability Metadata
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class CapabilityMetadata:
    """
    Canonical metadata describing a Foundation capability.

    Every Foundation capability publishes one
    CapabilityMetadata object.

    This enables discovery, governance,
    certification, documentation, observability,
    and Constitutional Library integration.
    """

    name: str

    genesis: str

    version: str

    description: str

    owner: str = "Foundation"

    status: str = "healthy"

    certification: str = "prototype"

    constitutional_articles: list[str] = field(default_factory=list)

    dependencies: list[str] = field(default_factory=list)

    proofs: list[str] = field(default_factory=list)

    release: str = ""

    created_at: str = field(default_factory=utc_now)

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)
