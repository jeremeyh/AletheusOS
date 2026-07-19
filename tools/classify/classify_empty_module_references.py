from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent

INPUT = (
    ROOT
    / "reports"
    / "repository_hygiene"
    / "empty_module_text_references.csv"
)

OUTPUT = (
    ROOT
    / "reports"
    / "repository_hygiene"
    / "empty_module_reference_classification.csv"
)


def classify_reference(path: str) -> str:
    reference = Path(path)

    if reference.parts and reference.parts[0] == "tests":
        return "ACTIVE_TEST_REFERENCE"

    if reference.parts and reference.parts[0] == "aletheus":
        return "ACTIVE_RUNTIME_REFERENCE"

    if reference.parts and reference.parts[0] in {
        "card_hawk",
        "cardhawk",
        "capability_engine",
    }:
        return "ACTIVE_SOURCE_REFERENCE"

    if reference.parts and reference.parts[0] == "tools":
        return "TOOL_REFERENCE"

    if reference.suffix == ".md":
        return "DOCUMENTATION_REFERENCE"

    if reference.suffix == ".sh":
        return "SCRIPT_REFERENCE"

    if reference.suffix in {
        ".yaml",
        ".yml",
        ".json",
        ".toml",
    }:
        return "CONFIG_REFERENCE"

    return "OTHER_REFERENCE"


def overall_classification(
    reference_types: set[str],
) -> str:
    active_types = {
        "ACTIVE_TEST_REFERENCE",
        "ACTIVE_RUNTIME_REFERENCE",
        "ACTIVE_SOURCE_REFERENCE",
    }

    if reference_types & active_types:
        return "KEEP_OR_IMPLEMENT"

    if reference_types <= {
        "DOCUMENTATION_REFERENCE",
        "SCRIPT_REFERENCE",
        "TOOL_REFERENCE",
        "CONFIG_REFERENCE",
        "OTHER_REFERENCE",
    }:
        return "ARCHIVE_REVIEW"

    return "MANUAL_REVIEW"


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(INPUT)

    rows = []

    with INPUT.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        for row in csv.DictReader(handle):
            if (
                row.get("classification")
                != "REVIEW_ACTIVE_TEXT_REFERENCE"
            ):
                continue

            references = [
                item.strip()
                for item in row["references"].split("|")
                if item.strip()
            ]

            reference_types = {
                classify_reference(reference)
                for reference in references
            }

            rows.append(
                {
                    "module": row["module"],
                    "path": row["path"],
                    "reference_count": len(references),
                    "reference_types": " | ".join(
                        sorted(reference_types)
                    ),
                    "references": " | ".join(references),
                    "classification": overall_classification(
                        reference_types
                    ),
                }
            )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT.open(
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
                "reference_types",
                "references",
                "classification",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(
        row["classification"]
        for row in rows
    )

    print(f"Modules classified: {len(rows)}")

    for classification, count in sorted(
        counts.items()
    ):
        print(f"{classification}: {count}")

    print(
        "Report:",
        OUTPUT.relative_to(ROOT),
    )


if __name__ == "__main__":
    main()
