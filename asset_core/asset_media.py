import shutil
import uuid
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AssetMedia:
    """
    Asset Media™

    Media vault for front/back images, details, receipts, certificates, and videos.
    """

    files: list[str] = field(default_factory=list)
    cover_image: str = ""

    def add_file(self, source_path: str, upload_dir: str = "uploads") -> str:
        src = Path(source_path)
        Path(upload_dir).mkdir(parents=True, exist_ok=True)

        if not src.exists():
            raise FileNotFoundError(f"Media source not found: {source_path}")

        dest = Path(upload_dir) / f"{uuid.uuid4().hex}_{src.name}"
        shutil.copy(src, dest)

        self.files.append(str(dest))

        if not self.cover_image:
            self.cover_image = str(dest)

        return str(dest)

    def set_cover(self, file_path: str):
        if file_path not in self.files:
            self.files.append(file_path)
        self.cover_image = file_path
