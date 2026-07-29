from __future__ import annotations

from aletheus.runtime_platform.manifest.runtime_manifest import (
    RuntimeManifest,
)


class RuntimeManifestBuilder:
    """
    Builds the canonical RuntimeManifest consumed by the Runtime Platform.

    Initially this returns an empty manifest. Existing runtime domains will
    be migrated incrementally into the manifest as integration progresses.
    """

    VERSION = "1.0.0"

    def build(self) -> RuntimeManifest:
        return RuntimeManifest(
            name="Aletheus Runtime",
            version=self.VERSION,
            entries=(),
        )
