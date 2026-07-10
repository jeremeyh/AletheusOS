from __future__ import annotations

from datetime import datetime


class Genesis6CertificationReport:

    VERSION = "1.0.0"


    def generate(self, runtime):

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


        return {
            "release": "Genesis 6",
            "report_version": self.VERSION,

            "timestamp": datetime.utcnow().isoformat(),

            "certified": certification.get(
                "ready",
                False
            ),

            "runtime_readiness": readiness,

            "architecture": {
                "registry": "Runtime Registry v2",
                "governance": True,
                "self_certification": True,
                "spa_integrated": True,
            },
        }
