"""
THORᵡ Intelligence Engine

Genesis 14.4
"""


from .confidence import ConfidenceEngine
from .ddef import DDEFEngine
from .nuclear_cloud import NuclearCloudEngine
from .qdef import QDEFEngine
from .scoring import THORScoringEngine
from .strike_zone import StrikeZoneEngine


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

