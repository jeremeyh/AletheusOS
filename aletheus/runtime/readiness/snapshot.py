from __future__ import annotations

from datetime import datetime


class RuntimeReadinessSnapshot:

    VERSION = "1.0.0"


    def generate(self, runtime):

        return {
            "engine": "Runtime Readiness Snapshot",
            "version": self.VERSION,

            "timestamp": datetime.utcnow().isoformat(),

            "runtime": {
                "initialized": True,
            },

            "registry": (
                runtime.registry.snapshot()
                if hasattr(runtime, "registry")
                else None
            ),

            "registry_compatibility": (
                runtime.registry_compatibility_validate()
                if hasattr(
                    runtime,
                    "registry_compatibility_validate"
                )
                else None
            ),

            "registry_governance": (
                runtime.registry_governance_validate()
                if hasattr(
                    runtime,
                    "registry_governance_validate"
                )
                else None
            ),

            "architecture_governance": (
                runtime.architecture_governance_validate()
                if hasattr(
                    runtime,
                    "architecture_governance_validate"
                )
                else None
            ),

            "boot_certification": (
                runtime.boot_certification_validate()
                if hasattr(
                    runtime,
                    "boot_certification_validate"
                )
                else None
            ),

            "spa": (
                runtime.spa.assess()
                if hasattr(
                    runtime,
                    "spa"
                )
                else None
            ),
        }
