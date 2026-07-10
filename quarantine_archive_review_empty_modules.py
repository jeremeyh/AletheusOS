from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent

REPORT = (
    ROOT
    / "reports"
    / "repository_hygiene"
    / "empty_module_reference_classification.csv"
)

BATCH_ID = datetime.now(
    timezone.utc
).strftime("%Y%m%dT%H%M%SZ")

QUARANTINE_ROOT = (
    ROOT
    / "archive"
    / "quarantine"
    / "archive_review_empty_modules"
    / BATCH_ID
)

MANIFEST = QUARANTINE_ROOT / "manifest.json"


def load_candidates() -> list[Path]:
    candidates: list[Path] = []

    with REPORT.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        for row in csv.DictReader(handle):
            if row["classification"] != "ARCHIVE_REVIEW":
                continue

            candidates.append(
                ROOT / row["path"]
            )

    return candidates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
    )
    args = parser.parse_args()

    candidates = load_candidates()
    existing: list[Path] = []

    for path in candidates:
        if not path.exists():
            continue

        if path.name == "__init__.py":
            raise RuntimeError(
                f"Refusing package marker: {path}"
            )

        if not path.is_file():
            raise RuntimeError(
                f"Not a file: {path}"
            )

        if path.stat().st_size != 0:
            raise RuntimeError(
                f"File is no longer empty: {path}"
            )

        existing.append(path)

    print("=" * 72)
    print(
        "Archive-Review Empty Module Quarantine — "
        + ("APPLY" if args.apply else "DRY RUN")
    )
    print("=" * 72)
    print(f"Candidates: {len(candidates)}")
    print(f"Existing: {len(existing)}")
    print(f"Already absent: {len(candidates) - len(existing)}")

    for path in existing:
        print(path.relative_to(ROOT))

    if not args.apply:
        print()
        print("No files were moved.")
        return

    if not existing:
        print()
        print("No existing candidates remain.")
        return

    QUARANTINE_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    moved = []

    for source in existing:
        relative = source.relative_to(ROOT)
        destination = QUARANTINE_ROOT / relative

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.move(
            str(source),
            str(destination),
        )

        moved.append(
            {
                "source": str(relative),
                "quarantine": str(
                    destination.relative_to(ROOT)
                ),
            }
        )

    MANIFEST.write_text(
        json.dumps(
            {
                "created_at": datetime.now(
                    timezone.utc
                ).isoformat(),
                "moved_count": len(moved),
                "moved": moved,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print(f"Moved: {len(moved)}")
    print(
        f"Manifest: {MANIFEST.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
