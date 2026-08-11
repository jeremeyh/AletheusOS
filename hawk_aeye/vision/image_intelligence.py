from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageStat


class ImageIntelligence:
    """
    Hawk A•Eye™ Image Intelligence v1

    Lightweight visual analysis for uploaded card images.
    """

    @staticmethod
    def analyze(image_path):

        path = Path(image_path)

        if not path.exists():
            return {
                "exists": False,
                "error": "Image not found.",
            }

        with open(path, "rb") as f:
            image_hash = sha256(f.read()).hexdigest()

        image = Image.open(path).convert("RGB")

        width, height = image.size
        stat = ImageStat.Stat(image)

        brightness = sum(stat.mean) / 3

        aspect_ratio = round(width / height, 3) if height else 0

        orientation = "Portrait"

        if width > height:
            orientation = "Landscape"

        quality = "Good"

        if brightness < 50:
            quality = "Too Dark"

        elif brightness > 220:
            quality = "Too Bright"

        return {
            "exists": True,
            "image_path": str(path),
            "width": width,
            "height": height,
            "aspect_ratio": aspect_ratio,
            "orientation": orientation,
            "brightness": round(brightness, 2),
            "quality": quality,
            "sha256": image_hash,
            "confidence": 85,
        }
