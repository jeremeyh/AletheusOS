from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple

PREDECESSOR_EVIDENCE_DIGEST = "sha256:dede44e71354c80bbfedfd841d99ef2d81143b634815a7d6d8802577c33d1f74"
PREDECESSOR_BINDING_DIGEST = "sha256:76de4dfce1810339d734e86c570f2adcc206fe7379d1104e66ca4b3d90447ab3"

class LifecycleState(str, Enum):
    DISCOVERED="DISCOVERED"
    REGISTERED="REGISTERED"
    INITIALIZING="INITIALIZING"
    READY="READY"
    STARTING="STARTING"
    RUNNING="RUNNING"
    DEGRADED="DEGRADED"
    STOPPING="STOPPING"
    STOPPED="STOPPED"
    UNREGISTERED="UNREGISTERED"
    FAULTED="FAULTED"

class RegistrationDisposition(str, Enum):
    ACCEPTED="ACCEPTED"
    REFUSED="REFUSED"
    IDEMPOTENT="IDEMPOTENT"

@dataclass(frozen=True)
class ServiceIdentity:
    service_id: str
    owner: str
    authority_domain: str
    implementation_ref: str
    dependencies: Tuple[str, ...] = field(default_factory=tuple)
    capabilities: Tuple[str, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class RegistrationReceipt:
    service_id: str
    disposition: RegistrationDisposition
    reason: str
    evidence_digest: str

@dataclass(frozen=True)
class LifecycleReceipt:
    service_id: str
    prior_state: LifecycleState
    new_state: LifecycleState
    accepted: bool
    reason: str
    evidence_digest: str
