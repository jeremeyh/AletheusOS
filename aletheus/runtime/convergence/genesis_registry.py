"""
AletheusOS Genesis Registry

Genesis 100.5
"""


class GenesisRegistry:


    def __init__(self):

        self.genesis = {}



    def register(self, version, capability):

        self.genesis[version] = capability



    def list_all(self):

        return self.genesis

