"""
Graph Storage

Genesis 14.6
"""


class KnowledgeGraph:


    def __init__(self):

        self.nodes = {}

        self.edges = []



    def add_node(
        self,
        node
    ):

        self.nodes[
            node.entity_id
        ] = node

