"""
JSON Importer

Version 1.6.0
"""

from __future__ import annotations

import json

from cardhawk.asset_vault import Asset


class JSONImporter:
    def load(self, filename):

        with open(filename, "r", encoding="utf-8") as f:
            records = json.load(f)

        assets = []

        for record in records:
            assets.append(Asset(**record))

        return assets
