"""
Card Hawk Registry Registrar

Genesis 13.12
"""


from .manifest import (
    CARD_HAWK_CAPABILITIES
)



class CardHawkRegistrar:


    def __init__(
        self,
        runtime=None
    ):

        self.runtime = runtime



    def register(
        self
    ):

        results = []


        if not self.runtime:

            return results


        registry = getattr(
            self.runtime,
            "registry",
            None
        )


        if not registry:

            return results



        for capability in CARD_HAWK_CAPABILITIES:


            registry.register_component(

                capability["id"],

                capability

            )


            results.append(
                capability["id"]
            )


        return results



    def snapshot(self):

        return {

            "domain":
                "card_hawk",

            "capabilities":
                len(
                    CARD_HAWK_CAPABILITIES
                )

        }

