from __future__ import annotations

from typing import Any

from aletheus.runtime.context import RuntimeContext


def register_memory_commands(runtime: Any) -> None:
    """
    Register memory, knowledge, semantic, graph, reasoning, and decision
    commands with the runtime command bus.

    This module is part of Genesis 6 core decomposition. It removes
    memory/knowledge-oriented command handlers from runtime/core.py while
    preserving runtime behavior.
    """
    runtime.commands.register("memory.mesh.store", lambda context: memory_mesh_store(runtime, context))
    runtime.commands.register("memory.mesh.retrieve", lambda context: memory_mesh_retrieve(runtime, context))
    runtime.commands.register("memory.mesh.search", lambda context: memory_mesh_search(runtime, context))
    runtime.commands.register("memory.mesh.restore", lambda context: memory_mesh_restore(runtime, context))
    runtime.commands.register("memory.mesh.replicate", lambda context: memory_mesh_replicate(runtime, context))
    runtime.commands.register("memory.mesh.sync", lambda context: memory_mesh_sync(runtime, context))
    runtime.commands.register("memory.mesh.history", lambda context: memory_mesh_history(runtime, context))
    runtime.commands.register("memory.mesh.cache", lambda context: memory_mesh_cache(runtime, context))
    runtime.commands.register("knowledge.entity.create", lambda context: kg_entity_create(runtime, context))
    runtime.commands.register("knowledge.entity.update", lambda context: kg_entity_update(runtime, context))
    runtime.commands.register("knowledge.entity.delete", lambda context: kg_entity_delete(runtime, context))
    runtime.commands.register("knowledge.relationship.create", lambda context: kg_relationship_create(runtime, context))
    runtime.commands.register("knowledge.relationship.delete", lambda context: kg_relationship_delete(runtime, context))
    runtime.commands.register("knowledge.search", lambda context: kg_search(runtime, context))
    runtime.commands.register("knowledge.graph", lambda context: kg_graph(runtime, context))
    runtime.commands.register("knowledge.neighbors", lambda context: kg_neighbors(runtime, context))
    runtime.commands.register("knowledge.infer", lambda context: kg_infer(runtime, context))
    runtime.commands.register("knowledge.statistics", lambda context: kg_statistics(runtime, context))


def memory_mesh_store(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload
    result = runtime.memory_mesh.store(
        key=payload.get("key", "untitled"),
        value=payload.get("value"),
        namespace=payload.get("namespace", "global"),
        object_type=payload.get("object_type", "generic"),
        tags=payload.get("tags", []),
        owner=payload.get("owner", context.application),
        metadata=payload.get("metadata", {}),
    )
    context.add_result("memory_object", result)
    return context



def memory_mesh_retrieve(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload
    result = runtime.memory_mesh.retrieve(
        object_id=payload.get("object_id", ""),
        key=payload.get("key", ""),
        namespace=payload.get("namespace", "global"),
    )
    context.add_result("memory_object", result)
    return context



def memory_mesh_search(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload
    result = runtime.memory_mesh.search(
        query=payload.get("query", ""),
        tags=payload.get("tags", []),
        namespace=payload.get("namespace", ""),
    )
    context.add_result("results", result)
    return context



def memory_mesh_restore(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    result = runtime.memory_mesh.restore(context.payload.get("snapshot_id", ""))
    context.add_result("restore", result)
    return context



def memory_mesh_replicate(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload
    result = runtime.memory_mesh.replicate(
        object_id=payload.get("object_id", ""),
        target_node=payload.get("target_node", "primary"),
    )
    context.add_result("replication", result)
    return context



def memory_mesh_sync(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    result = runtime.memory_mesh.sync(context.payload.get("node", "distributed_fabric"))
    context.add_result("sync", result)
    return context



def memory_mesh_history(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    result = runtime.memory_mesh.history(context.payload.get("object_id", ""))
    context.add_result("history", result)
    return context



def memory_mesh_cache(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    result = runtime.memory_mesh.cache(context.payload.get("object_id", ""))
    context.add_result("cache", result)
    return context



def kg_entity_create(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload
    result = runtime.knowledge_graph.create_entity(
        name=payload.get("name", "Untitled Entity"),
        node_type=payload.get("node_type", "entity"),
        properties=payload.get("properties", {}),
        metadata=payload.get("metadata", {}),
    )
    context.add_result("entity", result)
    return context



def kg_entity_update(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload
    result = runtime.knowledge_graph.update_entity(
        node_id=payload.get("node_id", ""),
        properties=payload.get("properties", {}),
        metadata=payload.get("metadata", {}),
    )
    context.add_result("entity", result)
    return context



def kg_entity_delete(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    result = runtime.knowledge_graph.delete_entity(context.payload.get("node_id", ""))
    context.add_result("entity", result)
    return context



def kg_relationship_create(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload
    result = runtime.knowledge_graph.create_relationship(
        source_id=payload.get("source_id", ""),
        target_id=payload.get("target_id", ""),
        relationship_type=payload.get("relationship_type", "related_to"),
        properties=payload.get("properties", {}),
    )
    context.add_result("relationship", result)
    return context



def kg_relationship_delete(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    result = runtime.knowledge_graph.delete_relationship(context.payload.get("relationship_id", ""))
    context.add_result("relationship", result)
    return context



def kg_search(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload
    result = runtime.knowledge_graph.search(
        query=payload.get("query", ""),
        node_type=payload.get("node_type", ""),
    )
    context.add_result("results", result)
    return context



def kg_graph(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("graph", runtime.knowledge_graph.graph())
    return context



def kg_neighbors(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload
    result = runtime.knowledge_graph.neighbors(
        node_id=payload.get("node_id", ""),
        direction=payload.get("direction", "both"),
    )
    context.add_result("neighbors", result)
    return context



def kg_infer(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("inference", runtime.knowledge_graph.infer())
    return context



def kg_statistics(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("knowledge_graph_stats", ((runtime.knowledge_graph.stats() if hasattr(runtime.knowledge_graph, 'stats') else runtime.knowledge_graph.statistics() if hasattr(runtime.knowledge_graph, 'statistics') else {'status': getattr(runtime.knowledge_graph, 'status', 'unknown')}) if hasattr(runtime.knowledge_graph, "stats") else runtime.knowledge_graph.statistics()))
    return context

