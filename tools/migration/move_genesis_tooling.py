#!/usr/bin/env python3

from pathlib import Path
import shutil
import sys

ROOT = Path.cwd()
TOOLS = ROOT / "tools" / "genesis"

PREFIXES = {
    "genesis_7_": "genesis_7",
    "genesis_8_": "genesis_8",
    "genesis_9_": "genesis_9",
    "genesis_10_": "genesis_10",
    "genesis_11_": "genesis_11",
    "genesis_12_": "genesis_12",
    "genesis_13_": "genesis_13",
    "post_genesis_": "post_genesis",
}

APPLY = "--apply" in sys.argv


def move(path: Path, destination: Path):
    if destination.exists():
        print(f"SKIP  {path} -> {destination} (exists)")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)

    if APPLY:
        shutil.move(str(path), str(destination))
        print(f"MOVE  {path} -> {destination}")
    else:
        print(f"PLAN  {path} -> {destination}")


def main():
    count = 0

    for item in ROOT.iterdir():

        if not item.is_file():
            continue

        name = item.name

        for prefix, folder in PREFIXES.items():

            if name.startswith(prefix):

                new_name = name[len(prefix):]

                destination = TOOLS / folder / new_name

                move(item, destination)

                count += 1
                break

    print()
    print(f"Files matched : {count}")
    print("Mode          :", "APPLY" if APPLY else "DRY RUN")


if __name__ == "__main__":
    main()
