from __future__ import annotations

from aletheus.boot_runtime import boot_runtime
from aletheus.contracts import PlatformComponentContract
from aletheus.self_assembly import self_assembly

from .models import PlatformLifecycleResult


class PlatformLifecycleManager(PlatformComponentContract):
    GENESIS = "15.0"
    VERSION = "0.1.0"

    OFFLINE = "OFFLINE"
    ASSEMBLING = "ASSEMBLING"
    PLANNING = "PLANNING"
    BOOTING = "BOOTING"
    VERIFYING = "VERIFYING"
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    SHUTTING_DOWN = "SHUTTING_DOWN"

    def __init__(self):
        self.state_value = self.OFFLINE
        self.last_report = None

    def boot(self):
        return self.start()

    def start(self):
        try:
            self.state_value = self.ASSEMBLING
            assembly = self_assembly.assemble()

            self.state_value = self.PLANNING
            plan = self_assembly.create_boot_plan()

            self.state_value = self.BOOTING
            report = boot_runtime.execute(plan)
            self.last_report = report.to_dict()

            self.state_value = self.VERIFYING

            if report.passed:
                self.state_value = self.ONLINE
                return PlatformLifecycleResult(
                    action="start",
                    state=self.state_value,
                    success=True,
                    message="Platform started successfully.",
                    metadata={
                        "assembly": assembly,
                        "boot_report": self.last_report,
                    },
                ).to_dict()

            self.state_value = self.DEGRADED
            return PlatformLifecycleResult(
                action="start",
                state=self.state_value,
                success=False,
                message="Platform started in degraded mode.",
                metadata={
                    "assembly": assembly,
                    "boot_report": self.last_report,
                },
            ).to_dict()

        except Exception as exc:
            self.state_value = self.DEGRADED
            return PlatformLifecycleResult(
                action="start",
                state=self.state_value,
                success=False,
                message=str(exc),
            ).to_dict()

    def shutdown(self):
        self.state_value = self.SHUTTING_DOWN
        self.state_value = self.OFFLINE
        return PlatformLifecycleResult(
            action="shutdown",
            state=self.state_value,
            success=True,
            message="Platform shutdown completed.",
        ).to_dict()

    def restart(self):
        self.shutdown()
        return self.start()

    def health(self):
        return {
            "name": "Platform Lifecycle Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online" if self.state_value == self.ONLINE else "available",
            "state": self.state_value,
        }

    def statistics(self):
        return {
            "name": "Platform Lifecycle Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "state": self.state_value,
            "has_last_report": self.last_report is not None,
        }

    def state(self):
        return self.state_value


platform_lifecycle = PlatformLifecycleManager()
