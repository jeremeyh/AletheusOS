"""
Hawk A•eye Intelligence Engine

Genesis 13.8
"""


from .recognition import CardRecognitionEngine
from .extraction import MetadataExtractionEngine
from .condition import ConditionAssessmentEngine



class HawkAEyeEngine:


    def __init__(self):

        self.recognition = (
            CardRecognitionEngine()
        )

        self.extraction = (
            MetadataExtractionEngine()
        )

        self.condition = (
            ConditionAssessmentEngine()
        )



    def analyze(
        self,
        image_reference
    ):

        return {

            "identity":
                self.recognition.identify(
                    image_reference
                ),

            "metadata":
                self.extraction.extract(
                    image_reference
                ),

            "condition":
                self.condition.evaluate(
                    image_reference
                )

        }

