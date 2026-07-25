"""
Card Hawk Knowledge Graph Engine

Genesis 14.6
"""


from .collector import CollectorIntelligence
from .comparables import ComparableEngine
from .entities import EntityRegistry
from .graph import KnowledgeGraph
from .narratives import NarrativeEngine
from .relationships import RelationshipEngine


class KnowledgeGraphEngine:


    def __init__(self):

        self.entities = EntityRegistry()

        self.graph = KnowledgeGraph()

        self.relationships = RelationshipEngine()

        self.comparables = ComparableEngine()

        self.narratives = NarrativeEngine()

        self.collectors = CollectorIntelligence()



    def analyze(
        self,
        entity
    ):


        return {

            "status":

                "connected"

        }

