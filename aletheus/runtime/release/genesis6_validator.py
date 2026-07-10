from __future__ import annotations


class Genesis6Validator:

    VERSION = "1.0.0"


    def validate(self, runtime):

        results = {}


        results["command_surface"] = (
            runtime.command_surface_audit()
            if hasattr(
                runtime,
                "command_surface_audit"
            )
            else {
                "healthy": False
            }
        )


        results["registry"] = (
            runtime.registry.snapshot()
            if hasattr(
                runtime,
                "registry"
            )
            else {
                "healthy": False
            }
        )


        results["registry_compatibility"] = (
            runtime.registry_compatibility_validate()
            if hasattr(
                runtime,
                "registry_compatibility_validate"
            )
            else {
                "compatible": False
            }
        )


        results["registry_governance"] = (
            runtime.registry_governance_validate()
            if hasattr(
                runtime,
                "registry_governance_validate"
            )
            else {
                "compliant": False
            }
        )


        results["architecture_governance"] = (
            runtime.architecture_governance_validate()
            if hasattr(
                runtime,
                "architecture_governance_validate"
            )
            else {
                "compliant": False
            }
        )


        results["boot_certification"] = (
            runtime.boot_certification_validate()
            if hasattr(
                runtime,
                "boot_certification_validate"
            )
            else {
                "ready": False
            }
        )


        results["readiness"] = (
            runtime.runtime_readiness()
            if hasattr(
                runtime,
                "runtime_readiness"
            )
            else {}
        )


        results["spa"] = (
            runtime.spa.assess()
            if hasattr(
                runtime,
                "spa"
            )
            else {}
        )


        results["freeze_review"] = (
            runtime.genesis6_freeze_review()
            if hasattr(
                runtime,
                "genesis6_freeze_review"
            )
            else {
                "approved": False
            }
        )


        failures = []


        if not results["boot_certification"].get(
            "ready",
            False
        ):
            failures.append(
                "boot_certification"
            )


        if not results["freeze_review"].get(
            "approved",
            False
        ):
            failures.append(
                "freeze_review"
            )


        return {
            "release": "Genesis 6",
            "validator_version": self.VERSION,
            "passed": len(failures) == 0,
            "failures": failures,
            "results": results,
        }
