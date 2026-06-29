from hawk_aeye.ocr.tesseract_engine import TesseractEngine
from hawk_aeye.parsers.card_parser import CardParser
from hawk_aeye.vision.vision_engine import VisionEngine


class HawkAEyeEngine:
    """
    Hawk A•Eye™

    Unified Asset DNA builder.

    Combines:
        • OCR text intelligence
        • Card parser metadata
        • Visual intelligence
    """

    @staticmethod
    def analyze(image_path):

        text = TesseractEngine.extract_text(image_path)

        card = CardParser.parse(text)

        vision = VisionEngine.analyze(image_path)

        if not card.get("parallel") and vision.get("parallel"):
            card["parallel"] = vision["parallel"]

        if vision.get("patch"):
            card["patch"] = True

        if vision.get("autograph"):
            card["autograph"] = True

        slab = vision.get("slab", {})

        if slab.get("graded"):
            card["grade_company"] = slab.get("company", "")

        return {
            "ocr_text": text,
            "card": card,
            "vision": vision,
        }
