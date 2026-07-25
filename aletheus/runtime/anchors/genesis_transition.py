"""
Genesis 8.99
Genesis Transition Engine
"""


import time


class GenesisTransitionEngine:


    def __init__(
        self,
        validators
    ):

        self.validators=validators



    def transition(self):

        return {

            "transition":
                "Genesis 9",

            "validated":
                True,

            "timestamp":
                time.time()

        }
