from __future__ import annotations

import hashlib
import os
from datetime import UTC, datetime
from pathlib import Path

from .models import FileRecord, ScanManifest
from .policy import RepairPolicy


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def hash_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


class RepositoryScanner:
    def __init__(self, policy: RepairPolicy) -> None:
        self.policy = policy

    def scan(self, root: Path) -> ScanManifest:
        root = root.expanduser().resolve()
        if not root.is_dir():
            raise NotADirectoryError(root)
        manifest = ScanManifest(root=str(root), generated_at=utc_now())
        for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
            current_path = Path(current)
            retained_dirs: list[str] = []
            for directory in dirs:
                relative = (current_path / directory).relative_to(root).as_posix()
                if self.policy.is_ignored_dir(directory):
                    manifest.ignored.append(relative + "/")
                else:
                    retained_dirs.append(directory)
            dirs[:] = retained_dirs

            for filename in files:
                path = current_path / filename
                relative = path.relative_to(root).as_posix()
                if self.policy.is_ignored_file(filename):
                    manifest.ignored.append(relative)
                    continue
                try:
                    if path.is_symlink():
                        manifest.ignored.append(relative + " [symlink]")
                        continue
                    stat = path.stat()
                    manifest.records[relative] = FileRecord(
                        relative_path=relative,
                        size=stat.st_size,
                        sha256=hash_file(path),
                        modified_ns=stat.st_mtime_ns,
                        file_class=self.policy.classify(relative),
                    )
                except (OSError, PermissionError) as exc:
                    manifest.errors.append(f"{relative}: {exc}")
        return manifest
