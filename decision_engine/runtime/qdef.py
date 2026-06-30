class QDEF:
    """
    Quick Decision Engine Framework™

    Fast acquisition and asset quality score.
    """

    @staticmethod
    def score(asset):
        thorx = float(asset.get("thorx_score") or 0)
        value = float(asset.get("current_value") or 0)
        floor = float(asset.get("floor") or 0)
        ceiling = float(asset.get("ceiling") or 0)
        confidence = float(asset.get("hawk_aeye_confidence") or 0)

        scarcity_bonus = 0

        if asset.get("serial_number"):
            scarcity_bonus += 8

        if asset.get("print_run"):
            print_run = int(asset.get("print_run") or 999)

            if print_run <= 10:
                scarcity_bonus += 12
            elif print_run <= 25:
                scarcity_bonus += 9
            elif print_run <= 50:
                scarcity_bonus += 6
            elif print_run <= 99:
                scarcity_bonus += 3

        auto_bonus = 5 if asset.get("autograph") else 0
        patch_bonus = 4 if asset.get("patch") else 0
        rookie_bonus = 5 if asset.get("rookie") else 0

        upside = 0

        if value and ceiling:
            upside = min(((ceiling - value) / value) * 10, 15)

        score = (
            thorx * 0.45
            + confidence * 0.15
            + scarcity_bonus
            + auto_bonus
            + patch_bonus
            + rookie_bonus
            + upside
        )

        return round(max(0, min(score, 100)), 2)
