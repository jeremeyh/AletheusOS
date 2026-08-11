from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping, Optional

class EvidenceEventType(str, Enum):
    PERSISTED = "PERSISTED"
    RETRIEVED_VERIFIED = "RETRIEVED_VERIFIED"
    LIFECYCLE_EVALUATED = "LIFECYCLE_EVALUATED"
    ARCHIVED = "ARCHIVED"
    TOMBSTONED = "TOMBSTONED"
    PURGED = "PURGED"
    REPAIRED = "REPAIRED"
    SNAPSHOT_VERIFIED = "SNAPSHOT_VERIFIED"

@dataclass(frozen=True, slots=True)
class MammothEvidenceRecord:
    sequence: int
    event_id: str
    event_type: EvidenceEventType
    object_id: str
    version_id: str
    content_digest: str
    metadata_digest: str
    previous_evidence_hash: str
    evidence_hash: str
    occurred_at_iso: str
    actor_capability: str
    authority_ref: Optional[str] = None
    attributes: Mapping[str, str] = MappingProxyType({})

@dataclass(frozen=True, slots=True)
class ChainVerificationResult:
    valid: bool
    record_count: int
    verified_head_hash: str
    error_sequence: int | None = None
    error: str = ""

@dataclass(frozen=True, slots=True)
class IntegrityVerificationResult:
    valid: bool
    expected_digest: str
    computed_digest: str
    size_bytes: int
