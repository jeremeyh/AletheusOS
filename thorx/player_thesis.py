class PlayerThesisScorer:
    """Player Thesis™ Alpha heuristic."""

    HIGH_CONVICTION = {
        "Caleb Williams": 10.0,
        "Rome Odunze": 9.0,
        "Garrett Wilson": 8.8,
        "Amen Thompson": 9.0,
        "Matas Buzelis": 8.8,
        "Noa Essengue": 8.8,
        "Will Anderson": 8.7,
        "Isaiah Thomas": 8.5,
        "Derrick Rose": 8.4,
    }

    @staticmethod
    def score(asset):
        player = getattr(asset, "player", "") or ""
        return PlayerThesisScorer.HIGH_CONVICTION.get(player, 6.0)
