"""
Universal Capability Registry

Genesis 91.5
"""


class UniversalCapabilityRegistry:


    def __init__(self):

        self.capabilities = []



    def register(self, capability):

        self.capabilities.append(
            capability
        )



    def list_capabilities(self):

        return self.capabilities

