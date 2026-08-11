import re
from pathlib import Path


class OCRRuntime:
    """
    Hawk A⦿Eye™ OCR Runtime.

    Alpha 0.7 uses filename/context text as a safe local fallback.
    Later versions can plug in pytesseract, OpenAI vision, or another OCR provider.
    """

    def extract(self, image_path: str, context_text: str = "") -> dict:
        name = Path(image_path).stem if image_path else ""
        combined = f"{name} {context_text}".replace("_", " ").replace("-", " ")
        combined = re.sub(r"\s+", " ", combined).strip()

        return {
            "text": combined,
            "confidence": 0.35 if combined else 0.0,
            "source": "filename_context_fallback",
        }
