from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

INPUT_REPORT = ROOT / "reports" / "repository_hygiene" / "empty_python_files.csv"

OUTPUT_REPORT = (
    ROOT / "reports" / "repository_hygiene" / "empty_module_text_references.csv"
)

SEARCH_SUFFIXES = {
    ".py",
    ".md",
    ".sh",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
}

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
    ".aletheus_restore_points",
    "runtime_state",
    "backups",
    "migrations",
}

EXCLUDED_ROOT_SCRIPT_PREFIXES = {
    "genesis_",
    "card_hawk_genesis_",
    "step",
}


def active_search_files() -> list[Path]:
    files = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix not in SEARCH_SUFFIXES:
            continue

        relative = path.relative_to(ROOT)

        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue

        if (
            len(relative.parts) == 1
            and path.suffix == ".sh"
            and any(
                path.name.startswith(prefix) for prefix in EXCLUDED_ROOT_SCRIPT_PREFIXES
            )
        ):
            continue

        files.append(path)

    return files


def load_targets() -> dict[str, str]:
    targets = {}

    with INPUT_REPORT.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        for row in csv.DictReader(handle):
            if row["classification"] == "REVIEW_TEXT_REFERENCED_MODULE":
                targets[row["module"]] = row["path"]

    return targets


def main() -> None:
    targets = load_targets()
    references = {module: [] for module in targets}

    for path in active_search_files():
        try:
            text = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except OSError:
            continue

        relative = str(path.relative_to(ROOT))

        for module in targets:
            dotted = module
            slashed = module.replace(".", "/")

            if dotted in text or slashed in text:
                references[module].append(relative)

    rows = []

    for module in sorted(targets):
        sources = sorted(set(references[module]))

        rows.append(
            {
                "module": module,
                "path": targets[module],
                "reference_count": len(sources),
                "references": " | ".join(sources),
                "classification": (
                    "NO_ACTIVE_REFERENCE"
                    if not sources
                    else "REVIEW_ACTIVE_TEXT_REFERENCE"
                ),
            }
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
                "path",
                "reference_count",
                "references",
                "classification",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    no_reference = sum(
        1 for row in rows if row["classification"] == "NO_ACTIVE_REFERENCE"
    )

    print(f"Modules mapped: {len(rows)}")
    print(f"No active reference: {no_reference}")
    print(
        "Active text reference:",
        len(rows) - no_reference,
    )
    print(
        "Report:",
        OUTPUT_REPORT.relative_to(ROOT),
    )


if __name__ == "__main__":
    main()
