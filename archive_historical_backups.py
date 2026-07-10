from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = (
    ROOT
    / "reports"
    / "repository_hygiene"
    / "backup_files.csv"
)

BATCH_ID = datetime.now(
    timezone.utc
).strftime("%Y%m%dT%H%M%SZ")

ARCHIVE_ROOT = (
    ROOT
    / "archive"
    / "historical_backups"
    / BATCH_ID
)

MANIFEST = ARCHIVE_ROOT / "manifest.json"


def original_candidate(path: Path) -> Path | None:
    name = path.name

    for suffix in (
        ".bak",
        ".orig",
        ".old",
        "~",
    ):
        if name.endswith(suffix):
            return path.with_name(
                name[: -len(suffix)]
            )

    match = re.match(
        r"^(?P<base>.+?)\.backup(?:_.*)?$",
        name,
    )

    if match:
        return path.with_name(
            match.group("base")
        )

    return None


def load_candidates() -> list[Path]:
    if not REPORT.exists():
        raise FileNotFoundError(REPORT)

    candidates: list[Path] = []

    with REPORT.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        for row in csv.DictReader(handle):
            candidates.append(
                ROOT / Path(row["path"])
            )

    return candidates


def classify(path: Path) -> str:
    if not path.exists():
        return "ABSENT"

    if not path.is_file():
        return "NOT_FILE"

    original = original_candidate(path)

    if original is None:
        return "UNKNOWN_PATTERN"

    if not original.exists():
        return "NO_LIVE_ORIGINAL"

    if not original.is_file():
        return "LIVE_ORIGINAL_NOT_FILE"

    try:
        if path.read_bytes() == original.read_bytes():
            return "IDENTICAL"
    except OSError:
        return "READ_ERROR"

    return "HISTORICAL_DIFFERENT_CONTENT"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
    )
    args = parser.parse_args()

    rows = []
    archive_candidates = []

    for path in load_candidates():
        status = classify(path)

        rows.append(
            {
                "path": str(
                    path.relative_to(ROOT)
                ),
                "status": status,
            }
        )

        if status == "HISTORICAL_DIFFERENT_CONTENT":
            archive_candidates.append(path)

    print("=" * 72)
    print(
        "Historical Backup Archive — "
        + ("APPLY" if args.apply else "DRY RUN")
    )
    print("=" * 72)
    print(
        "Historical backups:",
        len(archive_candidates),
    )

    for path in archive_candidates:
        print(path.relative_to(ROOT))

    unresolved = [
        row
        for row in rows
        if row["status"]
        not in {
            "ABSENT",
            "IDENTICAL",
            "HISTORICAL_DIFFERENT_CONTENT",
        }
    ]

    if unresolved:
        print()
        print("Unresolved files:")
        for row in unresolved:
            print(
                f'{row["status"]:24} '
                f'{row["path"]}'
            )

    if not args.apply:
        print()
        print("No files were moved.")
        return

    if not archive_candidates:
        print()
        print("No historical backups remain.")
        return

    ARCHIVE_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    moved = []

    for source in archive_candidates:
        relative = source.relative_to(ROOT)
        destination = ARCHIVE_ROOT / relative

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
                "archive": str(
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
                "unresolved": unresolved,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print(f"Archived files: {len(moved)}")
    print(
        f"Manifest: {MANIFEST.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
