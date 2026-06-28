class ScarcityScorer:
    """Scarcity™ scoring based on print run, serial scarcity, SSP/case-hit flags."""

    @staticmethod
    def score(asset):
        pr = getattr(asset, "print_run", None)
        one_of_one = bool(getattr(asset, "one_of_one", False))
        ssp = bool(getattr(asset, "ssp", False))
        case_hit = bool(getattr(asset, "case_hit", False))

        if one_of_one:
            base = 10.0
        elif pr is None or pr == 0:
            base = 4.5
        elif pr <= 5:
            base = 9.8
        elif pr <= 10:
            base = 9.5
        elif pr <= 25:
            base = 9.0
        elif pr <= 50:
            base = 8.2
        elif pr <= 99:
            base = 7.4
        elif pr <= 199:
            base = 6.4
        else:
            base = 5.0

        if ssp:
            base += 0.7
        if case_hit:
            base += 0.5

        return min(round(base, 2), 10.0)
