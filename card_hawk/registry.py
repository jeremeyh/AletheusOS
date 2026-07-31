"""
Card Hawk Application Registry

Genesis 14.0
"""


class CardHawkRegistry:
    def __init__(self):

        self.components = {}

    def register(self, name, component):

        self.components[name] = component

    def available(self):

        return list(self.components.keys())
