"""
Aletheus Cognitive Engine Base
"""


import time
import uuid


class CognitiveEngine:


    def __init__(
        self,
        name,
        layer
    ):

        self.id = str(
            uuid.uuid4()
        )

        self.name = name

        self.layer = layer

        self.created = time.time()

        self.active = True



    def execute(
        self,
        payload=None
    ):

        return {

            "engine":
                self.name,

            "layer":
                self.layer,

            "processed":
                True,

            "payload":
                payload

        }



    def status(self):

        return {

            "name":
                self.name,

            "layer":
                self.layer,

            "active":
                self.active

        }

