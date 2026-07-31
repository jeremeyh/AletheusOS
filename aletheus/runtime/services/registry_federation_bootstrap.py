"""
AletheusOS Registry Federation Bootstrap Hook

Genesis 12.6.2

Attaches federation intelligence during runtime startup.
"""

from aletheus.runtime.services.registry_federation_registration import (
    register_registry_federation,
)


class RegistryFederationBootstrap:
    def __init__(self, runtime):

        self.runtime = runtime
        self.service = None

    def initialize(self):

        self.service = register_registry_federation(self.runtime)

        return {"registry_federation": "initialized"}

    def health(self):

        if self.service:
            return self.service.health()

        return {"registry_federation": "inactive"}
