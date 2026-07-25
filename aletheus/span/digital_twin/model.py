from .node import TwinNode
from .relationship import Relationship


class ArchitecturalDigitalTwin:
    def __init__(self):
        self.nodes={}
        self.relationships=[]

    def add_node(self,node:TwinNode):
        self.nodes[node.identifier]=node

    def add_relationship(self,rel:Relationship):
        self.relationships.append(rel)

    def summary(self):
        return {
            "nodes":len(self.nodes),
            "relationships":len(self.relationships),
        }

    @classmethod
    def from_span(cls, providers=None, analyzers=None):
        twin=cls()
        if providers:
            for p in providers:
                twin.add_node(TwinNode(getattr(p,"name",p.__class__.__name__),"provider"))
        if analyzers:
            for a in analyzers:
                twin.add_node(TwinNode(getattr(a,"name",a.__class__.__name__),"analyzer"))
        return twin
