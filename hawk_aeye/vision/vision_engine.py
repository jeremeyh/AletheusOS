from PIL import Image

from hawk_aeye.vision.color_detector import ColorDetector
from hawk_aeye.vision.parallel_detector import ParallelDetector
from hawk_aeye.vision.patch_detector import PatchDetector
from hawk_aeye.vision.auto_detector import AutoDetector
from hawk_aeye.vision.slab_detector import SlabDetector


class VisionEngine:
    """
    Hawk A•Eye™

    Computer Vision Intelligence Layer.

    This analyzes the IMAGE itself rather than OCR text.
    """

    @staticmethod
    def analyze(image_path):

        image = Image.open(image_path)

        return {

            "dominant_color":
                ColorDetector.detect(image),

            "parallel":
                ParallelDetector.detect(image),

            "patch":
                PatchDetector.detect(image),

            "autograph":
                AutoDetector.detect(image),

            "slab":
                SlabDetector.detect(image),

        }
