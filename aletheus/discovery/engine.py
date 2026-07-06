from __future__ import annotations

from pathlib import Path

from .loader import DiscoveryLoader
from .scanner import DiscoveryScanner


class DiscoveryEngine:
    """
    Discovery Engine™

    Coordinates scanning and loading.

    Genesis 6.6
    """

    VERSION = "0.1.0"

    def __init__(self, root):

        self.root = Path(root)

        self.scanner = DiscoveryScanner(self.root)

        self.loader = DiscoveryLoader()

    def discover(self):

        discovered = []

        for package in self.scanner.scan():

            module_name = f"aletheus.{package.name}"

            module = self.loader.load(module_name)

            discovered.append(
                {
                    "package": package.name,
                    "module": module_name,
                    "loaded": module is not None,
                }
            )

        return discovered
