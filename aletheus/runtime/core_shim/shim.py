from aletheus.runtime.composition import RuntimeCompositionRoot

from .models import RuntimeShimReport


class RuntimeCoreShim:
    """
    Runtime Core Shim™

    Transitional compatibility layer.

    Bridges the legacy runtime core to the new
    Runtime Composition Root.

    Temporary by design.
    """

    def __init__(self):
        self.root = RuntimeCompositionRoot()
        self.runtime = None

    def bootstrap(self):

        self.runtime = self.root.build()

        return RuntimeShimReport(
            status="ready",
            delegated_services=sorted(
                self.runtime.services.keys()
            ),
        )

    @property
    def services(self):
        if self.runtime is None:
            self.bootstrap()

        return self.runtime.services
