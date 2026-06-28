from hawk_aeye.ocr_runtime import OCRRuntime
from hawk_aeye.card_classifier import CardClassifier
from hawk_aeye.player_detector import PlayerDetector
from hawk_aeye.brand_detector import BrandDetector
from hawk_aeye.year_detector import YearDetector
from hawk_aeye.parallel_detector import ParallelDetector
from hawk_aeye.serial_detector import SerialDetector
from hawk_aeye.condition_estimator import ConditionEstimator
from hawk_aeye.asset_dna_builder import AssetDNABuilder

class VisionPipeline:
    """
    Hawk A⦿Eye™ Vision Pipeline.

    Alpha 0.7 assisted data-entry pipeline:
    image/context → OCR fallback → detectors → suggested Asset DNA™.
    """

    def __init__(self):
        self.ocr = OCRRuntime()
        self.classifier = CardClassifier()
        self.player = PlayerDetector()
        self.brand = BrandDetector()
        self.year = YearDetector()
        self.parallel = ParallelDetector()
        self.serial = SerialDetector()
        self.condition = ConditionEstimator()

    def analyze(self, image_path: str = "", context_text: str = "") -> dict:
        ocr = self.ocr.extract(image_path, context_text=context_text)
        text = ocr.get("text", "")

        results = {
            "image_path": image_path,
            "ocr": ocr,
            "category": self.classifier.classify(text),
            "player": self.player.detect(text),
            "brand": self.brand.detect(text),
            "year": self.year.detect(text),
            "parallel": self.parallel.detect(text),
            "serial": self.serial.detect(text),
            "condition": self.condition.estimate(image_path),
        }

        results["asset_dna"] = AssetDNABuilder.build(results)

        return results
