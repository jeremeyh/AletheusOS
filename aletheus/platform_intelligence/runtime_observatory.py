from .runtime_health import RuntimeHealthService
from .runtime_snapshot import RuntimeSnapshotService


class RuntimeObservatory:
    """
    Runtime Observatory™

    Unified façade for Platform Intelligence.

    Consumers should request runtime intelligence from the
    Observatory rather than individual services.
    """

    def __init__(self):
        self.health_service = RuntimeHealthService()
        self.snapshot_service = RuntimeSnapshotService()

    def health(self, runtime):
        return self.health_service.collect(runtime)

    def snapshot(self, runtime):
        return self.snapshot_service.collect(runtime)

    def overview(self, runtime):
        return {
            "health": self.health(runtime),
            "snapshot": self.snapshot(runtime),
        }
