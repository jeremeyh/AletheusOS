from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Node:
    label: str
    node_type: str
    properties: dict = field(default_factory=dict)
    node_id: str = field(default_factory=lambda: f"NODE-{uuid.uuid4().hex[:10].upper()}")

@dataclass
class Edge:
    source: str
    target: str
    relationship: str
    properties: dict = field(default_factory=dict)
    edge_id: str = field(default_factory=lambda: f"EDGE-{uuid.uuid4().hex[:10].upper()}")
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class KnowledgeGraph:
    """CardHawk Knowledge Graph™."""

    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, label, node_type, **properties):
        node = Node(label=label, node_type=node_type, properties=properties)
        self.nodes[node.node_id] = node
        return node

    def add_edge(self, source, target, relationship, **properties):
        edge = Edge(source=source, target=target, relationship=relationship, properties=properties)
        self.edges.append(edge)
        return edge

    def snapshot(self):
        return {
            "nodes": [n.__dict__ for n in self.nodes.values()],
            "edges": [e.__dict__ for e in self.edges],
        }
