"""
Card Hawk Acquisition Intelligence Engine

Genesis 13.6
"""

from .scoring import AcquisitionScoringEngine
from .targets import AcquisitionTargetLibrary


class CardHawkAcquisitionEngine:
    def __init__(self):

        self.scoring = AcquisitionScoringEngine()

        self.library = AcquisitionTargetLibrary()

    def evaluate(self, target):

        result = self.scoring.score(target)

        self.library.add(result)

        return result

    def opportunities(self):

        return self.library.list()
