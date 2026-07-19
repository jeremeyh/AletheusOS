"""Filesystem inventory provider for SPAN™."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable
import os

from ..evidence_store import EvidenceRecord
from .base import Provider, ProviderContext


DEFAULT_EXCLUDES = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}


class FilesystemProvider(Provider):
    name = "filesystem"
    version = "1.0.0"
    description = "Collect files, directories, sizes, and timestamps."

    def __init__(
        self,
        *,
        excludes: Iterable[str] = DEFAULT_EXCLUDES,
        include_hidden: bool = False,
    ) -> None:
        self.excludes = frozenset(excludes)
        self.include_hidden = include_hidden

    def _excluded(self, relative: Path) -> bool:
        for part in relative.parts:
            if part in self.excludes:
                return True
            if not self.include_hidden and part.startswith("."):
                return True
        return False

    def collect(self, context: ProviderContext):
        root = context.root.resolve()

        yield EvidenceRecord(
            kind="repository",
            provider=self.name,
            source=".",
            location=str(root),
            payload={"path": ".", "absolute_path": str(root)},
            tags=("filesystem", "repository"),
        )

        for current, directories, files in os.walk(root):
            current_path = Path(current)
            relative_dir = current_path.relative_to(root)

            directories[:] = sorted(
                directory
                for directory in directories
                if not self._excluded(relative_dir / directory)
            )

            if relative_dir != Path(".") and not self._excluded(relative_dir):
                stat = current_path.stat()
                yield EvidenceRecord(
                    kind="directory",
                    provider=self.name,
                    source=relative_dir.as_posix(),
                    location=str(current_path),
                    payload={
                        "path": relative_dir.as_posix(),
                        "modified_ns": stat.st_mtime_ns,
                    },
                    tags=("filesystem", "directory"),
                )

            for filename in sorted(files):
                path = current_path / filename
                relative = path.relative_to(root)
                if self._excluded(relative):
                    continue
                try:
                    stat = path.stat()
                except OSError:
                    continue

                suffix = path.suffix.lower()
                yield EvidenceRecord(
                    kind="file",
                    provider=self.name,
                    source=relative.as_posix(),
                    location=str(path),
                    payload={
                        "path": relative.as_posix(),
                        "name": path.name,
                        "suffix": suffix,
                        "size": stat.st_size,
                        "modified_ns": stat.st_mtime_ns,
                        "is_python": suffix == ".py",
                        "is_symlink": path.is_symlink(),
                    },
                    tags=("filesystem", "file", suffix.lstrip(".") or "no-extension"),
                )
