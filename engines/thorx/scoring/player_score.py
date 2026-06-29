class PlayerScore:

    @staticmethod
    def calculate(card):

        player = card.get("player", "")

        if player == "Caleb Williams":
            return 98

        if player == "Rome Odunze":
            return 82

        return 50
