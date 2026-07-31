"""
AletheusOS Registry Federation Service Registration

Genesis 12.6.1

Registers federation capability into runtime services.
"""

from aletheus.runtime.services.registry_federation_service import (
    RegistryFederationService,
)


def register_registry_federation(runtime):

    service = RegistryFederationService(runtime)

    service.initialize()

    if hasattr(runtime, "services"):
        runtime.services.register("registry_federation", service)

    return service
