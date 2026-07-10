from __future__ import annotations


class Genesis6FreezeReview:


    VERSION = "1.0.0"


    def review(self, runtime):

        readiness = (
            runtime.runtime_readiness()
            if hasattr(
                runtime,
                "runtime_readiness"
            )
            else {}
        )


        certification = (
            runtime.boot_certification_validate()
            if hasattr(
                runtime,
                "boot_certification_validate"
            )
            else {}
        )


        architecture = (
            runtime.architecture_governance_validate()
            if hasattr(
                runtime,
                "architecture_governance_validate"
            )
            else {}
        )


        registry = (
            runtime.registry.snapshot()
            if hasattr(
                runtime,
                "registry"
            )
            else {}
        )


        spa = (
            runtime.spa.assess()
            if hasattr(
                runtime,
                "spa"
            )
            else {}
        )


        risks = []


        if not certification.get(
            "ready",
            False
        ):
            risks.append(
                "boot_certification_failed"
            )


        if not architecture.get(
            "compliant",
            False
        ):
            risks.append(
                "architecture_noncompliant"
            )


        return {

            "release": "Genesis 6 Freeze Review",

            "version": self.VERSION,


            "approved": len(risks) == 0,


            "runtime_readiness": readiness,


            "registry": registry,


            "architecture": architecture,


            "boot_certification": certification,


            "spa": spa,


            "risks": risks,

        }
