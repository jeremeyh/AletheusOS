from __future__ import annotations

from typing import Any

from aletheus.runtime.context import RuntimeContext


def register_uci_commands(runtime: Any) -> None:
    """
    Register Unified Cognitive Index commands with the runtime command bus.

    These handlers are intentionally outside runtime/core.py so the
    runtime core remains a lightweight composition root instead of a
    command-handler warehouse.
    """

    runtime.commands.register("uci.health", lambda context: uci_health(runtime, context))
    runtime.commands.register("uci.stats", lambda context: uci_stats(runtime, context))
    runtime.commands.register("uci.search", lambda context: uci_search(runtime, context))
    runtime.commands.register("uci.explain", lambda context: uci_explain(runtime, context))


def uci_health(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    from aletheus.unified_cognitive_index.health import health_report

    context.add_result("uci_health", health_report())
    return context


def uci_stats(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    from aletheus.unified_cognitive_index.health import statistics

    context.add_result("uci_statistics", statistics())
    return context


def uci_search(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    query = context.payload.get("query", "")

    result = runtime.uci.search(query)

    context.add_result(
        "uci_search",
        {
            "query": query,
            "total_nodes": result.total_nodes,
            "total_relationships": result.total_relationships,
            "nodes": [
                {
                    "node_id": node.node_id,
                    "node_type": node.node_type.value,
                    "title": node.title,
                    "description": node.description,
                    "source_system": node.source_system,
                    "intent_id": node.intent_id,
                    "tags": node.tags,
                }
                for node in result.nodes
            ],
        },
    )

    return context


def uci_explain(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    from aletheus.unified_cognitive_index.query import explain_node

    node_id = context.payload.get("node_id")

    context.add_result(
        "uci_explain",
        explain_node(node_id),
    )

    return context
