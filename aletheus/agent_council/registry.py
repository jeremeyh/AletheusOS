"""
Council Agent Registry

Genesis 13.29
"""


class CouncilRegistry:
    def __init__(self):

        self.members = {}

    def register(self, agent):

        self.members[agent] = {"status": "active"}

    def members_list(self):

        return list(self.members.keys())
