class StrikeZone:
    """
    Strike Zone™ visual opportunity rating.
    """

    @staticmethod
    def stars(score):
        if score >= 92:
            return "★★★★★"

        if score >= 82:
            return "★★★★☆"

        if score >= 70:
            return "★★★☆☆"

        if score >= 58:
            return "★★☆☆☆"

        return "★☆☆☆☆"
