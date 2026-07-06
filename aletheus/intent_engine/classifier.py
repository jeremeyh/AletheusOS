from __future__ import annotations


class IntentClassifier:
    GENESIS = "45.1"
    VERSION = "1.0.0"

    def classify(self, query: str) -> dict:
        normalized = query.lower().strip()

        appraisal_terms = [
            "worth",
            "value",
            "appraise",
            "appraisal",
            "valuation",
            "market value",
            "fair value",
        ]

        sell_terms = [
            "sell",
            "hold",
            "move",
            "liquidate",
            "cash out",
        ]

        search_terms = [
            "find",
            "search",
            "look up",
            "locate",
        ]

        if any(term in normalized for term in appraisal_terms):
            return {
                "intent_type": "APPRAISE",
                "objective": "Determine collectible asset value.",
                "capability_request": "appraisal",
                "expected_outcome": "Explainable appraisal with confidence, reasoning, and supporting valuation signals.",
                "confidence": 0.95,
            }

        if any(term in normalized for term in sell_terms):
            return {
                "intent_type": "EVALUATE",
                "objective": "Evaluate whether an asset should be sold, held, or monitored.",
                "capability_request": "evaluation",
                "expected_outcome": "Strategic recommendation with risk, timing, and reasoning.",
                "confidence": 0.88,
            }

        if any(term in normalized for term in search_terms):
            return {
                "intent_type": "SEARCH",
                "objective": "Search for relevant information or assets.",
                "capability_request": "marketplace",
                "expected_outcome": "Relevant search results or marketplace observations.",
                "confidence": 0.82,
            }

        return {
            "intent_type": "ANALYZE",
            "objective": "Analyze the request and determine the most appropriate Foundation capability.",
            "capability_request": "evidence",
            "expected_outcome": "Structured analysis with available evidence and confidence.",
            "confidence": 0.65,
        }

    def health(self) -> dict:
        return {
            "name": "Intent Classifier",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
        }


intent_classifier = IntentClassifier()
