class PlayerDetector:
    """Detects known player names from OCR/context text."""

    KNOWN_PLAYERS = [
        "Caleb Williams", "Rome Odunze", "Luther Burden", "Colston Loveland",
        "Garrett Wilson", "Isaiah Thomas", "Derrick Rose", "Noa Essengue",
        "Matas Buzelis", "Amen Thompson", "Ausar Thompson", "Will Anderson",
        "C.J. Stroud", "CJ Stroud", "Jalen Carter", "Austin Booker"
    ]

    def detect(self, text: str = "") -> dict:
        lower = (text or "").lower()
        for player in self.KNOWN_PLAYERS:
            if player.lower() in lower:
                return {"player": player, "confidence": 0.9}
        return {"player": "", "confidence": 0.0}
