from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

REQUIRED = (
    "manifest.json",
    "core",
    "components",
    "applications",
    "config",
    "manifests/checksums.sha256",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()

    failures: list[str] = []

    for item in REQUIRED:
        if not (args.root / item).exists():
            failures.append(f"missing: {item}")

    checksum_file = args.root / "manifests" / "checksums.sha256"
    if checksum_file.exists():
        for line in checksum_file.read_text().splitlines():
            expected, relative = line.split("  ", 1)
            path = args.root / relative
            if not path.exists():
                failures.append(f"checksum target missing: {relative}")
            elif sha256(path) != expected:
                failures.append(f"checksum mismatch: {relative}")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1

    print("Genesis 37.21 distribution validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
