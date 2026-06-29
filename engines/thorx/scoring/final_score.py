class FinalScore:

    @staticmethod
    def calculate(
        player,
        scarcity,
        market,
        condition,
    ):

        return round(
            (
                player * 0.40
                + scarcity * 0.25
                + market * 0.20
                + condition * 0.15
            ),
            2,
        )
