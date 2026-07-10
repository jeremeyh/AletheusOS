"""
Compatibility Command Handlers

Genesis 7 Runtime Orchestration

Extracted from runtime/core.py.
"""

from aletheus.runtime.context import RuntimeContext


def compatibility_list(runtime, context: RuntimeContext):

    context.add_result(
        "compatibility",
        runtime.compat.snapshot(),
    )

    return context


def compatibility_statistics(runtime, context: RuntimeContext):

    context.add_result(
        "statistics",
        runtime.compat.statistics(),
    )

    return context


def compatibility_resolve(runtime, context: RuntimeContext):

    payload = context.payload

    result = runtime.compat.resolve(
        payload.get(
            "name",
            "",
        )
    )

    context.add_result(
        "resolution",
        result,
    )

    return context


def compatibility_contract(runtime, context: RuntimeContext):

    payload = context.payload

    result = runtime.compat.contract(
        payload.get(
            "name",
            "",
        )
    )

    context.add_result(
        "contract",
        result,
    )

    return context
