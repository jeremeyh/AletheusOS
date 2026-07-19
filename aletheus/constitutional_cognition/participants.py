"""Reference participants for Constitutional Cognition™."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .models import EngineContribution


class FunctionalCognitiveParticipant:
    """Adapt a bounded callable into a cognitive participant."""

    def __init__(
        self,
        *,
        engine_id: str,
        evaluator: Callable[
            [dict[str, Any]],
            EngineContribution,
        ],
    ) -> None:
        if not engine_id.strip():
            raise ValueError(
                "engine_id may not be blank."
            )

        self.engine_id = engine_id
        self._evaluator = evaluator

    def evaluate(
        self,
        payload: dict[str, Any],
    ) -> EngineContribution:
        return self._evaluator(payload)
