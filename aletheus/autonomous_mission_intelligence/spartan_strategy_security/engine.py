from __future__ import annotations

from hmac import compare_digest
from typing import Any, ClassVar

from .helpers import digest


class Engine:
    VERSION: ClassVar[str] = "34.16.0"

    def inspect(
        self, plan: dict[str, Any], expected_digest: str | None = None
    ) -> dict[str, Any]:
        observed = digest(plan)
        integrity = (
            True
            if expected_digest is None
            else compare_digest(observed, expected_digest)
        )
        suspicious = any(
            key in plan
            for key in ("overrideConstitution", "disableHumanAuthority", "silentCommit")
        )
        payload = {
            "integrityVerified": integrity,
            "missionHijackIndicators": suspicious,
            "authorized": integrity and not suspicious,
            "controls": [
                "SIGNED_PLAN",
                "REPLAY_DEFENSE",
                "LEAST_PRIVILEGE",
                "HUMAN_AUTHORITY",
                "EVIDENCE_AUDIT",
            ],
            "executionAuthorized": False,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, plan: dict[str, Any]) -> dict[str, Any]:
        return self.inspect(plan)
