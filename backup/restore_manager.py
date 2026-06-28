from pathlib import Path
from zipfile import ZipFile

class RestoreManager:
    """Restore manager for CardHawk OS™ snapshots."""

    @staticmethod
    def restore(zip_path, target_dir="."):
        target = Path(target_dir)
        with ZipFile(zip_path, "r") as z:
            z.extractall(target)
        return str(target)
