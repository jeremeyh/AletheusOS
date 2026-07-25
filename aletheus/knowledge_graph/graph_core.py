from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


def now() -> str:
    return utc_now_iso()


@dataclass
class GraphNode:
    name: str
    node_type: str = "entity"
    properties: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    updated_at: str = field(default_factory=now)

    def update(self, properties: dict[str, Any] | None = None, metadata: dict[str, Any] | None = None) -> None:
        if properties:
            self.properties.update(properties)
        if metadata:
            self.metadata.update(metadata)
        self.updated_at = now()

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class GraphRelationship:
    source_id: str
    target_id: str
    relationship_type: str
    properties: dict[str, Any] = field(default_factory=dict)
    relationship_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class InferenceRule:
    name: str
    description: str
    source_type: str = ""
    relationship_type: str = ""
    target_type: str = ""
    rule_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


class AletheusKnowledgeGraph:
    def __init__(self) -> None:
        self.version = "2.4.0"
        self.nodes: dict[str, GraphNode] = {}
        self.relationships: dict[str, GraphRelationship] = {}
        self.inference_rules: dict[str, InferenceRule] = {}

    def create_entity(
        self,
        name: str,
        node_type: str = "entity",
        properties: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        existing = self.find_entity_by_name(name)
        if existing:
            return existing.to_dict()

        node = GraphNode(
            name=name,
            node_type=node_type,
            properties=properties or {},
            metadata=metadata or {},
        )
        self.nodes[node.node_id] = node
        return node.to_dict()

    def update_entity(
        self,
        node_id: str,
        properties: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        node = self.nodes.get(node_id)
        if node is None:
            return {"error": f"Node not found: {node_id}"}
        node.update(properties=properties or {}, metadata=metadata or {})
        return node.to_dict()

    def delete_entity(self, node_id: str) -> dict[str, Any]:
        node = self.nodes.get(node_id)
        if node is None:
            return {"error": f"Node not found: {node_id}"}

        deleted = node.to_dict()
        self.nodes.pop(node_id)

        self.relationships = {
            rid: rel
            for rid, rel in self.relationships.items()
            if rel.source_id != node_id and rel.target_id != node_id
        }

        return deleted

    def find_entity_by_name(self, name: str) -> GraphNode | None:
        lower = name.lower()
        return next((node for node in self.nodes.values() if node.name.lower() == lower), None)

    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if source_id not in self.nodes:
            return {"error": f"Source node not found: {source_id}"}
        if target_id not in self.nodes:
            return {"error": f"Target node not found: {target_id}"}

        rel = GraphRelationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            properties=properties or {},
        )
        self.relationships[rel.relationship_id] = rel
        return rel.to_dict()

    def delete_relationship(self, relationship_id: str) -> dict[str, Any]:
        rel = self.relationships.get(relationship_id)
        if rel is None:
            return {"error": f"Relationship not found: {relationship_id}"}
        return self.relationships.pop(relationship_id).to_dict()

    def search(self, query: str = "", node_type: str = "") -> list[dict[str, Any]]:
        q = query.lower()
        results = []

        for node in self.nodes.values():
            text = f"{node.name} {node.node_type} {node.properties} {node.metadata}".lower()
            if (not q or q in text) and (not node_type or node.node_type == node_type):
                results.append(node.to_dict())

        return results

    def neighbors(self, node_id: str, direction: str = "both") -> dict[str, Any]:
        if node_id not in self.nodes:
            return {"error": f"Node not found: {node_id}"}

        outgoing = []
        incoming = []

        for rel in self.relationships.values():
            if rel.source_id == node_id:
                outgoing.append({
                    "relationship": rel.to_dict(),
                    "node": self.nodes[rel.target_id].to_dict(),
                })
            if rel.target_id == node_id:
                incoming.append({
                    "relationship": rel.to_dict(),
                    "node": self.nodes[rel.source_id].to_dict(),
                })

        if direction == "outgoing":
            incoming = []
        elif direction == "incoming":
            outgoing = []

        return {
            "node": self.nodes[node_id].to_dict(),
            "incoming": incoming,
            "outgoing": outgoing,
        }

    def graph(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "relationships": [rel.to_dict() for rel in self.relationships.values()],
            "inference_rules": [rule.to_dict() for rule in self.inference_rules.values()],
        }

    def add_inference_rule(
        self,
        name: str,
        description: str,
        source_type: str = "",
        relationship_type: str = "",
        target_type: str = "",
    ) -> dict[str, Any]:
        rule = InferenceRule(
            name=name,
            description=description,
            source_type=source_type,
            relationship_type=relationship_type,
            target_type=target_type,
        )
        self.inference_rules[rule.rule_id] = rule
        return rule.to_dict()

    def infer(self) -> dict[str, Any]:
        inferences = []

        for rule in self.inference_rules.values():
            for rel in self.relationships.values():
                source = self.nodes.get(rel.source_id)
                target = self.nodes.get(rel.target_id)

                if not source or not target:
                    continue

                source_match = not rule.source_type or source.node_type == rule.source_type
                rel_match = not rule.relationship_type or rel.relationship_type == rule.relationship_type
                target_match = not rule.target_type or target.node_type == rule.target_type

                if source_match and rel_match and target_match:
                    inferences.append({
                        "rule": rule.to_dict(),
                        "source": source.to_dict(),
                        "relationship": rel.to_dict(),
                        "target": target.to_dict(),
                        "inference": f"{source.name} {rel.relationship_type} {target.name}",
                    })

        return {
            "inferences": inferences,
            "count": len(inferences),
        }

    def bootstrap_cardhawk_graph(self) -> dict[str, Any]:
        cardhawk = self.create_entity("Card Hawk Foundation™", "application", {"domain": "collectibles"})
        asset_vault = self.create_entity("Asset Vault", "service", {"category": "asset_management"})
        portfolio = self.create_entity("Portfolio Engine", "service", {"category": "valuation"})
        marketplace = self.create_entity("Marketplace Intelligence", "service", {"category": "market_data"})
        hawk_aeye = self.create_entity("Hawk A•Eye™", "service", {"category": "visual_intelligence"})
        thorx = self.create_entity("THORᵡ", "service", {"category": "opportunity_rating"})

        for target in [asset_vault, portfolio, marketplace, hawk_aeye, thorx]:
            self.create_relationship(cardhawk["node_id"], target["node_id"], "owns")

        self.add_inference_rule(
            name="Application owns service",
            description="If an application owns a service, the service is part of that application's native capability stack.",
            source_type="application",
            relationship_type="owns",
            target_type="service",
        )

        return self.graph()

    def stats(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "nodes": len(self.nodes),
            "relationships": len(self.relationships),
            "inference_rules": len(self.inference_rules),
        }


knowledge_graph_core = AletheusKnowledgeGraph()
