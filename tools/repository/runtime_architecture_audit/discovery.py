from __future__ import annotations

from pathlib import Path

from .models import RuntimeModule

IGNORED_DIRECTORY_NAMES = {
    "__pycache__",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
}

IGNORED_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
}

IGNORED_SOURCE_MARKERS = {
    ".before_",
    ".backup",
    "_backup",
    ".genesis",
    ".runtime_boot_restored",
}


def _is_ignored_source(path: Path) -> bool:
    if any(part in IGNORED_DIRECTORY_NAMES for part in path.parts):
        return True

    if path.suffix in IGNORED_FILE_SUFFIXES:
        return True

    name = path.name

    return any(marker in name for marker in IGNORED_SOURCE_MARKERS)


def _module_name(repo_root: Path, path: Path) -> str:
    """
    Produce the canonical absolute Python module name.

    Example:
        aletheus/runtime/core.py
        -> aletheus.runtime.core
    """

    relative = path.relative_to(repo_root).with_suffix("")
    parts = list(relative.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]

    return ".".join(parts)


def _package_name(module_name: str, path: Path) -> str:
    if path.name == "__init__.py":
        return module_name

    return module_name.rpartition(".")[0]


def discover_runtime_modules(runtime_root: Path) -> list[RuntimeModule]:
    """Discover canonical Python modules beneath the runtime package."""

    modules: list[RuntimeModule] = []

    if not runtime_root.exists():
        return modules

    repo_root = runtime_root.parent.parent

    for path in sorted(runtime_root.rglob("*.py")):
        if _is_ignored_source(path):
            continue

        relative_path = path.relative_to(repo_root)
        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )
        module_name = _module_name(repo_root, path)

        modules.append(
            RuntimeModule(
                name=module_name,
                path=path,
                relative_path=relative_path,
                package=_package_name(module_name, path),
                lines=len(text.splitlines()),
                size_bytes=path.stat().st_size,
            )
        )

    return modules
