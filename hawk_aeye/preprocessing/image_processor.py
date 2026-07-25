from PIL import Image, ImageEnhance, ImageOps


class ImageProcessor:
    """
    Hawk A•Eye™

    Safer image preprocessing before OCR.
    """

    @staticmethod
    def preprocess(image_path):

        image = Image.open(image_path)

        image = ImageOps.exif_transpose(image)

        image = image.convert("RGB")

        width, height = image.size

        image = image.resize(
            (width * 2, height * 2)
        )

        image = ImageOps.grayscale(image)

        image = ImageOps.autocontrast(image)

        image = ImageEnhance.Contrast(image).enhance(1.5)

        return image
