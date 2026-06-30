class RankingEngine:
    """
    DEF Ranking Engine™
    """

    @staticmethod
    def rank(reports):
        return sorted(
            reports,
            key=lambda report: report.get("final_score", 0),
            reverse=True,
        )
