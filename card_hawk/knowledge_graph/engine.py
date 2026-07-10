"""
Card Hawk Knowledge Graph Engine

Genesis 14.6
"""


from .entities import EntityRegistry
from .graph import KnowledgeGraph
from .relationships import RelationshipEngine
from .comparables import ComparableEngine
from .narratives import NarrativeEngine
from .collector import CollectorIntelligence



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

