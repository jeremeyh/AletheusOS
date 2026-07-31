#!/usr/bin/env python3

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

GENESIS_RE = re.compile(r"^genesis(\d+)_(.+)$")

parser = argparse.ArgumentParser(description="Move remaining Genesis files")
parser.add_argument("--apply", action="store_true", help="Actually move files")
args = parser.parse_args()

matched = 0
moved = 0
skipped = 0

print(f"Repository Root: {ROOT}")
print()

for item in sorted(ROOT.iterdir()):
    if not item.is_file():
        continue

    match = GENESIS_RE.match(item.name)

    if not match:
        continue

    matched += 1

    generation = match.group(1)
    remainder = match.group(2)

    destination = ROOT / "tools" / "genesis" / f"genesis_{generation}" / remainder

    print(f"{'MOVE' if args.apply else 'PLAN'}")
    print(f"  {item.name}")
    print(f"  -> {destination.relative_to(ROOT)}")

    if not args.apply:
        continue

    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        print("     SKIP (already exists)")
        skipped += 1
        continue

    shutil.move(str(item), str(destination))
    moved += 1

print()
print("=" * 60)
print(f"Matched : {matched}")
print(f"Moved   : {moved}")
print(f"Skipped : {skipped}")
print(f"Mode    : {'APPLY' if args.apply else 'DRY RUN'}")
print("=" * 60)
