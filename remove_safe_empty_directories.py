from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = (
    ROOT
    / "reports"
    / "repository_hygiene"
    / "empty_directories.csv"
)

PRESERVE_NAMES = {
    "uploads",
    "exports",
    "cache",
    "caches",
    "logs",
    "runtime_state",
    "snapshots",
    "artifacts",
    "reports",
    "data",
    "tmp",
    "temp",
    "storage",
    "backups",
    "checkpoints",
}


def candidates() -> list[Path]:
    result = []

    with REPORT.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle)

        for row in reader:
            relative = Path(row["path"])

            if any(
                part.lower() in PRESERVE_NAMES
                for part in relative.parts
            ):
                continue

            result.append(ROOT / relative)

    return sorted(
        result,
        key=lambda path: len(path.parts),
        reverse=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
    )
    args = parser.parse_args()

    paths = candidates()

    print(
        "Mode:",
        "APPLY" if args.apply else "DRY RUN",
    )
    print("Candidates:", len(paths))

    removed = 0
    skipped = 0

    for path in paths:
        if not path.exists():
            skipped += 1
            continue

        try:
            if any(path.iterdir()):
                skipped += 1
                continue
        except OSError:
            skipped += 1
            continue

        print(path.relative_to(ROOT))

        if args.apply:
            path.rmdir()
            removed += 1

    print()
    print("Removed:", removed)
    print("Skipped:", skipped)


if __name__ == "__main__":
    main()
