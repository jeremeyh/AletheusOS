from services.asset_service import AssetService


class PortfolioService:
    """
    Portfolio Engine™ Service

    Computes portfolio-level metrics from Asset Vault™ records.
    """

    @staticmethod
    def snapshot() -> dict:
        assets = AssetService.get_all()

        total_assets = len(assets)
        cost_basis = 0
        current_value = 0

        for asset in assets:
            cost_basis += float(asset["cost_basis"] or asset["purchase_price"] or 0)
            current_value += float(asset["current_value"] or asset["market_value"] or 0)

        gain_loss = current_value - cost_basis
        roi = (gain_loss / cost_basis * 100) if cost_basis else 0

        return {
            "total_assets": total_assets,
            "cost_basis": cost_basis,
            "current_value": current_value,
            "gain_loss": gain_loss,
            "roi": roi,
        }

    @staticmethod
    def allocation_by(field: str) -> dict:
        assets = AssetService.get_all()
        allocation = {}

        for asset in assets:
            key = asset[field] if field in asset.keys() and asset[field] else "Unassigned"
            allocation[key] = allocation.get(key, 0) + float(asset["current_value"] or 0)

        return allocation
