"""
Knowledge Graph Runtime

Genesis 13.37
"""


from .entities import EntityRegistry
from .relationships import RelationshipEngine



class KnowledgeGraph:


    def __init__(self):

        self.entities = EntityRegistry()

        self.relationships = RelationshipEngine()



    def snapshot(
        self
    ):


        return {


            "entities":

                len(
                    self.entities.entities
                ),


            "relationships":

                len(
                    self.relationships.relationships
                )

        }

