from PIL import Image
import pytesseract


class TesseractEngine:
    @staticmethod
    def extract_text(image_path: str) -> str:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
