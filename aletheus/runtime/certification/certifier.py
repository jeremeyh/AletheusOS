from __future__ import annotations


class RuntimeCertifier:

    def __init__(self, runtime):
        self.runtime = runtime


    def certify(self):

        checks = {}


        # Boot
        checks["boot"] = (
            getattr(
                self.runtime,
                "state",
                None
            )
            is not None
        )


        # Commands
        if hasattr(
            self.runtime,
            "command_surface_audit"
        ):
            audit = (
                self.runtime.command_surface_audit()
            )

            checks["commands"] = audit.get(
                "healthy",
                False
            )

        else:
            checks["commands"] = False



        # Registry
        if hasattr(
            self.runtime,
            "registry_snapshot"
        ):
            registry = (
                self.runtime.registry_snapshot()
            )

            checks["registry"] = registry.get(
                "available",
                False
            )

        else:
            checks["registry"] = False



        # Invariants
        if hasattr(
            self.runtime,
            "invariants"
        ):
            checks["invariants"] = bool(
                self.runtime.invariants()
            )

        else:
            checks["invariants"] = False



        # SPA
        if hasattr(
            self.runtime,
            "spa"
        ):
            spa = self.runtime.spa.assess()

            checks["spa"] = (
                spa.get("risk_count",1) == 0
            )

        else:
            checks["spa"] = False



        certified = all(
            checks.values()
        )


        return {
            "certified": certified,
            "status":
                "CERTIFIED"
                if certified
                else "BLOCKED",
            "checks": checks,
        }
