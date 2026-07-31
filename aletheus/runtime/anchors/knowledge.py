"""
Knowledge Anchor Circuit

Genesis 8
"""

from .base import RuntimeAnchorCircuit


class KnowledgeAnchorCircuit(RuntimeAnchorCircuit):
    def attach(self):

        self.connected = True

        self.runtime.knowledge_anchor = self

        return self.status()

    def capabilities(self):

        return ["knowledge_graph", "semantic_search"]
