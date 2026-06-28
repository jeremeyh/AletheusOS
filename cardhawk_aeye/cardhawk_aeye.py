class CardHawkAEye:
    """
    CardHawk A•Eye™ orchestration layer.

    Keeps the classic A•Eye naming while delegating to Hawk A⦿Eye™ modules when available.
    """

    def analyze(self, image_path="", context_text=""):
        try:
            from hawk_aeye.vision_pipeline import VisionPipeline
            return VisionPipeline().analyze(image_path, context_text)
        except Exception:
            return {
                "image_path": image_path,
                "context_text": context_text,
                "asset_dna": {},
                "confidence": 0.0,
                "status": "Hawk A⦿Eye™ pipeline unavailable"
            }
