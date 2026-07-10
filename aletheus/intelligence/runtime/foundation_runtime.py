"""
Aletheus Foundation Runtime

Composition root for intelligence layers.
"""


class FoundationRuntime:


    def __init__(self):

        self.layers = {}



    def attach(
        self,
        name,
        component
    ):

        self.layers[name] = component



    def status(self):

        return {

            "layers":
                list(
                    self.layers.keys()
                ),

            "active":
                True

        }

