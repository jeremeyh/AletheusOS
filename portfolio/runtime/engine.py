from asset_core.repository.asset_repository import AssetRepository


class PortfolioEngine:
    """
    CardHawkOS™

    Live Portfolio Engine
    """

    @staticmethod
    def snapshot():

        # --------------------------------------------------
        # Load Assets
        # --------------------------------------------------

        assets = AssetRepository.all(include_archived=False)

        if assets is None:
            assets = []

        asset_count = len(assets)

        # --------------------------------------------------
        # Empty Portfolio
        # --------------------------------------------------

        if asset_count == 0:
            return {
                "asset_count": 0,
                "total_value": 0.0,
                "total_cost": 0.0,
                "gain_loss": 0.0,
                "average_thorx": 0.0,
                "allocation_by_player": {},
                "allocation_by_brand": {},
                "allocation_by_sport": {},
                "top_assets": [],
                "highest_thorx": [],
                "assets": [],
            }

        # --------------------------------------------------
        # Portfolio Totals
        # --------------------------------------------------

        total_value = 0.0
        total_cost = 0.0

        thorx_scores = []

        allocation_by_player = {}
        allocation_by_brand = {}
        allocation_by_sport = {}

        # --------------------------------------------------
        # Iterate Assets
        # --------------------------------------------------

        for asset in assets:
            value = float(asset.get("current_value") or 0)
            cost = float(asset.get("purchase_price") or 0)
            thorx = float(asset.get("thorx_score") or 0)

            total_value += value
            total_cost += cost

            if thorx > 0:
                thorx_scores.append(thorx)

            player = asset.get("player") or "Unknown"
            brand = asset.get("brand") or "Unknown"
            sport = asset.get("sport") or "Unknown"

            allocation_by_player[player] = allocation_by_player.get(player, 0) + value

            allocation_by_brand[brand] = allocation_by_brand.get(brand, 0) + value

            allocation_by_sport[sport] = allocation_by_sport.get(sport, 0) + value

        # --------------------------------------------------
        # Metrics
        # --------------------------------------------------

        gain_loss = total_value - total_cost

        average_thorx = sum(thorx_scores) / len(thorx_scores) if thorx_scores else 0.0

        # --------------------------------------------------
        # Rankings
        # --------------------------------------------------

        top_assets = sorted(
            assets,
            key=lambda asset: float(asset.get("current_value") or 0),
            reverse=True,
        )

        highest_thorx = sorted(
            assets,
            key=lambda asset: float(asset.get("thorx_score") or 0),
            reverse=True,
        )

        # --------------------------------------------------
        # Snapshot
        # --------------------------------------------------

        return {
            "asset_count": asset_count,
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "gain_loss": round(gain_loss, 2),
            "average_thorx": round(average_thorx, 2),
            "allocation_by_player": allocation_by_player,
            "allocation_by_brand": allocation_by_brand,
            "allocation_by_sport": allocation_by_sport,
            "top_assets": top_assets[:10],
            "highest_thorx": highest_thorx[:10],
            "assets": assets,
        }
