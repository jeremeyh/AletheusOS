from asset_core.repository.asset_repository import AssetRepository


class PortfolioHealth:
    """
    Portfolio Health Engine™

    Computes live portfolio health metrics from Asset Vault.
    """

    @staticmethod
    def snapshot():
        assets = AssetRepository.all(include_archived=False) or []

        total_purchase = 0.0
        total_value = 0.0
        total_thorx = 0.0
        scored_assets = 0

        for asset in assets:
            purchase_price = float(asset.get("purchase_price") or 0)
            current_value = float(
                asset.get("current_value")
                or asset.get("market_value")
                or 0
            )
            thorx_score = float(asset.get("thorx_score") or 0)

            total_purchase += purchase_price
            total_value += current_value

            if thorx_score > 0:
                total_thorx += thorx_score
                scored_assets += 1

        asset_count = len(assets)
        gain_loss = total_value - total_purchase

        roi = 0.0
        if total_purchase > 0:
            roi = (gain_loss / total_purchase) * 100

        avg_thorx = 0.0
        if scored_assets > 0:
            avg_thorx = total_thorx / scored_assets

        return {
            "asset_count": asset_count,
            "purchase": round(total_purchase, 2),
            "value": round(total_value, 2),
            "gain": round(gain_loss, 2),
            "roi": round(roi, 2),
            "avg_thorx": round(avg_thorx, 2),
        }
