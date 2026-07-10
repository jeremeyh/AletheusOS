from __future__ import annotations

from typing import Any, Dict


class RuntimeRegistry:

    def __init__(self):
        self.version = "2.0.0"

        self.domains = {}
        self.services = {}
        self.components = {}

    def register_domain(
        self,
        name: str,
        instance: Any,
    ):
        self.domains[name] = instance

    def register_service(
        self,
        name: str,
        instance: Any,
    ):
        self.services[name] = instance

    def register_component(
        self,
        name: str,
        metadata: Dict[str, Any],
    ):
        self.components[name] = metadata

    def snapshot(self):

        return {
            "version": self.version,
            "healthy": True,

            "domains": list(
                self.domains.keys()
            ),

            "services": list(
                self.services.keys()
            ),

            "components": list(
                self.components.keys()
            ),

            "domain_count": len(
                self.domains
            ),

            "service_count": len(
                self.services
            ),

            "component_count": len(
                self.components
            ),
        }


runtime_registry = RuntimeRegistry()
