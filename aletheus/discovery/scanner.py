from __future__ import annotations

from pathlib import Path


class DiscoveryScanner:
    """
    Discovery Scanner™

    Finds candidate AletheusOS platform packages.

    Phase 1 intentionally performs filesystem discovery only.
    """

    VERSION = "0.1.0"

    def __init__(self, root):

        self.root = Path(root)

    def scan(self):

        packages = []

        for path in sorted(self.root.iterdir()):
            if not path.is_dir():
                continue

            if path.name.startswith("__"):
                continue

            if (path / "__init__.py").exists():
                packages.append(path)

        return packages
