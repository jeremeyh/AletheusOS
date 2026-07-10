from __future__ import annotations


class KnowledgeGraphDomain:
    """
    Runtime adapter for Knowledge Graph capability.
    Genesis 6
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def entity_create(self, context):
        payload = context.payload
        result = self.runtime.knowledge_graph.create_entity(
            name=payload.get("name", "Unnamed Entity"),
            node_type=payload.get("node_type", "entity"),
            properties=payload.get("properties", {}),
            metadata=payload.get("metadata", {}),
        )
        context.add_result("entity", result)
        return context

    def entity_update(self, context):
        payload = context.payload
        result = self.runtime.knowledge_graph.update_entity(
            node_id=payload.get("node_id", ""),
            properties=payload.get("properties", {}),
            metadata=payload.get("metadata", {}),
        )
        context.add_result("entity", result)
        return context

    def entity_delete(self, context):
        result = self.runtime.knowledge_graph.delete_entity(
            context.payload.get("node_id", "")
        )
        context.add_result("entity", result)
        return context

    def relationship_create(self, context):
        payload = context.payload
        result = self.runtime.knowledge_graph.create_relationship(
            source_id=payload.get("source_id", ""),
            target_id=payload.get("target_id", ""),
            relationship_type=payload.get("relationship_type", ""),
            properties=payload.get("properties", {}),
        )
        context.add_result("relationship", result)
        return context

    def relationship_delete(self, context):
        result = self.runtime.knowledge_graph.delete_relationship(
            context.payload.get("relationship_id", "")
        )
        context.add_result("relationship", result)
        return context

    def search(self, context):
        payload = context.payload
        result = self.runtime.knowledge_graph.search(
            query=payload.get("query", ""),
            node_type=payload.get("node_type", ""),
        )
        context.add_result("results", result)
        return context

    def graph(self, context):
        context.add_result(
            "graph",
            self.runtime.knowledge_graph.graph(),
        )
        return context

    def neighbors(self, context):
        payload = context.payload
        result = self.runtime.knowledge_graph.neighbors(
            node_id=payload.get("node_id", ""),
            direction=payload.get("direction", "both"),
        )
        context.add_result("neighbors", result)
        return context

    def infer(self, context):
        context.add_result(
            "inference",
            self.runtime.knowledge_graph.infer(),
        )
        return context

    def bootstrap_cardhawk(self, context):
        context.add_result(
            "graph",
            self.runtime.knowledge_graph.bootstrap_cardhawk_graph(),
        )
        return context

    def statistics(self, context):
        context.add_result(
            "knowledge_graph_stats",
            {
                "version": self.runtime.knowledge_graph.version,
                "nodes": len(self.runtime.knowledge_graph.nodes),
                "relationships": len(self.runtime.knowledge_graph.relationships),
                "rules": len(self.runtime.knowledge_graph.inference_rules),
            },
        )
        return context
