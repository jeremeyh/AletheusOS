#!/usr/bin/env python3

"""
Move validation scripts into the canonical validation hierarchy.

Default:
    Dry run

Use:
    python tools/migration/move_validation_files.py
    python tools/migration/move_validation_files.py --apply
"""

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
args = parser.parse_args()

matched = 0
moved = 0
skipped = 0


def destination(name: str) -> Path | None:

    if not name.startswith("validate_"):
        return None

    if ".before_" in name:
        return ROOT / "tools" / "validation" / "archive" / name

    if name.startswith("validate_genesis"):
        return ROOT / "tools" / "validation" / "genesis" / name

    if name.startswith("validate_nimble"):
        return ROOT / "tools" / "validation" / "nimble" / name

    return ROOT / "tools" / "validation" / "misc" / name


for item in sorted(ROOT.iterdir()):
    if not item.is_file():
        continue

    dest = destination(item.name)

    if dest is None:
        continue

    matched += 1

    print(f"{'MOVE' if args.apply else 'PLAN'}")
    print(f"  {item.name}")
    print(f"  -> {dest.relative_to(ROOT)}")

    if not args.apply:
        continue

    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists():
        print("     SKIP (already exists)")
        skipped += 1
        continue

    shutil.move(str(item), str(dest))
    moved += 1


print()
print("=" * 60)
print(f"Matched : {matched}")
print(f"Moved   : {moved}")
print(f"Skipped : {skipped}")
print(f"Mode    : {'APPLY' if args.apply else 'DRY RUN'}")
print("=" * 60)
