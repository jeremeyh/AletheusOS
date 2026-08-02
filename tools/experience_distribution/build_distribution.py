from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.output.exists():
        shutil.rmtree(args.output)
    shutil.copytree(args.source, args.output)

    files = [
        path
        for path in args.output.rglob("*")
        if path.is_file() and path.name != "checksums.sha256"
    ]

    checksum_path = args.output / "manifests" / "checksums.sha256"
    checksum_path.parent.mkdir(parents=True, exist_ok=True)
    checksum_path.write_text(
        "\n".join(
            f"{sha256(path)}  {path.relative_to(args.output)}" for path in sorted(files)
        )
        + "\n"
    )

    report = {
        "distributionRoot": str(args.output),
        "fileCount": len(files),
        "checksumIndex": str(checksum_path),
        "artifactState": "source-first-build-required",
        "status": "assembled-not-runtime-certified",
    }
    (args.output / "manifests" / "build-report.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
