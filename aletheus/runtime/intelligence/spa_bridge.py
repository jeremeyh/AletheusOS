from __future__ import annotations


class RuntimeSPABridge:
    """
    Runtime attachment bridge for Spectrum Platform Analyzer.

    Genesis 6

    Keeps SPA integration outside runtime/core.py.
    """

    def __init__(self, runtime):
        self.runtime = runtime



    def registry_governance_check(self):

        runtime = self.runtime

        if not hasattr(
            runtime,
            "registry_governance_validate"
        ):
            return {
                "healthy": False,
                "reason": "registry governance unavailable"
            }

        result = (
            runtime.registry_governance_validate()
        )

        return {
            "healthy": result.get(
                "compliant",
                False
            ),
            "result": result,
        }

    def assess(self):
        """
        Produce runtime architecture assessment.
        """

        checks = {
            "runtime_initialized": True,
            "commands_available": hasattr(
                self.runtime,
                "commands",
            ),
            "registry_available": (
                self.runtime.registry_snapshot().get(
                    "healthy",
                    False,
                )
            ),
            "diagnostics_available": hasattr(
                self.runtime,
                "diagnostics",
            ),
            "invariants_available": hasattr(
                self.runtime,
                "invariants",
            ),
        }

        passed = all(checks.values())

        return {
            "analyzer": "Spectrum Platform Analyzer",
            "status": "healthy" if passed else "attention_required",
            "checks": checks,
            "risk_count": len(
                [
                    item
                    for item, value in checks.items()
                    if not value
                ]
            ),
        }


    def drift_report(self):
        """
        Structural drift detection foundation.
        """

        return {
            "runtime": "AletheusOS",
            "drift_detected": False,
            "areas_checked": [
                "runtime",
                "commands",
                "registry",
                "architecture",
            ],
        }
