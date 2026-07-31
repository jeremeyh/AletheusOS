"""
Principle Registry

Genesis 13.54
"""


class PrincipleRegistry:
    def __init__(self):

        self.principles = {}

    def register(self, principle):

        self.principles[principle.principle_id] = principle
