from __future__ import annotations

from typing import Any, ClassVar

from .helpers import digest


class Engine:
    VERSION: ClassVar[str] = "34.11.0"

    def adapt(
        self, strategy: dict[str, Any], evidence: dict[str, Any]
    ) -> dict[str, Any]:
        revised = dict(strategy)
        changes: list[str] = []
        if evidence.get("securityThreat"):
            revised["state"] = "PAUSED"
            changes.append("PAUSE_FOR_SECURITY_REVIEW")
        if evidence.get("resourceLoss"):
            revised["resourceMode"] = "REBALANCE_REQUIRED"
            changes.append("REALLOCATE_RESOURCES")
        if evidence.get("confidence", 1.0) < 0.5:
            revised["state"] = "EVIDENCE_REQUIRED"
            changes.append("EXPAND_EVIDENCE_COLLECTION")
        payload = {
            "revisedStrategy": revised,
            "changes": changes,
            "requiresHumanReview": bool(changes),
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(
        self, strategy: dict[str, Any], evidence: dict[str, Any]
    ) -> dict[str, Any]:
        return self.adapt(strategy, evidence)
