"""
Platform Fabric Registry

Genesis 13.57
"""


class PlatformFabricRegistry:
    def __init__(self):

        self.engines = {}

    def register(self, name, engine):

        self.engines[name] = engine

    def list_engines(self):

        return list(self.engines.keys())
