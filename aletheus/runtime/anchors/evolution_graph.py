"""
Anchor Evolution Knowledge Graph

Genesis 8.23

Tracks relationships between runtime evolution events.
"""


import time
import uuid


class AnchorEvolutionKnowledgeGraph:


    def __init__(self):

        self.nodes = {}
        self.relationships = []



    def add_node(
        self,
        node_type,
        data
    ):

        node_id = str(uuid.uuid4())


        self.nodes[node_id] = {

            "id":
                node_id,

            "type":
                node_type,

            "data":
                data,

            "created":
                time.time()

        }


        return node_id



    def connect(
        self,
        source,
        target,
        relationship
    ):

        edge = {

            "source":
                source,

            "target":
                target,

            "relationship":
                relationship,

            "created":
                time.time()

        }


        self.relationships.append(edge)


        return edge



    def record_evolution(
        self,
        anchor,
        proposal,
        verification
    ):


        anchor_node = self.add_node(
            "anchor",
            {
                "name":
                    anchor
            }
        )


        proposal_node = self.add_node(
            "proposal",
            proposal
        )


        verification_node = self.add_node(
            "verification",
            verification
        )


        self.connect(
            anchor_node,
            proposal_node,
            "evolved_by"
        )


        self.connect(
            proposal_node,
            verification_node,
            "validated_by"
        )


        return {

            "anchor":
                anchor_node,

            "proposal":
                proposal_node,

            "verification":
                verification_node

        }



    def query_anchor(
        self,
        anchor_name
    ):

        return [

            node

            for node
            in self.nodes.values()

            if (
                node["type"] == "anchor"
                and
                node["data"].get("name")
                == anchor_name
            )

        ]



    def snapshot(self):

        return {

            "nodes":
                len(self.nodes),

            "relationships":
                len(self.relationships)

        }
