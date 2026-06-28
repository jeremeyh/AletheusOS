class CardClassifier:
    """Classifies whether the upload appears to be a card, memorabilia, Funko, etc."""

    def classify(self, text: str = "") -> dict:
        lower = (text or "").lower()

        if "funko" in lower or "pop" in lower:
            return {"category": "Funko Pop", "confidence": 0.75}

        if "helmet" in lower or "jersey" in lower or "signed" in lower:
            return {"category": "Memorabilia", "confidence": 0.7}

        return {"category": "Trading Card", "confidence": 0.6}
