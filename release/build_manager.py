import json
from pathlib import Path

from release.manifest import BuildManifest


class BuildManager:
    """Build & Release Manager™."""

    @staticmethod
    def generate_manifest(path="release_manifest.json"):
        manifest = BuildManifest()
        Path(path).write_text(
            json.dumps(manifest.to_dict(), indent=2), encoding="utf-8"
        )
        return manifest.to_dict()
