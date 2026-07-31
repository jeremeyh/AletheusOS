class RuntimeDashboard:
    """
    Runtime Dashboard™

    Consolidated runtime operational snapshot.
    """

    def snapshot(self, runtime):

        boot = getattr(runtime, "boot_context", None)

        return {
            "lifecycle": getattr(runtime, "lifecycle", None),
            "services": len(runtime.services.list())
            if hasattr(runtime.services, "list")
            else None,
            "commands": len(runtime.commands.list())
            if hasattr(runtime.commands, "list")
            else None,
            "boot_phases": len(boot.executed) if boot else 0,
            "boot_skipped": len(boot.skipped) if boot else 0,
            "boot_time_ms": sum(boot.timings.values()) if boot else 0,
        }
