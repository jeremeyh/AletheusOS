"""
Hawk A•eye Vision Engine

Genesis 13.36
"""

from .condition import ConditionAnalyzer
from .matching import VisualMatchingEngine
from .ocr import CollectibleOCREngine
from .recognition import ObjectRecognitionEngine
from .signatures import SignatureAnalyzer


class HawkAEyeEngine:
    def __init__(self):

        self.recognition = ObjectRecognitionEngine()

        self.ocr = CollectibleOCREngine()

        self.matching = VisualMatchingEngine()

        self.condition = ConditionAnalyzer()

        self.signature = SignatureAnalyzer()

    def analyze(self, image):

        return {
            "recognition": self.recognition.detect(image),
            "ocr": self.ocr.extract(image),
            "condition": self.condition.analyze(image),
            "signature": self.signature.detect(image),
        }
