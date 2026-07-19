"""Public Constitutional Cognition Surface for AletheusOS."""

from __future__ import annotations

from typing import Any

from aletheus.constitutional_cognition import (
    CognitiveParticipant,
    MultiplicitousIntelligenceMesh,
    VirtueContext,
)


class CognitionSurface:
    """
    Stable application-facing interface to Constitutional Cognition™.

    Applications may register bounded cognitive participants and request
    cognition without depending directly on mesh implementation details.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        mesh: MultiplicitousIntelligenceMesh,
    ) -> None:
        self._mesh = mesh

    def register(
        self,
        participant: CognitiveParticipant,
        *,
        replace: bool = False,
    ) -> CognitiveParticipant:
        return self._mesh.register(
            participant,
            replace=replace,
        )

    def get(
        self,
        engine_id: str,
    ) -> CognitiveParticipant | None:
        return self._mesh.get(engine_id)

    def participants(
        self,
    ) -> tuple[CognitiveParticipant, ...]:
        return self._mesh.list()

    def execute(
        self,
        *,
        assertion_key: str,
        payload: dict[str, Any],
        virtue_context: VirtueContext | None = None,
    ):
        return self._mesh.execute(
            assertion_key=assertion_key,
            payload=payload,
            virtue_context=virtue_context,
        )

    def health(self) -> dict[str, Any]:
        return self._mesh.health()
