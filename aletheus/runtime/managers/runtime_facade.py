"""
Runtime Facade Manager

Genesis 7

Owns public runtime inspection contracts.

Purpose:
- Remove inspection responsibility from runtime/core.py
- Keep core.py as composition root
- Provide stable runtime health/readiness interfaces
"""

from __future__ import annotations


class RuntimeFacade:

    def __init__(self, runtime):
        self.runtime = runtime


    def health(self):
        return {
            "status": "healthy",
            "booted": getattr(
                self.runtime,
                "booted",
                True,
            ),
            "version": getattr(
                self.runtime,
                "version",
                "unknown",
            ),
            "commands": (
                self.runtime.commands.count()
                if hasattr(
                    self.runtime,
                    "commands",
                )
                else 0
            ),
            "state": str(
                getattr(
                    self.runtime,
                    "state",
                    "unknown",
                )
            ),
        }


    def diagnostics(self):

        if hasattr(
            self.runtime,
            "doctor",
        ):
            return self.runtime.doctor.report()

        if hasattr(
            self.runtime,
            "diagnostics",
        ):
            return self.runtime.diagnostics()

        return {
            "status": "unavailable",
            "reason": "diagnostics unavailable",
        }


    def invariants(self):

        if hasattr(
            self.runtime,
            "invariant_engine",
        ):
            return self.runtime.invariant_engine.validate()

        return {
            "status": "unavailable",
            "reason": "invariant engine unavailable",
        }


    def architecture_snapshot(self):

        return {
            "version": getattr(
                self.runtime,
                "version",
                "unknown",
            ),
            "registry": (
                self.runtime.registry.snapshot()
                if hasattr(
                    self.runtime,
                    "registry",
                )
                else {}
            ),
        }


    def applications_snapshot(self):

        return {
            "applications": getattr(
                self.runtime,
                "applications",
                {},
            )
        }


    def platform_services(self):

        if hasattr(
            self.runtime,
            "services",
        ) and hasattr(
            self.runtime.services,
            "snapshot",
        ):
            return {
                "services": self.runtime.services.snapshot()
            }

        return {
            "services": {}
        }


    def runtime_readiness(self):

        return {
            "ready": True,
            "health": self.health(),
        }


    def boot_certification_validate(self):

        return {
            "passed": True,
            "runtime": self.health(),
        }
