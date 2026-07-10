from __future__ import annotations

from datetime import datetime, timezone


class PlatformCouncil:

    def __init__(self, runtime):
        self.runtime = runtime


    def review(self):

        findings = []

        certification = (
            self.runtime.certify_runtime()
            if hasattr(
                self.runtime,
                "certify_runtime"
            )
            else {
                "certified": False
            }
        )


        manifest = (
            self.runtime.generate_release_manifest()
            if hasattr(
                self.runtime,
                "generate_release_manifest"
            )
            else {}
        )


        spa = (
            self.runtime.spa.assess()
            if hasattr(
                self.runtime,
                "spa"
            )
            else {}
        )


        if not certification.get(
            "certified",
            False
        ):
            findings.append(
                "runtime_not_certified"
            )


        if spa.get(
            "risk_count",
            1
        ) > 0:
            findings.append(
                "architecture_risk_detected"
            )


        if not manifest.get(
            "release_ready",
            False
        ):
            findings.append(
                "release_not_ready"
            )


        if len(findings) == 0:
            decision = "APPROVED"

        else:
            decision = (
                "APPROVED_WITH_WARNINGS"
                if certification.get(
                    "certified",
                    False
                )
                else "BLOCKED"
            )


        return {
            "council": "Aletheus Platform Council",
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "decision": decision,

            "approved":
                decision != "BLOCKED",

            "findings": findings,

            "confidence":
                100
                if decision == "APPROVED"
                else 85
                if decision == "APPROVED_WITH_WARNINGS"
                else 0,

            "certification": certification,

            "spa": spa,
        }
