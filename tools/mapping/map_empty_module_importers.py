from __future__ import annotations

import ast
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent

INPUT_REPORT = ROOT / "reports" / "repository_hygiene" / "empty_python_files.csv"

OUTPUT_REPORT = ROOT / "reports" / "repository_hygiene" / "empty_module_importers.csv"

EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "venv",
    "archive",
    "reports",
    "__pycache__",
    ".pytest_cache",
    "build",
    "dist",
}


def active_python_files() -> list[Path]:
    files = []

    for path in ROOT.rglob("*.py"):
        relative = path.relative_to(ROOT)

        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue

        files.append(path)

    return files


def load_targets() -> set[str]:
    if not INPUT_REPORT.exists():
        raise FileNotFoundError(INPUT_REPORT)

    targets = set()

    with INPUT_REPORT.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        for row in csv.DictReader(handle):
            if row.get("classification") == "REVIEW_REFERENCED_EMPTY_MODULE":
                targets.add(row["module"])

    return targets


def resolve_from_import(
    importer: Path,
    node: ast.ImportFrom,
) -> str | None:
    if node.level == 0:
        return node.module

    importer_parts = list(importer.relative_to(ROOT).with_suffix("").parts)

    if importer_parts[-1] == "__init__":
        importer_parts.pop()
    else:
        importer_parts.pop()

    levels_up = node.level - 1

    if levels_up:
        importer_parts = importer_parts[:-levels_up]

    if node.module:
        importer_parts.extend(node.module.split("."))

    return ".".join(importer_parts)


def main() -> None:
    targets = load_targets()
    importers: dict[str, set[str]] = defaultdict(set)

    for path in active_python_files():
        try:
            source = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
            tree = ast.parse(source)
        except (OSError, SyntaxError):
            continue

        relative_importer = str(path.relative_to(ROOT))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in targets:
                        importers[alias.name].add(relative_importer)

            elif isinstance(node, ast.ImportFrom):
                base = resolve_from_import(
                    path,
                    node,
                )

                if not base:
                    continue

                if base in targets:
                    importers[base].add(relative_importer)

                for alias in node.names:
                    full_name = f"{base}.{alias.name}"

                    if full_name in targets:
                        importers[full_name].add(relative_importer)

    rows = []

    for module in sorted(targets):
        sources = sorted(importers[module])

        rows.append(
            {
                "module": module,
                "importer_count": len(sources),
                "importers": " | ".join(sources),
                "classification": (
                    "NO_EXACT_IMPORT_FOUND" if not sources else "EXACT_IMPORT_FOUND"
                ),
            }
        )

    OUTPUT_REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_REPORT.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "module",
                "importer_count",
                "importers",
                "classification",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    no_exact = sum(
        1 for row in rows if row["classification"] == "NO_EXACT_IMPORT_FOUND"
    )

    print(f"Modules mapped: {len(rows)}")
    print(f"Exact import found: {len(rows) - no_exact}")
    print(f"No exact importer found: {no_exact}")
    print(
        "Report:",
        OUTPUT_REPORT.relative_to(ROOT),
    )


if __name__ == "__main__":
    main()
