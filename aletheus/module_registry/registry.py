"""
Universal Module Registry

Post-Genesis 80.5
"""


class ModuleRegistry:
    def __init__(self):

        self.modules = {}

    def register(self, name, genesis):

        self.modules[name] = {"genesis": genesis, "status": "registered"}

    def list_modules(self):

        return self.modules
