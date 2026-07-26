"""
Genesis 11 Repository Scanner.

The scanner is responsible only for discovering Python source files.
It performs no AST parsing and no RUF012 analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
}


@dataclass(frozen=True, slots=True)
class ScanSummary:
    """Repository discovery summary."""

    root: Path
    python_files: tuple[Path, ...]
    files_discovered: int

    @property
    def successful(self) -> bool:
        return True


class RepositoryScanner:
    """
    Discover Python files beneath a repository root.
    """

    def __init__(
        self,
        root: Path,
        excludes: set[str] | None = None,
    ) -> None:
        self.root = Path(root).resolve()
        self.excludes = excludes or DEFAULT_EXCLUDES

    def scan(self) -> ScanSummary:
        """Return all Python files beneath the repository."""

        files: list[Path] = []

        for path in self.root.rglob("*.py"):
            if any(part in self.excludes for part in path.parts):
                continue

            files.append(path)

        files.sort()

        return ScanSummary(
            root=self.root,
            python_files=tuple(files),
            files_discovered=len(files),
        )
