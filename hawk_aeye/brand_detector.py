class BrandDetector:
    """Detects card/manufacturer brands from text."""

    KNOWN_BRANDS = [
        "Prizm", "Optic", "Select", "Phoenix", "Mosaic", "Donruss",
        "Donruss Elite", "National Treasures", "Flawless", "Immaculate",
        "Topps Chrome", "Bowman Chrome", "Bowman", "Topps Midnight",
        "Court Kings", "Obsidian", "Revolution", "Leaf", "Panini"
    ]

    def detect(self, text: str = "") -> dict:
        lower = (text or "").lower()
        for brand in self.KNOWN_BRANDS:
            if brand.lower() in lower:
                return {"brand": brand, "confidence": 0.85}
        return {"brand": "", "confidence": 0.0}
