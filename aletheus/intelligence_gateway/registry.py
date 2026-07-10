"""
API Capability Registry

Genesis 13.43
"""


class APICapabilityRegistry:


    def __init__(self):

        self.capabilities = {}



    def register(
        self,
        name,
        handler
    ):

        self.capabilities[name] = handler

