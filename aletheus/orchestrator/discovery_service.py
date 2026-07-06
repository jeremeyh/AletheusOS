from __future__ import annotations

from pathlib import Path

from aletheus.discovery import DiscoveryEngine


class DiscoveryService:
    GENESIS = "6.7"
    VERSION = "0.1.0"

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.engine = DiscoveryEngine(self.root)

    def discover(self):
        return self.engine.discover()

    def health(self):
        discovered = self.discover()
        loaded = sum(1 for item in discovered if item.get("loaded"))

        return {
            "name": "Discovery Service",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "discovered": len(discovered),
            "loaded": loaded,
        }
