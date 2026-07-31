"""
Genesis Capability Index

Post-Genesis 80.5
"""


class GenesisIndex:
    def __init__(self):

        self.index = {}

    def add(self, genesis, capability):

        self.index[str(genesis)] = capability

    def lookup(self, genesis):

        return self.index.get(str(genesis))
