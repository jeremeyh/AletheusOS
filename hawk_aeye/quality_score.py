class QualityScore:
    """Combines visual quality signals."""

    @staticmethod
    def score(*values):
        nums = [float(v) for v in values if v is not None]
        if not nums:
            return 0.0
        return round(sum(nums) / len(nums), 2)
