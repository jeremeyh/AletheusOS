"""
Aletheus Intelligence Registry

Foundation registry for cognitive engines.
"""


class IntelligenceRegistry:


    def __init__(self):

        self.engines = {}



    def register(
        self,
        name,
        engine
    ):

        self.engines[name] = engine



    def get(
        self,
        name
    ):

        return self.engines.get(name)



    def list_engines(self):

        return list(
            self.engines.keys()
        )



    def status(self):

        return {

            "engine_count":
                len(self.engines),

            "registry_active":
                True

        }

