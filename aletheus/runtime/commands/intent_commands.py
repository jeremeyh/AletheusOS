from __future__ import annotations

from typing import Any

from aletheus.runtime.context import RuntimeContext


def register_intent_commands(runtime: Any) -> None:
    """
    Register Intent Runtime commands with the runtime command bus.

    Intent commands are extracted from runtime/core.py to preserve
    Small Core, Massive Capability.
    """

    runtime.commands.register("intent.stats", lambda context: intent_stats(runtime, context))
    runtime.commands.register("intent.list", lambda context: intent_list(runtime, context))


def intent_stats(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "intent_runtime",
        runtime.intent_runtime.statistics(),
    )

    return context


def intent_list(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "intents",
        [
            {
                "intent_id": intent.intent_id,
                "mission": intent.mission,
                "objective": intent.objective,
                "beneficiary": intent.beneficiary,
                "priority": intent.priority.value,
                "status": intent.status.value,
                "source": intent.source,
                "steward": intent.steward,
            }
            for intent in runtime.intent_runtime.active()
        ],
    )

    return context
