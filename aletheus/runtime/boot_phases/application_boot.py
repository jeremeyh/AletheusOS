class RuntimeApplicationBootPhase:
    """
    Runtime Application Boot Phase™

    Boots built-in runtime applications.
    """

    def run(self, runtime):

        runtime.applications.register_card_hawk_foundation()

        return {
            "applications": [
                "Card Hawk Foundation",
            ],
        }
