from __future__ import annotations

from pathlib import Path

IGNORED_DIRECTORY_NAMES = {
    "__pycache__",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "backups",
}

IGNORED_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".zip",
}

IGNORED_FILE_MARKERS = {
    ".before_",
    ".backup",
    "_backup",
    ".genesis",
    ".runtime_boot_restored",
}


def _include_entry(entry: Path) -> bool:
    if entry.name in IGNORED_DIRECTORY_NAMES:
        return False

    if entry.suffix in IGNORED_FILE_SUFFIXES:
        return False

    if any(marker in entry.name for marker in IGNORED_FILE_MARKERS):
        return False

    return True


def build_package_tree(runtime_root: Path) -> str:
    """Render the active runtime source package tree."""

    if not runtime_root.exists():
        return f"{runtime_root.name} [missing]"

    lines = [runtime_root.name]

    def walk(directory: Path, prefix: str = "") -> None:
        entries = sorted(
            (entry for entry in directory.iterdir() if _include_entry(entry)),
            key=lambda entry: (
                entry.is_file(),
                entry.name.lower(),
                entry.name,
            ),
        )

        for index, entry in enumerate(entries):
            last = index == len(entries) - 1
            connector = "└── " if last else "├── "

            lines.append(f"{prefix}{connector}{entry.name}")

            if entry.is_dir():
                extension = "    " if last else "│   "
                walk(entry, prefix + extension)

    walk(runtime_root)

    return "\n".join(lines)
