from __future__ import annotations

from .models import CapabilityDecision, new_decision_id
from .resolver import capability_resolver


class DecisionEngine:
    GENESIS = "21.6"
    VERSION = "1.0.0"

    def evaluate(
        self,
        identity_id: str,
        capability_id: str,
        intent: str = "",
        context: dict | None = None,
    ):

        allowed = capability_resolver.has(
            identity_id,
            capability_id,
        )

        if allowed:
            return CapabilityDecision(
                decision_id=new_decision_id(),
                identity_id=identity_id,
                capability_id=capability_id,
                intent=intent,
                result="APPROVED",
                reason="Capability resolved successfully.",
                confidence=1.0,
                context=context or {},
                constitutional_articles=[
                    "Article XLII",
                    "Article LV",
                ],
            )

        return CapabilityDecision(
            decision_id=new_decision_id(),
            identity_id=identity_id,
            capability_id=capability_id,
            intent=intent,
            result="DENIED",
            reason="Capability not granted.",
            confidence=1.0,
            context=context or {},
            constitutional_articles=[
                "Article XLIII",
                "Article LVII",
            ],
            alternatives=[
                "Request capability",
                "Request elevation",
                "Contact administrator",
            ],
        )

    def health(self):

        return {
            "status": "healthy",
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }


decision_engine = DecisionEngine()
