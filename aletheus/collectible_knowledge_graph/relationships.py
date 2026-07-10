"""
Relationship Engine

Genesis 13.37
"""


class RelationshipEngine:


    def __init__(self):

        self.relationships = []



    def connect(
        self,
        relationship
    ):

        self.relationships.append(
            relationship
        )


        return relationship

