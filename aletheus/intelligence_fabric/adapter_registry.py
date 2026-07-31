"""
Adapter Registry

Post-Genesis 37
"""


class AdapterRegistry:
    def __init__(self):

        self.adapters = {}

    def register(self, name, adapter):

        self.adapters[name] = adapter

        return {"adapter": name, "status": "registered"}

    def get(self, name):

        return self.adapters.get(name)
