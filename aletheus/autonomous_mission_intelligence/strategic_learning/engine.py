from __future__ import annotations

from typing import Any, ClassVar

from .helpers import clamp, digest


class Engine:
    VERSION: ClassVar[str] = "34.17.0"

    def learn(
        self,
        prior_weight: float,
        predicted: float,
        actual: float,
        learning_rate: float = 0.1,
    ) -> dict[str, Any]:
        bounded_rate = clamp(learning_rate)
        error = actual - predicted
        revised = clamp(prior_weight + bounded_rate * error)
        payload = {
            "priorWeight": round(prior_weight, 6),
            "predictionError": round(error, 6),
            "revisedWeight": round(revised, 6),
            "humanReviewRequired": abs(error) >= 0.5,
            "selfModificationAuthorized": False,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(
        self, prior_weight: float, predicted: float, actual: float
    ) -> dict[str, Any]:
        return self.learn(prior_weight, predicted, actual)
