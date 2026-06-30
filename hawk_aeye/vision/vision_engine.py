from hawk_aeye.vision.image_intelligence import ImageIntelligence


class VisionEngine:
    """
    Hawk A•Eye™ Vision Engine
    """

    @staticmethod
    def analyze(image_path):

        image = ImageIntelligence.analyze(image_path)

        if not image.get("exists"):
            return {
                "dominant_color": "Unknown",
                "parallel": None,
                "patch": False,
                "autograph": False,
                "slab": {
                    "graded": False,
                    "company": None,
                },
                "image": image,
            }

        return {
            "dominant_color": "Unknown",
            "parallel": None,
            "patch": False,
            "autograph": False,
            "slab": {
                "graded": False,
                "company": None,
            },
            "image": image,
        }
