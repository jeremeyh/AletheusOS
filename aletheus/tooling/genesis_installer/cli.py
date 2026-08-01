from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import InstallerEngine
from .models import ReleaseManifest


def load_manifest(path: Path) -> tuple[ReleaseManifest, dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    release = ReleaseManifest(
        release_id=payload["release_id"],
        version=payload["version"],
        title=payload["title"],
        commit_message=payload["commit_message"],
        package_root=(path.parent / payload["package_root"]).resolve(),
        targets=list(payload["targets"]),
        dependencies=list(payload.get("dependencies", [])),
        validation_commands=list(payload.get("validation_commands", [])),
        metadata=dict(payload.get("metadata", {})),
    )
    return release, dict(payload["checksums"])


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
        engine.verify_checksums(manifest.package_root, checksums)
        engine.resolve_dependencies(manifest)
        print(f"Verified {manifest.release_id}.")
        return 0

    result = engine.install(
        manifest,
        checksums=checksums,
        dry_run=args.command == "dry-run",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0
