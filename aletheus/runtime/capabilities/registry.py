class RuntimeCapabilityRegistry:
    """
    Runtime Capability Registry™

    Maintains the canonical runtime capability catalog.
    """

    def __init__(self):

        self._capabilities = {}

    def register(self, name, capability):

        self._capabilities[name] = capability

    def get(self, name):

        return self._capabilities[name]

    def exists(self, name):

        return name in self._capabilities

    def names(self):

        return tuple(sorted(self._capabilities.keys()))

    def count(self):

        return len(self._capabilities)

    def snapshot(self):

        return dict(self._capabilities)
