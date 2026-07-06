from __future__ import annotations

from typing import Dict, Optional

from .models import (
    Intent,
    IntentStatus,
)

from aletheus.unified_cognitive_index.core import (
    uci_service,
)
from aletheus.unified_cognitive_index.models import (
    UCINode,
    UCINodeType,
)


class IntentRuntime:
    """
    Intent Runtime

    Every meaningful operation inside AletheusOS should
    originate from an Intent.

    Intent answers:

        Why are we doing this?

    before the platform decides

        How should it be done?
    """

    def __init__(self):

        self._active: Dict[str, Intent] = {}

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register(
        self,
        intent: Intent,
    ) -> None:

        self._active[intent.intent_id] = intent

        uci_service.publish_node(
            UCINode(
                node_id=intent.intent_id,
                node_type=UCINodeType.INTENT,
                title=intent.mission,
                description=intent.objective,
                tags=[
                    "intent",
                    intent.priority.value,
                    intent.status.value,
                ],
            )
        )

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    def get(
        self,
        intent_id: str,
    ) -> Optional[Intent]:

        return self._active.get(intent_id)

    def active(self):

        return list(self._active.values())

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def activate(
        self,
        intent_id: str,
    ):

        intent = self.get(intent_id)

        if intent:

            intent.status = IntentStatus.ACTIVE

    def complete(
        self,
        intent_id: str,
    ):

        intent = self.get(intent_id)

        if intent:

            intent.status = IntentStatus.COMPLETED

    def cancel(
        self,
        intent_id: str,
    ):

        intent = self.get(intent_id)

        if intent:

            intent.status = IntentStatus.CANCELLED

    # --------------------------------------------------
    # Metrics
    # --------------------------------------------------

    def statistics(self):

        return {
            "active_intents": len(self._active),
            "completed": len(
                [
                    i
                    for i in self._active.values()
                    if i.status == IntentStatus.COMPLETED
                ]
            ),
            "cancelled": len(
                [
                    i
                    for i in self._active.values()
                    if i.status == IntentStatus.CANCELLED
                ]
            ),
        }


intent_runtime = IntentRuntime()
