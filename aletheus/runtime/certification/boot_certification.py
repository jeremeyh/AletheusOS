from __future__ import annotations


class BootCertification:
    VERSION = "1.0.0"

    def certify(self, runtime):

        checks = {}

        checks["registry"] = hasattr(runtime, "registry")

        checks["registry_compatibility"] = (
            runtime.registry_compatibility_validate().get("compatible", False)
            if hasattr(runtime, "registry_compatibility_validate")
            else False
        )

        checks["registry_governance"] = (
            runtime.registry_governance_validate().get("compliant", False)
            if hasattr(runtime, "registry_governance_validate")
            else False
        )

        checks["architecture_governance"] = (
            runtime.architecture_governance_validate().get("compliant", False)
            if hasattr(runtime, "architecture_governance_validate")
            else False
        )

        healthy = all(checks.values())

        return {
            "engine": "Boot Certification",
            "version": self.VERSION,
            "ready": healthy,
            "checks": checks,
        }
