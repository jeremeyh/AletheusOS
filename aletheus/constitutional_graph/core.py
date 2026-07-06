from __future__ import annotations

from .edges import constitutional_edge_factory
from .nodes import constitutional_node_factory
from .registry import ConstitutionalGraphRegistry
from .traversal import ConstitutionalGraphTraversal


class ConstitutionalKnowledgeGraph:
    GENESIS = "20.0"
    VERSION = "0.1.0"

    def __init__(self):
        self.registry = ConstitutionalGraphRegistry()
        self.traversal = ConstitutionalGraphTraversal(self.registry)

    def add_node(self, node_type: str, label: str, data: dict | None = None):
        node = constitutional_node_factory.create(
            node_type,
            label,
            data,
        )
        self.registry.add_node(node)
        return node.to_dict()

    def connect(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
        data: dict | None = None,
    ):
        edge = constitutional_edge_factory.create(
            source_id,
            target_id,
            relationship,
            data,
        )
        self.registry.add_edge(edge)
        return edge.to_dict()

    def from_memory_record(self, memory_record: dict):
        memory_node = self.add_node(
            "constitutional_memory",
            memory_record["memory_id"],
            memory_record,
        )

        ledger_node = self.add_node(
            "constitutional_ledger",
            memory_record["ledger_id"],
            {
                "ledger_id": memory_record["ledger_id"],
                "decision_trace_id": memory_record["decision_trace_id"],
                "certification_id": memory_record["certification_id"],
            },
        )

        app_node = self.add_node(
            "application",
            memory_record["application"],
            {
                "application": memory_record["application"],
            },
        )

        relix_node = self.add_node(
            "relix_profile",
            memory_record["relix_profile"],
            {
                "relix_profile": memory_record["relix_profile"],
            },
        )

        self.connect(
            ledger_node["node_id"],
            memory_node["node_id"],
            "INDEXED_AS",
        )

        self.connect(
            app_node["node_id"],
            ledger_node["node_id"],
            "PRODUCED_LEDGER_ENTRY",
        )

        self.connect(
            ledger_node["node_id"],
            relix_node["node_id"],
            "USED_RELIX_PROFILE",
        )

        return {
            "memory": memory_node,
            "ledger": ledger_node,
            "application": app_node,
            "relix": relix_node,
        }

    def neighbors(self, node_id: str):
        return self.traversal.neighbors(node_id)

    def path_from(self, node_id: str, depth: int = 2):
        return self.traversal.path_from(node_id, depth)

    def health(self):
        stats = self.registry.statistics()

        return {
            "name": "Constitutional Knowledge Graph",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            **stats,
        }

    def statistics(self):
        return self.health()


constitutional_graph = ConstitutionalKnowledgeGraph()
