from pathlib import Path
import os

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
        print("\n========== IMAGE DEBUG ==========")
        print("Current Working Directory:", os.getcwd())
        print("Asset ID:", asset.get("id"))

        for field in cls.IMAGE_FIELDS:
            value = asset.get(field)

            print(f"{field}: {value}")

            if value:
                p = Path(value)

                print("Resolved Path:", p.resolve())
                print("Exists:", p.exists())

                if p.exists():
                    print("RETURNING:", str(p))
                    return str(p)

        print("\nSearching fallback folders...")

        asset_id = asset.get("id")

        if asset_id is not None:
            for folder in (
                "uploads/assets",
                "uploads/scans",
                "uploads/thumbnails",
                "uploads/incoming",
            ):
                for ext in cls.EXTENSIONS:
                    p = Path(folder) / f"{asset_id}.{ext}"

                    print("Checking:", p)

                    if p.exists():
                        print("FOUND:", str(p))
                        return str(p)

        print("NO IMAGE FOUND")
        print("Using Placeholder")

        return PLACEHOLDER_IMAGE

    @classmethod
    def has_real_image(cls, asset):
        return cls.get_image(asset) != PLACEHOLDER_IMAGE
