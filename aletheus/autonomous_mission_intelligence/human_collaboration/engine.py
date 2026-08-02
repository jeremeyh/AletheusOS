from __future__ import annotations

from typing import Any, ClassVar

from .helpers import digest


class Engine:
    VERSION: ClassVar[str] = "34.15.0"

    def route(
        self, request_id: str, risk_score: float, delegates: list[str]
    ) -> dict[str, Any]:
        if not request_id.strip():
            raise ValueError("Request identity is required.")
        level = (
            "EXECUTIVE"
            if risk_score >= 0.8
            else "OWNER" if risk_score >= 0.5 else "REVIEWER"
        )
        payload = {
            "requestId": request_id,
            "approvalLevel": level,
            "delegates": sorted(set(delegates)),
            "state": "AWAITING_HUMAN_DECISION",
            "executionAuthorized": False,
            "escalationRequired": risk_score >= 0.5,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(
        self,
        request_id: str,
        risk_score: float = 0.0,
        delegates: list[str] | None = None,
    ) -> dict[str, Any]:
        return self.route(request_id, risk_score, delegates or [])
