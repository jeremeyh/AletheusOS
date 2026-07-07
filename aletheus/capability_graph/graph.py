from .models import CapabilityEdge, CapabilityNode


class CapabilityGraph:

    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node: CapabilityNode):
        self.nodes[node.id] = node

    def connect(
        self,
        source: str,
        target: str,
        relationship: str = "depends_on",
    ):
        self.edges.append(
            CapabilityEdge(
                source=source,
                target=target,
                relationship=relationship,
            )
        )

    def node_count(self):
        return len(self.nodes)

    def edge_count(self):
        return len(self.edges)

    def dependencies(self, node_id):
        return [
            edge.target
            for edge in self.edges
            if edge.source == node_id
        ]

    def reverse_dependencies(self, node_id):
        return [
            edge.source
            for edge in self.edges
            if edge.target == node_id
        ]
