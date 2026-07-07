from aletheus.runtime.discovery import RuntimeCapabilityDiscovery


class RuntimeCapabilitySynchronizer:
    """
    Runtime Capability Synchronizer™

    Synchronizes discovered container services into the runtime
    capability registry.
    """

    def __init__(self, discovery=None):

        self.discovery = discovery or RuntimeCapabilityDiscovery()

    def sync(self, container, registry):

        capabilities = self.discovery.discover(container)

        for capability in capabilities:
            registry.register(
                capability,
                container.resolve(capability),
            )

        return {
            "synced": len(capabilities),
            "capabilities": capabilities,
        }
