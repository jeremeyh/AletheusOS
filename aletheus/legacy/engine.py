"""
Aletheus Civilization Legacy Core

Post-Genesis 951-975
"""


class LegacyEngine:
    def __init__(self):

        self.legacies = []

    def initialize(self):

        return {
            "system": "aletheus_civilization_legacy",
            "range": "951-975",
            "status": "operational",
        }

    def create_legacy(self, civilization):

        legacy = {"civilization": civilization, "status": "established"}

        self.legacies.append(legacy)

        return legacy

    def list_legacies(self):

        return self.legacies
