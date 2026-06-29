from hawk_aeye.runtime.engine import HawkAEyeEngine


class HawkAEyeService:
    """
    Hawk A•Eye™

    High-level service used by the entire platform.

    This becomes the single public entry point for
    image analysis.
    """

    @staticmethod
    def analyze(image_path):

        result = HawkAEyeEngine.analyze(image_path)

        card = result["card"]
        vision = result["vision"]

        #
        # Confidence Score
        #

        confidence = 0

        if card.get("player"):
            confidence += 20

        if card.get("brand"):
            confidence += 15

        if card.get("set"):
            confidence += 15

        if card.get("year"):
            confidence += 10

        if card.get("grade"):
            confidence += 10

        if card.get("parallel"):
            confidence += 10

        if card.get("autograph"):
            confidence += 10

        if vision.get("parallel"):
            confidence += 5

        if vision.get("slab", {}).get("graded"):
            confidence += 5

        result["confidence"] = confidence

        return result
