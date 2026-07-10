"""
Genesis 8.58
Cognitive Capability Registry
"""


class CognitiveCapabilityRegistry:


    def __init__(self):

        self.capabilities={}



    def register(
        self,
        name,
        version
    ):

        self.capabilities[name]={

            "version":
                version

        }



    def snapshot(self):

        return {

            "capabilities":
                len(self.capabilities)

        }
