"""
AletheusOS
Genesis 47.5

Foundation Capability Base™

Foundation Contracts
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class FoundationCapabilityContract:
    """
    Machine-readable Foundation Contract.

    Every permanent Foundation capability should eventually
    publish a contract describing its institutional role.
    """

    capability_name: str

    purpose: str

    responsibilities: list[str] = field(default_factory=list)

    non_responsibilities: list[str] = field(default_factory=list)

    consumes: list[str] = field(default_factory=list)

    produces: list[str] = field(default_factory=list)

    dependencies: list[str] = field(default_factory=list)

    constitutional_articles: list[str] = field(default_factory=list)

    invariants: list[str] = field(default_factory=list)

    proof_contract: list[str] = field(default_factory=list)

    health_contract: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)
