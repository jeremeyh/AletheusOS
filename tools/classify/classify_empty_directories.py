from __future__ import annotations

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


def main() -> None:
    if not REPORT.exists():
        raise FileNotFoundError(REPORT)

    preserve = []
    remove = []

    with REPORT.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle)

        for row in reader:
            path = Path(row["path"])

            if any(
                part.lower() in PRESERVE_NAMES
                for part in path.parts
            ):
                preserve.append(path)
            else:
                remove.append(path)

    print("PRESERVE / REVIEW")
    for path in preserve:
        print(path)

    print()
    print("REMOVE CANDIDATES")
    for path in remove:
        print(path)

    print()
    print(f"Preserve/review: {len(preserve)}")
    print(f"Remove candidates: {len(remove)}")


if __name__ == "__main__":
    main()
