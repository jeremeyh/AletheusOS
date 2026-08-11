class ParallelDetector:
    """Detects likely parallels and premium terms."""

    KNOWN_PARALLELS = [
        "Gold",
        "Black",
        "Silver",
        "Green",
        "Red",
        "Blue",
        "Purple",
        "Orange",
        "White Sparkle",
        "Color Blast",
        "Downtown",
        "Kaboom",
        "Manga",
        "Galactic",
        "Superfractor",
        "Finite",
        "Vinyl",
        "Pandora",
        "X-Fractor",
        "Refractor",
        "RPA",
        "Patch Auto",
        "Rookie Auto",
        "Auto",
    ]

    def detect(self, text: str = "") -> dict:
        lower = (text or "").lower()
        found = [p for p in self.KNOWN_PARALLELS if p.lower() in lower]
        return {
            "parallel": found[0] if found else "",
            "all_matches": found,
            "confidence": 0.8 if found else 0.0,
        }
