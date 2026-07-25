from __future__ import annotations

import ast
import csv
import os
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT_DIR = ROOT / "reports" / "repository_hygiene"

EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".venv",
    "venv",
    "venv_backup",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "archive",
    ".aletheus_restore_points",
}

SEARCHABLE_SUFFIXES = {
    ".py",
    ".sh",
    ".md",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
}

SAFE_ZERO_BYTE_SUFFIXES = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".sh",
}


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def module_name(path: Path) -> str:
    parts = list(
        path.relative_to(ROOT)
        .with_suffix("")
        .parts
    )

    if parts and parts[-1] == "__init__":
        parts.pop()

    return ".".join(parts)


def discover() -> tuple[list[Path], list[Path]]:
    files: list[Path] = []
    directories: list[Path] = []

    for current_root, directory_names, filenames in os.walk(
        ROOT,
        topdown=True,
        followlinks=False,
    ):
        current = Path(current_root)

        directory_names[:] = [
            name
            for name in directory_names
            if name not in EXCLUDED_DIRECTORY_NAMES
        ]

        if current != ROOT:
            directories.append(current)

        for filename in filenames:
            files.append(current / filename)

    return files, directories


def parse_imports(
    python_files: list[Path],
) -> tuple[set[str], set[str]]:
    imports: set[str] = set()
    imported_symbols: set[str] = set()

    for path in python_files:
        try:
            text = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
            tree = ast.parse(text)
        except (OSError, SyntaxError):
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if not node.module:
                    continue

                imports.add(node.module)

                for alias in node.names:
                    imported_symbols.add(
                        f"{node.module}.{alias.name}"
                    )

    return imports, imported_symbols


def build_reference_index(
    files: list[Path],
) -> str:
    chunks: list[str] = []

    for path in files:
        if path.suffix not in SEARCHABLE_SUFFIXES:
            continue

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except OSError:
            continue

        chunks.append(text)

    return "\n".join(chunks)


def is_imported(
    module: str,
    imports: set[str],
    imported_symbols: set[str],
) -> bool:
    """
    Return True only when the precise module is imported.

    Imported symbols and parent packages do not prove that an empty
    descendant module is active.
    """
    if not module:
        return False

    return module in imports


def classify_empty_python(
    path: Path,
    imports: set[str],
    imported_symbols: set[str],
    reference_text: str,
) -> dict[str, object]:
    module = module_name(path)
    package_marker = path.name == "__init__.py"
    imported = is_imported(
        module,
        imports,
        imported_symbols,
    )

    slash_name = module.replace(".", "/")

    referenced = (
        bool(module)
        and (
            module in reference_text
            or slash_name in reference_text
        )
    )

    if package_marker:
        classification = "KEEP_PACKAGE_MARKER"
    elif imported:
        classification = "REVIEW_REFERENCED_EMPTY_MODULE"
    elif referenced:
        classification = "REVIEW_TEXT_REFERENCED_MODULE"
    else:
        classification = "DELETE_CANDIDATE"

    return {
        "path": relative(path),
        "module": module,
        "package_marker": package_marker,
        "imported": imported,
        "referenced": referenced,
        "classification": classification,
    }


def write_csv(
    filename: str,
    rows: list[dict[str, object]],
) -> Path:
    path = REPORT_DIR / filename

    if not rows:
        path.write_text("", encoding="utf-8")
        return path

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)

    return path


def main() -> None:
    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    files, directories = discover()

    python_files = [
        path
        for path in files
        if path.suffix == ".py"
    ]

    print(f"Files discovered: {len(files)}")
    print(f"Python files: {len(python_files)}")

    imports, imported_symbols = parse_imports(
        python_files
    )

    print("Building one-pass text reference index...")
    reference_text = build_reference_index(files)

    empty_python_rows = []

    for path in python_files:
        try:
            if path.stat().st_size != 0:
                continue
        except OSError:
            continue

        empty_python_rows.append(
            classify_empty_python(
                path,
                imports,
                imported_symbols,
                reference_text,
            )
        )

    empty_directory_rows = []

    for path in directories:
        try:
            if any(path.iterdir()):
                continue
        except OSError:
            continue

        empty_directory_rows.append(
            {
                "path": relative(path),
                "classification": "DELETE_CANDIDATE",
            }
        )

    zero_byte_other_rows = []

    protected_zero_byte_names = {
        ".gitkeep",
        ".keep",
        "PLACEHOLDER",
        "LOCK",
        "READY",
        "ENABLED",
        "DISABLED",
    }

    for path in files:
        if path.suffix == ".py":
            continue

        try:
            if path.stat().st_size != 0:
                continue
        except OSError:
            continue

        relative_path = relative(path)

        if path.name in protected_zero_byte_names:
            classification = "KEEP_MARKER"

        elif relative_path.startswith(
            "reports/repository_hygiene/"
        ):
            classification = "KEEP_GENERATED_REPORT"

        elif path.suffix in SAFE_ZERO_BYTE_SUFFIXES:
            classification = "DELETE_CANDIDATE"

        elif not path.suffix:
            classification = "REVIEW_EXTENSIONLESS"

        else:
            classification = "REVIEW"

        zero_byte_other_rows.append(
            {
                "path": relative_path,
                "suffix": path.suffix or "<none>",
                "classification": classification,
            }
        )

    backup_rows = []

    for path in files:
        name = path.name.lower()

        if (
            name.endswith(".bak")
            or name.endswith(".orig")
            or name.endswith(".old")
            or name.endswith("~")
            or ".backup" in name
        ):
            backup_rows.append(
                {
                    "path": relative(path),
                    "size": path.stat().st_size,
                    "classification": "REVIEW_OR_DELETE",
                }
            )

    reports = {
        "empty_python_files.csv": empty_python_rows,
        "empty_directories.csv": empty_directory_rows,
        "zero_byte_other_files.csv": zero_byte_other_rows,
        "backup_files.csv": backup_rows,
    }

    for filename, rows in reports.items():
        report = write_csv(filename, rows)
        print(
            f"{filename}: {len(rows)} -> {report}"
        )

    counts = Counter(
        row["classification"]
        for row in empty_python_rows
    )

    print()
    print("Empty Python classifications:")

    for classification, count in sorted(
        counts.items()
    ):
        print(
            f"  {classification}: {count}"
        )

    print()
    print("No files were deleted.")


if __name__ == "__main__":
    main()
