from __future__ import annotations

from aletheus.runtime_platform.bootstrap import BootManager
from aletheus.runtime_platform.manifest.runtime_manifest import (
    RuntimeManifest,
)


class RuntimeBootstrap:
    """
    Compatibility adapter between the existing runtime and the
    Runtime Platform.

    Existing runtime/core.py should delegate runtime startup here.
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        runtime,
        manifest: RuntimeManifest,
    ) -> None:

        self.runtime = runtime
        self.manager = BootManager(manifest)

    def boot(self):

        return self.manager.boot(self.runtime)

    @property
    def registry(self):
        return self.manager.registry
