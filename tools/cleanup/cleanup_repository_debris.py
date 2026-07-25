from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REMOVE_DIRECTORY_NAMES = {
    "venv_backup",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    "htmlcov",
    "build",
    "dist",
}

PROTECTED_DIRECTORY_NAMES = {
    ".git",
    ".venv",
    "venv",
}

REMOVE_FILE_NAMES = {
    ".DS_Store",
    ".coverage",
    "coverage.xml",
}

REMOVE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".bak",
    ".orig",
    ".tmp",
    ".swp",
    ".swo",
}


def human_size(size: int) -> str:
    value = float(size)

    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{size} B"


def directory_size(path: Path) -> int:
    total = 0

    for current_root, _, filenames in os.walk(
        path,
        topdown=True,
        followlinks=False,
    ):
        current = Path(current_root)

        for filename in filenames:
            file_path = current / filename

            try:
                if file_path.is_symlink():
                    continue

                total += file_path.stat().st_size
            except (FileNotFoundError, PermissionError, OSError):
                continue

    return total


def file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except (FileNotFoundError, PermissionError, OSError):
        return 0


def discover_targets() -> tuple[list[Path], list[Path]]:
    removable_directories: list[Path] = []
    removable_files: list[Path] = []

    for current_root, directory_names, filenames in os.walk(
        ROOT,
        topdown=True,
        followlinks=False,
    ):
        current = Path(current_root)

        kept_directories: list[str] = []

        for directory_name in directory_names:
            directory_path = current / directory_name

            if directory_name in PROTECTED_DIRECTORY_NAMES:
                continue

            if directory_name in REMOVE_DIRECTORY_NAMES:
                removable_directories.append(directory_path)
                continue

            kept_directories.append(directory_name)

        directory_names[:] = kept_directories

        for filename in filenames:
            file_path = current / filename

            if filename == Path(__file__).name:
                continue

            if filename in REMOVE_FILE_NAMES:
                removable_files.append(file_path)
                continue

            if file_path.suffix.lower() in REMOVE_SUFFIXES:
                removable_files.append(file_path)
                continue

            if filename.endswith("~"):
                removable_files.append(file_path)

    removable_directories.sort(
        key=lambda path: str(path.relative_to(ROOT))
    )
    removable_files.sort(
        key=lambda path: str(path.relative_to(ROOT))
    )

    return removable_directories, removable_files


def remove_target(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
        return

    if path.is_dir():
        shutil.rmtree(path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Remove objectively safe repository debris. "
            "Dry-run is the default."
        )
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Delete discovered debris.",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Show totals without listing every target.",
    )
    args = parser.parse_args()

    directories, files = discover_targets()

    directory_sizes = {
        path: directory_size(path)
        for path in directories
    }

    file_sizes = {
        path: file_size(path)
        for path in files
    }

    total_size = (
        sum(directory_sizes.values())
        + sum(file_sizes.values())
    )

    print("=" * 72)
    print(
        "AletheusOS Repository Cleanup — "
        + ("APPLY" if args.apply else "DRY RUN")
    )
    print("=" * 72)
    print(f"Root: {ROOT}")
    print(f"Directories: {len(directories)}")
    print(f"Files: {len(files)}")
    print(f"Estimated recovery: {human_size(total_size)}")

    if not args.summary_only:
        print()

        for path in directories:
            relative = path.relative_to(ROOT)
            print(
                f"DIR   {relative} "
                f"({human_size(directory_sizes[path])})"
            )

        for path in files:
            relative = path.relative_to(ROOT)
            print(
                f"FILE  {relative} "
                f"({human_size(file_sizes[path])})"
            )

    if not args.apply:
        print()
        print("No files were deleted.")
        print(
            "Apply with: "
            "python cleanup_repository_debris.py "
            "--apply --summary-only"
        )
        return

    removed_directories = 0
    removed_files = 0
    failures: list[tuple[Path, Exception]] = []

    for path in files:
        try:
            remove_target(path)
            removed_files += 1
        except Exception as exc:
            failures.append((path, exc))

    for path in sorted(
        directories,
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        try:
            remove_target(path)
            removed_directories += 1
        except FileNotFoundError:
            continue
        except Exception as exc:
            failures.append((path, exc))

    print()
    print(f"Removed directories: {removed_directories}")
    print(f"Removed files: {removed_files}")
    print(
        "Recovered approximately: "
        f"{human_size(total_size)}"
    )

    if failures:
        print()
        print("Failures:")

        for path, error in failures:
            print(
                f"  {path.relative_to(ROOT)}: "
                f"{type(error).__name__}: {error}"
            )

        raise SystemExit(1)

    print("Cleanup completed successfully.")


if __name__ == "__main__":
    main()
