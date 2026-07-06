from __future__ import annotations

from pathlib import Path


class FoundationReadiness:
    GENESIS = "30.0"
    VERSION = "1.0.0"

    def check(self):
        results = {}

        try:
            from aletheus.runtime import runtime_core
            results["runtime"] = runtime_core.status == "online"
            results["identity_engine"] = runtime_core.services.has("identity_engine")
            results["capability_engine"] = runtime_core.services.has("capability_engine")
            results["aos_search"] = runtime_core.services.has("aos_search")
        except Exception:
            results["runtime"] = False
            results["identity_engine"] = False
            results["capability_engine"] = False
            results["aos_search"] = False

        try:
            from aletheus.execution_engine import execution_engine
            results["execution_engine"] = execution_engine.health()["status"] == "healthy"
        except Exception:
            results["execution_engine"] = False

        try:
            from aletheus.foundation import aletheus_foundation
            aletheus_foundation.bootstrap_defaults()
            results["foundation_registry"] = (
                aletheus_foundation.statistics()["engines"] >= 10
            )
        except Exception:
            results["foundation_registry"] = False

        spec = Path("docs/specifications/aletheusos_architecture_spec_v1.md")
        results["architecture_spec"] = spec.exists()

        overall = all(results.values())

        return {
            "name": "AletheusOS Foundation Readiness",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "ready": overall,
            "checks": results,
        }


foundation_readiness = FoundationReadiness()
