"""
Capability Registry

Genesis 60.6
"""


class CapabilityRegistry:


    def __init__(self):

        self.registry = []


    def register(self, capability):

        self.registry.append(capability)


    def list_all(self):

        return self.registry

