from __future__ import annotations

from .models import CapabilityResolution, new_resolution_id
from .registry import foundation_service_registry


class FoundationServiceRouter:
    GENESIS = "32.1"
    VERSION = "1.0.0"

    def resolve(self, requested_capability: str) -> CapabilityResolution:
        capability = foundation_service_registry.get(requested_capability)

        if capability and capability.enabled:
            return CapabilityResolution(
                resolution_id=new_resolution_id(),
                requested_capability=requested_capability,
                resolved=True,
                capability_id=capability.capability_id,
                name=capability.name,
                engine_id=capability.engine_id,
                execution_plan=capability.execution_plan,
                reason="Capability resolved through Foundation Service Bus.",
                confidence=1.0,
            )

        return CapabilityResolution(
            resolution_id=new_resolution_id(),
            requested_capability=requested_capability,
            resolved=False,
            reason="No enabled Foundation capability matched the request.",
            confidence=0.0,
            alternatives=[capability.capability_id for capability in foundation_service_registry.list()],
        )

    def health(self) -> dict:
        return {
            "name": "Foundation Service Router",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
        }


foundation_service_router = FoundationServiceRouter()
