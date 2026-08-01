from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import InstallerEngine
from .models import ReleaseManifest, ReleaseTarget


def load_manifest(path: Path) -> tuple[ReleaseManifest, dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    manifest = ReleaseManifest(
        release_id=str(payload["release_id"]),
        version=str(payload["version"]),
        title=str(payload["title"]),
        commit_message=str(payload["commit_message"]),
        package_root=(path.parent / payload["package_root"]).resolve(),
        targets=tuple(
            ReleaseTarget(
                source=str(item["source"]),
                destination=str(item["destination"]),
            )
            for item in payload["targets"]
        ),
        dependencies=tuple(str(item) for item in payload.get("dependencies", [])),
        metadata=dict(payload.get("metadata", {})),
    )
    return manifest, dict(payload["checksums"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("install", "dry-run", "verify"))
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--repository",
        type=Path,
        default=Path.home() / "Development/AletheusOS",
    )
    args = parser.parse_args()

    manifest, checksums = load_manifest(args.manifest)
    engine = InstallerEngine(args.repository)

    if args.command == "verify":
        engine.verify_repository()
        engine.verify_dependencies(manifest)
        engine.verify_package_layout(manifest)
        engine.verify_checksums(manifest, checksums)
        print(f"Verified {manifest.release_id}.")
        return 0

    result = engine.install(
        manifest,
        checksums=checksums,
        dry_run=args.command == "dry-run",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0
