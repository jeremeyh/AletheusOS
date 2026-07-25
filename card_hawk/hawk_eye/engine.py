"""
Hawk A•eye Engine

Genesis 14.5
"""


from .condition import ConditionEngine
from .detection import DetectionEngine
from .fraud import FraudEngine
from .matching import MatchingEngine
from .ocr import OCREngine
from .recognition import RecognitionEngine


class HawkEyeEngine:


    def __init__(self):

        self.detection = DetectionEngine()

        self.ocr = OCREngine()

        self.recognition = RecognitionEngine()

        self.matching = MatchingEngine()

        self.condition = ConditionEngine()

        self.fraud = FraudEngine()



    def analyze(
        self,
        image
    ):


        return {

            "status":

                "processed"

        }

