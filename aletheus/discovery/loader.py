from __future__ import annotations

import importlib


class DiscoveryLoader:
    """
    Imports discovered packages.

    Phase 1 performs safe imports only.
    """

    VERSION = "0.1.0"

    def load(self, module_name: str):

        try:

            return importlib.import_module(module_name)

        except Exception:

            return None
