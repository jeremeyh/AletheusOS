from __future__ import annotations

from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path

from .models import FileClass


@dataclass(slots=True)
class RepairPolicy:
    """Safety policy for repository repair.

    Deletion is never implied by classification. Known debris is quarantined unless
    the caller explicitly requests permanent deletion.
    """

    ignored_directory_names: set[str] = field(default_factory=lambda: {
        ".git", ".venv", "venv", "node_modules", "__pycache__",
        ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox",
    })
    ignored_file_patterns: tuple[str, ...] = (
        "*.pyc", "*.pyo", ".DS_Store", "Thumbs.db", "*.swp", "*.swo",
    )
    known_orphan_file_names: set[str] = field(default_factory=lambda: {
        "=END", ".sh", "cd",
    })
    known_orphan_patterns: tuple[str, ...] = (
        "*.tmp", "*.temp", "*.orig", "*.rej", "*~",
    )
    backup_patterns: tuple[str, ...] = (
        "*.backup", "*.bak", "*.before_*", "*.genesis*_backup",
        "*.runtime_boot_restored",
    )
    report_directory_names: set[str] = field(default_factory=lambda: {
        "reports", "runtime_state", "logs",
    })
    protected_prefixes: tuple[str, ...] = (
        ".git/", "aletheus/", "tests/", "docs/", "config/", "tools/",
        "nimble/", "card_hawk/",
    )

    @classmethod
    def default(cls) -> RepairPolicy:
        return cls()

    def is_ignored_dir(self, name: str) -> bool:
        return name in self.ignored_directory_names

    def is_ignored_file(self, name: str) -> bool:
        return any(fnmatch(name, pattern) for pattern in self.ignored_file_patterns)

    def is_known_orphan(self, relative_path: str, size: int) -> bool:
        path = Path(relative_path)
        if path.name in self.known_orphan_file_names:
            return size == 0 or path.name in {"=END", ".sh"}
        return any(fnmatch(path.name, pattern) for pattern in self.known_orphan_patterns)

    def classify(self, relative_path: str) -> FileClass:
        path = Path(relative_path)
        parts = set(path.parts)
        name = path.name
        if any(part in self.ignored_directory_names for part in path.parts):
            return FileClass.CACHE
        if self.is_ignored_file(name):
            return FileClass.CACHE
        if any(fnmatch(name, pattern) for pattern in self.backup_patterns):
            return FileClass.BACKUP
        if parts & self.report_directory_names:
            return FileClass.REPORT
        if "archive" in parts:
            return FileClass.ARCHIVE
        if path.suffix == ".py" or path.suffix in {".pyi", ".sh"}:
            if "tests" in parts or name.startswith("test_"):
                return FileClass.TEST
            return FileClass.SOURCE
        if path.suffix in {".md", ".rst", ".txt"}:
            return FileClass.DOCUMENTATION
        if path.suffix in {".toml", ".yaml", ".yml", ".json", ".ini", ".cfg", ".env"}:
            return FileClass.CONFIGURATION
        if path.suffix in {".log", ".sqlite", ".db"}:
            return FileClass.GENERATED
        return FileClass.UNKNOWN
