from marketplace.runtime.market_snapshot import MarketSnapshot


class ValuationEngine:
    """
    CardHawkOS Valuation Engine™

    Converts market snapshots into action signals.
    """

    @staticmethod
    def evaluate(asset):
        market = MarketSnapshot.build(asset)

        current_value = float(market.get("current_value") or 0)
        purchase_price = float(asset.get("purchase_price") or 0)
        thorx = float(asset.get("thorx_score") or 0)

        gain_loss = current_value - purchase_price

        roi = 0.0

        if purchase_price > 0:
            roi = (gain_loss / purchase_price) * 100

        rating = "HOLD"

        if thorx >= 90 and roi >= 10:
            rating = "BUY"
        elif thorx >= 80 and roi >= 0:
            rating = "HOLD"
        elif roi < -20:
            rating = "REVIEW"
        elif thorx < 60:
            rating = "PASS"

        return {
            "asset_id": asset.get("id"),
            "player": asset.get("player"),
            "market": market,
            "current_value": round(current_value, 2),
            "purchase_price": round(purchase_price, 2),
            "gain_loss": round(gain_loss, 2),
            "roi": round(roi, 2),
            "thorx": thorx,
            "rating": rating,
        }
