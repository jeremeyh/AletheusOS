from pathlib import Path
from shutil import copyfile
from datetime import datetime
import uuid


class ImageRepository:
    """
    CardHawkOS Image Repository

    Stores original uploaded images using stable filenames.
    """

    ROOT = Path("data/images")
    ORIGINALS = ROOT / "originals"
    THUMBNAILS = ROOT / "thumbnails"
    SCANS = ROOT / "scans"

    @classmethod
    def ensure_dirs(cls):
        cls.ORIGINALS.mkdir(parents=True, exist_ok=True)
        cls.THUMBNAILS.mkdir(parents=True, exist_ok=True)
        cls.SCANS.mkdir(parents=True, exist_ok=True)

    @classmethod
    def store_original(cls, source_path):

        cls.ensure_dirs()

        source = Path(source_path)
        suffix = source.suffix.lower() or ".jpg"

        filename = (
            f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_"
            f"{uuid.uuid4().hex[:10]}"
            f"{suffix}"
        )

        destination = cls.ORIGINALS / filename

        copyfile(
            source,
            destination,
        )

        return str(destination)
