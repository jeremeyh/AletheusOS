class RuntimeCapabilityDiscovery:
    """
    Runtime Capability Discovery™

    Discovers runtime capabilities from the dependency container.
    """

    def discover(self, container):

        capabilities = []

        for name in container.services():
            capabilities.append(name)

        return tuple(sorted(capabilities))
