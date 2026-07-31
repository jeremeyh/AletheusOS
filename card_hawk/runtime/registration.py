"""
Capability Registration

Genesis 14.15
"""


class CapabilityRegistry:
    def __init__(self):

        self.capabilities = []

    def register(self, capability):

        self.capabilities.append(capability)
