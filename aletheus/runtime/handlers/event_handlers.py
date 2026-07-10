"""
Event Command Handlers

Genesis 7 Runtime Orchestration

Extracted from runtime/core.py.
"""

from aletheus.runtime.context import RuntimeContext


def event_bootstrap(runtime, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "event_bus",
        runtime.event_bus_v3.bootstrap(),
    )
    return context


def event_publish(runtime, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload

    context.add_result(
        "event",
        runtime.event_bus_v3.publish(
            topic=payload.get(
                "topic",
                "runtime.event",
            ),
            payload=payload.get(
                "payload",
                {},
            ),
            publisher=payload.get(
                "publisher",
                "runtime",
            ),
            priority=payload.get(
                "priority",
                "normal",
            ),
        ),
    )

    return context


def event_subscribe(runtime, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload

    context.add_result(
        "subscription",
        runtime.event_bus_v3.subscribe(
            topic=payload.get("topic", ""),
            subscriber=payload.get("subscriber", ""),
        ),
    )

    return context


def event_unsubscribe(runtime, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload

    context.add_result(
        "subscription",
        runtime.event_bus_v3.unsubscribe(
            topic=payload.get("topic", ""),
            subscriber=payload.get("subscriber", ""),
        ),
    )

    return context


def event_history(runtime, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "history",
        runtime.event_bus_v3.history(
            context.payload.get("topic"),
        ),
    )

    return context


def event_replay(runtime, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "replay",
        runtime.event_bus_v3.replay(
            context.payload.get("topic", ""),
        ),
    )

    return context


def event_statistics(runtime, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "event_stats",
        runtime.event_bus_v3.statistics(),
    )

    return context
