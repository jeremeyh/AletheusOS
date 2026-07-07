from aletheus.runtime.container import RuntimeContainer


class RuntimeBuilder:
    """
    Runtime Builder™

    Responsible for assembling the runtime container prior
    to bootstrapping.
    """

    def __init__(self):

        self.container = RuntimeContainer()

        self._development = False
        self._enterprise = False
        self._clustered = False
        self._plugins = True

    def development(self, enabled=True):
        self._development = enabled
        return self

    def enterprise(self, enabled=True):
        self._enterprise = enabled
        return self

    def clustered(self, enabled=True):
        self._clustered = enabled
        return self

    def plugins(self, enabled=True):
        self._plugins = enabled
        return self

    def build(self):

        return {
            "container": self.container,
            "development": self._development,
            "enterprise": self._enterprise,
            "clustered": self._clustered,
            "plugins": self._plugins,
        }
