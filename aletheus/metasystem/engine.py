"""
Aletheus Intelligence Metasystem Core

Post-Genesis 376-400
"""


class MetasystemEngine:
    def __init__(self):

        self.civilizations = []

    def initialize(self):

        return {
            "system": "aletheus_intelligence_metasystem",
            "range": "376-400",
            "status": "operational",
        }

    def register_civilization(self, civilization):

        self.civilizations.append(civilization)

        return {"civilization": civilization, "status": "registered"}

    def list_civilizations(self):

        return self.civilizations
