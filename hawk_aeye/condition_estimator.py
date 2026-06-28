class ConditionEstimator:
    """
    Alpha 0.7 condition placeholder.

    Later versions will estimate centering, corners, edges, surface, and grade risk.
    """

    def estimate(self, image_path: str) -> dict:
        return {
            "centering": None,
            "corners": None,
            "edges": None,
            "surface": None,
            "condition_score": 0.0,
            "notes": ["Condition estimation staged; visual scoring not enabled yet."],
        }
