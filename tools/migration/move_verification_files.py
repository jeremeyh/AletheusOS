#!/usr/bin/env python3

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
args = parser.parse_args()


def destination(name: str):

    if not name.startswith("verify_"):
        return None

    if name.startswith("verify_plugin"):
        return ROOT / "tools" / "verification" / "plugins" / name

    if name.startswith("verify_agents"):
        return ROOT / "tools" / "verification" / "agents" / name

    return ROOT / "tools" / "verification" / "runtime" / name


matched = moved = skipped = 0

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
