from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple

PREDECESSOR_CERTIFICATION_DIGEST = "sha256:a2667459d19993ef096552f64fc25abf89c6c32fff29a461fc0d8df6fae5beeb"
STANDARD = "ALETHEUSOS-PLATFORM-CAPABILITY-INTEGRATION-FABRIC"
GENESIS = "112.22.1"

class CapabilityKind(str, Enum):
    ENGINE = "ENGINE"
    FRAMEWORK = "FRAMEWORK"
    INTELLIGENCE = "INTELLIGENCE_CAPABILITY"
    SECURITY = "SECURITY_SYSTEM"
    PERCEPTION = "PERCEPTION_SYSTEM"
    APPLICATION_FACING = "APPLICATION_FACING_PLATFORM_CAPABILITY"

class AttachmentMode(str, Enum):
    SERVICE_CONTRACT = "SERVICE_CONTRACT"
    EVENT_ROUTE = "EVENT_ROUTE"
    REGISTERED_ADAPTER = "REGISTERED_ADAPTER"
    READ_ONLY_OBSERVER = "READ_ONLY_OBSERVER"

@dataclass(frozen=True)
class CapabilityIdentity:
    capability_id: str
    kind: CapabilityKind
    authority_owner: str
    lifecycle_owner: str
    service_dependencies: Tuple[str, ...] = field(default_factory=tuple)
    attachment_mode: AttachmentMode = AttachmentMode.SERVICE_CONTRACT
    durable_state_owner: str = "MAMMOTH"
    reliability_observer: str = "RSF"
    final_certification_authority: str = "EXTERNAL_RAF"

    def validate(self) -> None:
        if not self.capability_id or not self.authority_owner or not self.lifecycle_owner:
            raise ValueError("capability identity and ownership must be explicit")
        if self.capability_id.startswith("service."):
            raise ValueError("capability identity cannot masquerade as a service identity")
        if self.durable_state_owner != "MAMMOTH":
            raise ValueError("durable persistence authority must remain Mammoth")
        if self.reliability_observer != "RSF":
            raise ValueError("reliability authority must remain RSF")
        if self.final_certification_authority != "EXTERNAL_RAF":
            raise ValueError("final certification authority must remain external RAF")
