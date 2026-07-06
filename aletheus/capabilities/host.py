from __future__ import annotations

from typing import Dict, List

from aletheus.capabilities.contract import (
    CapabilityHealthReport,
    CapabilityMetadata,
    CapabilityRequest,
    CapabilityResult,
    RuntimeCapability,
)


class CapabilityHost:
    """
    Runtime host for installable AletheusOS capabilities.

    The host owns capability installation and lookup. It does not know
    capability implementation details.
    """

    def __init__(self) -> None:
        self._capabilities: Dict[str, RuntimeCapability] = {}

    def install(
        self,
        capability: RuntimeCapability,
        runtime=None,
    ) -> None:
        metadata = capability.metadata()

        if metadata.capability_id in self._capabilities:
            raise ValueError(
                f"Capability '{metadata.capability_id}' is already installed."
            )

        capability.register(runtime)
        self._capabilities[metadata.capability_id] = capability

    def uninstall(
        self,
        capability_id: str,
    ) -> None:
        capability = self._capabilities.get(capability_id)

        if capability:
            capability.stop()

        self._capabilities.pop(capability_id, None)

    def get(
        self,
        capability_id: str,
    ) -> RuntimeCapability | None:
        return self._capabilities.get(capability_id)

    def exists(
        self,
        capability_id: str,
    ) -> bool:
        return capability_id in self._capabilities

    def all(self) -> List[RuntimeCapability]:
        return list(self._capabilities.values())

    def metadata(self) -> List[CapabilityMetadata]:
        return [
            capability.metadata()
            for capability in self._capabilities.values()
        ]

    def health(self) -> List[CapabilityHealthReport]:
        return [
            capability.health()
            for capability in self._capabilities.values()
        ]

    def start_all(self) -> None:
        for capability in self._capabilities.values():
            capability.start()

    def stop_all(self) -> None:
        for capability in reversed(
            list(self._capabilities.values())
        ):
            capability.stop()

    def execute(
        self,
        request: CapabilityRequest,
    ) -> CapabilityResult:
        capability = self.get(request.capability_id)

        if capability is None:
            return CapabilityResult(
                capability_id=request.capability_id,
                action=request.action,
                success=False,
                error="Capability is not installed.",
            )

        return capability.execute(request)

    def summary(self) -> dict:
        return {
            "installed_capabilities": len(self._capabilities),
            "capabilities": [
                {
                    "id": metadata.capability_id,
                    "name": metadata.name,
                    "version": metadata.version,
                    "owner_kernel": metadata.owner_kernel,
                    "provider": metadata.provider,
                    "tags": metadata.tags,
                }
                for metadata in self.metadata()
            ],
        }
