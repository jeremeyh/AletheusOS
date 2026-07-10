"""
Capability Registry

Post-Genesis 37
"""


class CapabilityRegistry:


    def __init__(self):

        self.capabilities = {}



    def register(self, name, capability):

        self.capabilities[name] = capability

        return {

            "capability":
            name,

            "status":
            "registered"

        }



    def list(self):

        return self.capabilities

