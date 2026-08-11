from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Any
import hashlib, json

PREDECESSOR_TOPOLOGY_DIGEST="sha256:9d32904d85c7bd23bfe21a4a6dace3a986ced578e0ccbb04507cb7ceb32bef23"
PREDECESSOR_EVIDENCE_DIGEST="sha256:b6e8510265e71063ad322a8309549937392dfcae9b7644591971a40b040726e9"

def digest(obj: Any) -> str:
    raw=json.dumps(obj,sort_keys=True,separators=(",",":"),default=str).encode()
    return "sha256:"+hashlib.sha256(raw).hexdigest()

class ActivationState(str, Enum):
    DECLARED="DECLARED"
    BOUND="BOUND"
    ACTIVE="ACTIVE"
    DEGRADED="DEGRADED"
    FAILED="FAILED"
    ROLLED_BACK="ROLLED_BACK"

@dataclass(frozen=True)
class BindingIntent:
    service_id:str
    owner:str
    dependencies:Tuple[str,...]=()
    topology_digest:str=PREDECESSOR_TOPOLOGY_DIGEST

@dataclass(frozen=True)
class BindingReceipt:
    service_id:str
    state:ActivationState
    accepted:bool
    reason:str
    evidence_digest:str

@dataclass(frozen=True)
class ReliabilityObservation:
    service_id:str
    lifecycle_state:str
    health_state:str
    reliability_state:str
    evidence_digest:str
