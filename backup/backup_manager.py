from pathlib import Path
from zipfile import ZipFile
from datetime import datetime

class BackupManager:
    """Backup & Restore™ backup manager."""

    def __init__(self, root_dir=".", backup_dir="backups"):
        self.root_dir = Path(root_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, name=None):
        stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        zip_path = self.backup_dir / f"{name or 'cardhawk_backup'}_{stamp}.zip"
        exclude = {"venv", ".venv", "__pycache__", ".git", "backups"}

        with ZipFile(zip_path, "w") as z:
            for p in self.root_dir.rglob("*"):
                if any(part in exclude for part in p.parts):
                    continue
                if p.is_file():
                    z.write(p, arcname=str(p.relative_to(self.root_dir)))

        return str(zip_path)
