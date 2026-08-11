from asset_core.repository.asset_repository import AssetRepository
from decision_engine.runtime.engine import DecisionEngine
from nest.runtime.score import NestScoringEngine


class FalconForecasting:
    """
    FALCON™ Forecast Engine

    Lightweight projection model for asset and portfolio values.
    """

    @staticmethod
    def forecast_asset(asset):
        current = float(asset.get("current_value") or asset.get("market_value") or 0)
        thorx = float(asset.get("thorx_score") or 0)

        def_report = DecisionEngine.evaluate(asset)
        nest = NestScoringEngine.calculate(asset)

        signal = (
            thorx * 0.30
            + float(def_report.get("final_score") or 0) * 0.40
            + float(nest.score or 0) * 0.30
        )

        growth_factor = max(0, (signal - 50) / 100)

        return {
            "asset_id": asset.get("id"),
            "player": asset.get("player") or "Unknown",
            "current_value": round(current, 2),
            "thirty_day": round(current * (1 + growth_factor * 0.05), 2),
            "ninety_day": round(current * (1 + growth_factor * 0.14), 2),
            "one_year": round(current * (1 + growth_factor * 0.45), 2),
            "confidence": round(signal, 2),
        }

    @staticmethod
    def forecast_portfolio():
        assets = AssetRepository.all(include_archived=False) or []

        forecasts = [FalconForecasting.forecast_asset(asset) for asset in assets]

        return {
            "current_value": round(sum(item["current_value"] for item in forecasts), 2),
            "thirty_day": round(sum(item["thirty_day"] for item in forecasts), 2),
            "ninety_day": round(sum(item["ninety_day"] for item in forecasts), 2),
            "one_year": round(sum(item["one_year"] for item in forecasts), 2),
            "assets": forecasts,
        }
