from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("root", type=Path)
    args = p.parse_args()
    failures = []
    manifest = args.root / "manifest.json"
    if not manifest.exists():
        failures.append("manifest missing")
    else:
        data = json.loads(manifest.read_text())
        if data.get("genesis") != "37.22-37.29":
            failures.append("incorrect genesis")
    check = args.root / "manifests" / "checksums.sha256"
    if not check.exists():
        failures.append("checksums missing")
    else:
        for line in check.read_text().splitlines():
            expected, rel = line.split("  ", 1)
            path = args.root / rel
            if not path.exists():
                failures.append(f"missing {rel}")
            elif sha(path) != expected:
                failures.append(f"checksum mismatch {rel}")
    if failures:
        print("\n".join(f"ERROR: {f}" for f in failures))
        return 1
    print("Genesis 37 runtime distribution validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
