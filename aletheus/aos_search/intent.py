from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SearchIntent:

    intent: str
    confidence: float
    category: str
    reasoning: str

    def to_dict(self):

        return {
            "intent": self.intent,
            "confidence": self.confidence,
            "category": self.category,
            "reasoning": self.reasoning,
        }


class IntentEngine:

    GENESIS = "21.8.1"
    VERSION = "1.0.0"

    def classify(
        self,
        query: str,
    ) -> SearchIntent:

        q = query.lower()

        if any(word in q for word in [
            "worth",
            "value",
            "price",
            "ebay",
            "card",
        ]):

            return SearchIntent(
                intent="marketplace_analysis",
                confidence=0.95,
                category="marketplace",
                reasoning="Marketplace terminology detected.",
            )

        if any(word in q for word in [
            "inventory",
            "stock",
            "available",
        ]):

            return SearchIntent(
                intent="inventory_lookup",
                confidence=0.94,
                category="enterprise",
                reasoning="Inventory terminology detected.",
            )

        return SearchIntent(
            intent="general_knowledge",
            confidence=0.80,
            category="knowledge",
            reasoning="Default knowledge classification.",
        )


intent_engine = IntentEngine()
