class ScarcityScore:

    @staticmethod
    def calculate(card):

        serial = str(card.get("serial", ""))

        if "/10" in serial:
            return 100

        if "/25" in serial:
            return 95

        if "/50" in serial:
            return 90

        if "/99" in serial:
            return 80

        return 50
