import re

class YearDetector:
    """Detects likely year from OCR/context text."""

    def detect(self, text: str = "") -> dict:
        matches = re.findall(r"\b(19[5-9]\d|20[0-4]\d)\b", text or "")
        if matches:
            return {"year": int(matches[0]), "confidence": 0.85}
        return {"year": None, "confidence": 0.0}
