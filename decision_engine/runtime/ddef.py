class DDEF:
    """
    Deep Decision Engine Framework™

    Multi-factor collectible investment evaluation.
    """

    @staticmethod
    def score(asset):
        thorx = float(asset.get("thorx_score") or 0)
        market_score = float(asset.get("market_score") or 0)
        risk_score = float(asset.get("risk_score") or 0)
        confidence = float(asset.get("hawk_aeye_confidence") or 0)
        current = float(asset.get("current_value") or 0)
        purchase = float(asset.get("purchase_price") or 0)
        ceiling = float(asset.get("ceiling") or 0)
        floor = float(asset.get("floor") or 0)

        scarcity = float(asset.get("scarcity_score") or 0)
        liquidity = float(asset.get("liquidity_score") or 0)
        eye = float(asset.get("eye_appeal_score") or 0)
        player = float(asset.get("player_thesis_score") or 0)
        portfolio_fit = float(asset.get("portfolio_fit_score") or 0)

        if scarcity == 0:
            scarcity = 65

            if asset.get("serial_number"):
                scarcity += 10

            if asset.get("print_run"):
                run = int(asset.get("print_run") or 999)

                if run <= 10:
                    scarcity += 20
                elif run <= 25:
                    scarcity += 15
                elif run <= 50:
                    scarcity += 10

        if liquidity == 0:
            comps = int(asset.get("active_listings") or asset.get("sold_comps") or 0)
            liquidity = min(50 + comps * 8, 90)

        if eye == 0:
            eye = confidence or 70

        if player == 0:
            player_name = (asset.get("player") or "").lower()

            if "caleb" in player_name:
                player = 88
            elif "rome" in player_name:
                player = 82
            else:
                player = 70

        if portfolio_fit == 0:
            portfolio_fit = 75

        roi_component = 50

        if purchase > 0:
            roi = ((current - purchase) / purchase) * 100
            roi_component = max(0, min(50 + roi, 100))

        upside_component = 50

        if current > 0 and ceiling > current:
            upside_component = min(50 + ((ceiling - current) / current) * 10, 100)

        floor_component = 70

        if current > 0 and floor > 0:
            floor_component = max(0, min((floor / current) * 100, 100))

        if market_score == 0:
            market_score = float(asset.get("confidence") or 70)

        if risk_score == 0:
            risk_score = 100 - max(0, 100 - floor_component)

        score = (
            thorx * 0.18
            + scarcity * 0.13
            + liquidity * 0.10
            + eye * 0.10
            + player * 0.14
            + portfolio_fit * 0.10
            + roi_component * 0.08
            + upside_component * 0.09
            + market_score * 0.05
            + risk_score * 0.03
        )

        return round(max(0, min(score, 100)), 2)
