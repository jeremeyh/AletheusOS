class ThorX:

    @staticmethod
    def score(asset):

        score = 50

        if asset.get("grade") == "Gem Mint":
            score += 20

        if asset.get("year") == 2022:
            score += 5

        if asset.get("brand") == "Leaf":
            score += 3

        if asset.get("player") == "Caleb Williams":
            score += 20

        return min(score, 100)
