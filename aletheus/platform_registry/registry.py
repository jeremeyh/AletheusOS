from __future__ import annotations

from typing import Any

from aletheus.contracts import RegistryContract, PlatformComponentContract

from .models import PlatformComponentRecord


class PlatformRegistry(RegistryContract):
    GENESIS = "13.6"
    VERSION = "0.1.0"

    def __init__(self):
        self._components: dict[str, PlatformComponentRecord] = {}
        self._instances: dict[str, PlatformComponentContract] = {}

    def register(
        self,
        component_id: str,
        instance: PlatformComponentContract | None = None,
        name: str | None = None,
        version: str = "0.1.0",
        genesis: str = "unknown",
        critical: bool = False,
        dependencies: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        record = PlatformComponentRecord(
            component_id=component_id,
            name=name or component_id,
            version=version,
            genesis=genesis,
            critical=critical,
            dependencies=dependencies or [],
            metadata=metadata or {},
        )

        self._components[component_id] = record

        if instance is not None:
            self._instances[component_id] = instance

        return record

    def unregister(self, key: str):
        self._instances.pop(key, None)
        return self._components.pop(key, None)

    def get(self, key: str):
        return self._components.get(key)

    def get_instance(self, key: str):
        return self._instances.get(key)

    def list(self):
        return list(self._components.values())

    def health(self):
        return {
            "name": "Unified Platform Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "components": len(self._components),
            "instances": len(self._instances),
        }

    def statistics(self):
        return {
            "components": len(self._components),
            "critical": sum(1 for c in self._components.values() if c.critical),
            "with_instances": len(self._instances),
            "component_ids": sorted(self._components.keys()),
        }

    def verify(self):
        return {
            "verified": True,
            "components": len(self._components),
            "contract_instances": sum(
                1
                for instance in self._instances.values()
                if isinstance(instance, PlatformComponentContract)
            ),
        }
