from __future__ import annotations

from .classifier import intent_classifier
from .models import Intent, new_intent_id


class IntentEngine:
    GENESIS = "45.1"
    VERSION = "1.0.0"

    def __init__(self) -> None:
        self.classifier = intent_classifier
        self._history: list[Intent] = []

    def resolve(
        self,
        *,
        identity: str,
        application: str,
        query: str,
        context: dict | None = None,
        constraints: list[str] | None = None,
        priority: str = "normal",
    ) -> Intent:
        classification = self.classifier.classify(query)

        intent = Intent(
            intent_id=new_intent_id(),
            identity=identity,
            application=application,
            query=query,
            intent_type=classification["intent_type"],
            objective=classification["objective"],
            capability_request=classification["capability_request"],
            priority=priority,
            confidence=classification["confidence"],
            constraints=constraints or [],
            expected_outcome=classification["expected_outcome"],
            context=context or {},
            constitutional_articles=[
                "Principle X",
                "Applications Request Capabilities",
                "Canonical Intelligence Objects",
                "Discovery Principle",
                "Founder's Humility Principle",
            ],
        )

        self._history.append(intent)
        return intent

    def history(self) -> list[dict]:
        return [intent.to_dict() for intent in self._history]

    def health(self) -> dict:
        return {
            "name": "Intent Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "classifier": self.classifier.health(),
            "intents": len(self._history),
        }

    def statistics(self) -> dict:
        counts: dict[str, int] = {}

        for intent in self._history:
            counts[intent.intent_type] = counts.get(intent.intent_type, 0) + 1

        return {
            "name": "Intent Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "intents": len(self._history),
            "intent_types": counts,
        }


intent_engine = IntentEngine()
