"""
THORᵡ Intelligence Engine

Genesis 14.4
"""


from .qdef import QDEFEngine
from .ddef import DDEFEngine
from .strike_zone import StrikeZoneEngine
from .confidence import ConfidenceEngine
from .nuclear_cloud import NuclearCloudEngine
from .scoring import THORScoringEngine



class THORXEngine:


    def __init__(self):

        self.qdef = QDEFEngine()

        self.ddef = DDEFEngine()

        self.strike = StrikeZoneEngine()

        self.confidence = ConfidenceEngine()

        self.nuclear = NuclearCloudEngine()

        self.scoring = THORScoringEngine()



    def evaluate(
        self,
        asset
    ):


        return {

            "thor_score":

                0

        }

