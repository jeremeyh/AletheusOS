"""
Universal Trust Intelligence Engine

Genesis 13.56
"""


from .authentication import AuthenticationEngine
from .custody import CustodyEngine
from .fraud import FraudDetectionEngine
from .identity import IdentityEngine
from .provenance import ProvenanceEngine
from .scoring import TrustScoringEngine


class TrustNetworkEngine:


    def __init__(self):

        self.identity = IdentityEngine()

        self.provenance = ProvenanceEngine()

        self.custody = CustodyEngine()

        self.authentication = AuthenticationEngine()

        self.fraud = FraudDetectionEngine()

        self.scoring = TrustScoringEngine()



    def evaluate(
        self,
        asset
    ):


        return {

            "trust":

                self.scoring.calculate(
                    asset
                )

        }

