from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def _timestamp():
    return datetime.now(UTC).isoformat()


def new_decision_id():
    return f"CAP-DEC-{uuid4().hex[:12].upper()}"


@dataclass(slots=True)
class Capability:
    capability_id: str
    name: str
    namespace: str
    category: str = ""
    description: str = ""
    version: str = "1.0.0"
    genesis: str = "21.6"
    dependencies: list[str] = field(default_factory=list)
    status: str = "enabled"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "capability_id": self.capability_id,
            "name": self.name,
            "namespace": self.namespace,
            "category": self.category,
            "description": self.description,
            "version": self.version,
            "genesis": self.genesis,
            "dependencies": self.dependencies,
            "status": self.status,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class CapabilityProfile:
    profile_id: str
    name: str
    description: str = ""
    inherits: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    denials: list[str] = field(default_factory=list)
    bundles: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "profile_id": self.profile_id,
            "name": self.name,
            "description": self.description,
            "inherits": self.inherits,
            "capabilities": self.capabilities,
            "denials": self.denials,
            "bundles": self.bundles,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class CapabilityBundle:
    bundle_id: str
    name: str
    description: str = ""
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "bundle_id": self.bundle_id,
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class CapabilityGrant:
    identity_id: str
    capability_id: str
    granted_by: str = "system"
    reason: str = ""
    expires_at: str | None = None
    granted_at: str = field(default_factory=_timestamp)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "identity_id": self.identity_id,
            "capability_id": self.capability_id,
            "granted_by": self.granted_by,
            "reason": self.reason,
            "expires_at": self.expires_at,
            "granted_at": self.granted_at,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class CapabilityDecision:
    decision_id: str
    identity_id: str
    capability_id: str
    intent: str
    result: str
    reason: str
    confidence: float = 1.0
    context: dict[str, Any] = field(default_factory=dict)
    risk: str = "low"
    constitutional_articles: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)
    ledger_reference: str | None = None
    timestamp: str = field(default_factory=_timestamp)

    def to_dict(self):
        return {
            "decision_id": self.decision_id,
            "identity_id": self.identity_id,
            "capability_id": self.capability_id,
            "intent": self.intent,
            "result": self.result,
            "reason": self.reason,
            "confidence": self.confidence,
            "context": self.context,
            "risk": self.risk,
            "constitutional_articles": self.constitutional_articles,
            "alternatives": self.alternatives,
            "ledger_reference": self.ledger_reference,
            "timestamp": self.timestamp,
        }
