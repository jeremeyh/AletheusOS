class ExplanationEngine:
    """
    DEF Explanation Engine™

    Produces human-readable reasons.
    """

    @staticmethod
    def explain(asset, qdef_score, ddef_score, recommendation):
        reasons = []

        thorx = float(asset.get("thorx_score") or 0)
        current = float(asset.get("current_value") or 0)
        purchase = float(asset.get("purchase_price") or 0)
        ceiling = float(asset.get("ceiling") or 0)

        if thorx >= 85:
            reasons.append("Strong THORᵡ profile.")

        if asset.get("serial_number") or asset.get("print_run"):
            reasons.append("Scarcity signal detected.")

        if asset.get("autograph"):
            reasons.append("Autograph premium adds collectible strength.")

        if asset.get("patch"):
            reasons.append("Patch/memorabilia component increases asset appeal.")

        if purchase > 0 and current > purchase:
            reasons.append("Current value is above cost basis.")

        if current > 0 and ceiling > current:
            reasons.append(
                "Meaningful upside exists between current value and ceiling."
            )

        if float(asset.get("hawk_aeye_confidence") or 0) >= 80:
            reasons.append("Hawk A•Eye™ confidence is strong.")

        if recommendation in ["STRIKE", "BUY"]:
            reasons.append("DEF recommends active acquisition or accumulation.")
        elif recommendation == "HOLD":
            reasons.append(
                "Asset remains portfolio-worthy but does not demand urgent action."
            )
        elif recommendation == "WATCH":
            reasons.append(
                "Asset has some signals but needs stronger market confirmation."
            )
        else:
            reasons.append("Risk/reward profile is currently below CardHawk standards.")

        if not reasons:
            reasons.append("Insufficient signal density for a strong recommendation.")

        return reasons
