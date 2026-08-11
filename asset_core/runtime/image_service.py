from pathlib import Path

PLACEHOLDER_IMAGE = "https://placehold.co/300x420?text=Card"


class AssetImageService:
    IMAGE_FIELDS = [
        "image_path",
        "front_image",
        "back_image",
    ]

    EXTENSIONS = [
        "jpg",
        "jpeg",
        "png",
        "webp",
    ]

    @classmethod
    def get_image(cls, asset):
        for field in cls.IMAGE_FIELDS:
            path = asset.get(field)

            if path and Path(path).exists():
                return path

        asset_id = asset.get("id")

        if asset_id is not None:
            for folder in [
                "uploads/assets",
                "uploads/scans",
                "uploads/thumbnails",
                "uploads/incoming",
            ]:
                for ext in cls.EXTENSIONS:
                    path = Path(folder) / f"{asset_id}.{ext}"

                    if path.exists():
                        return str(path)

        return PLACEHOLDER_IMAGE

    @classmethod
    def has_real_image(cls, asset):
        return cls.get_image(asset) != PLACEHOLDER_IMAGE
