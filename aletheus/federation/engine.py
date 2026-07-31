"""
Aletheus Civilization Federation Core

Post-Genesis 701-725
"""


class FederationEngine:
    def __init__(self):

        self.members = []

    def initialize(self):

        return {
            "system": "aletheus_civilization_federation",
            "range": "701-725",
            "status": "operational",
        }

    def register_member(self, civilization):

        member = {"civilization": civilization, "status": "federated"}

        self.members.append(member)

        return member

    def list_members(self):

        return self.members
