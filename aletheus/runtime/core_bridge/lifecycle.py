from aletheus.runtime.core_shim import RuntimeCoreShim

from .models import CoreLifecycleBridgeReport


class CoreLifecycleBridge:
    """
    Core Lifecycle Bridge™

    Transitional bridge for moving lifecycle responsibility out of
    runtime/core.py and into the Runtime Lifecycle Manager and Boot Pipeline.

    Temporary by design.
    """

    def __init__(self):
        self.shim = RuntimeCoreShim()
        self.report = self.shim.bootstrap()
        self.services = self.shim.services

    def boot(self):
        lifecycle = self.services["lifecycle"]
        boot_pipeline = self.services["boot_pipeline"]

        lifecycle.transition(
            "booting",
            "Core Lifecycle Bridge requested boot.",
        )

        boot_report = boot_pipeline.execute()

        if boot_report.status == "ready":
            lifecycle.transition(
                "ready",
                "Boot Pipeline completed successfully.",
            )
            lifecycle.transition(
                "running",
                "Runtime accepted control after boot.",
            )

            status = "running"

        else:
            lifecycle.transition(
                "recovering",
                "Boot Pipeline did not reach ready state.",
            )

            status = "recovering"

        return CoreLifecycleBridgeReport(
            status=status,
            lifecycle_state=lifecycle.state.name,
            boot_status=boot_report.status,
            services=sorted(self.services.keys()),
        )

    def health(self):
        lifecycle = self.services["lifecycle"]

        return {
            "status": lifecycle.state.name,
            "services": sorted(self.services.keys()),
            "lifecycle": lifecycle.health(),
        }
