import pytesseract
from hawk_aeye.preprocessing.image_processor import ImageProcessor
from PIL import Image


class TesseractEngine:
    """
    Hawk A•Eye OCR Engine
    """

    @staticmethod
    def extract_text(image_path):

        raw_image = Image.open(image_path)

        raw_text = pytesseract.image_to_string(
            raw_image,
            config="--oem 3 --psm 6",
        )

        processed_image = ImageProcessor.preprocess(image_path)

        processed_text = pytesseract.image_to_string(
            processed_image,
            config="--oem 3 --psm 6",
        )

        if len(processed_text.strip()) >= len(raw_text.strip()):
            return processed_text

        return raw_text
