from collections import defaultdict

from components.cardhawk_utils import roi_percent, row_value, safe_float


class PortfolioAnalyticsService:
    """CardHawk OS™ 6.0D Portfolio Analytics™."""

    @staticmethod
    def allocation(assets, field):
        totals = defaultdict(float)
        for asset in assets or []:
            key = row_value(asset, field, "Unknown") or "Unknown"
            totals[str(key)] += safe_float(row_value(asset, "current_value", 0))
        return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))

    @staticmethod
    def distribution(assets, field):
        counts = defaultdict(int)
        for asset in assets or []:
            key = row_value(asset, field, "Unknown") or "Unknown"
            counts[str(key)] += 1
        return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    @staticmethod
    def risk_distribution(assets):
        out = {"High": 0, "Medium": 0, "Low": 0}
        for asset in assets or []:
            thorx = safe_float(row_value(asset, "thorx_score", 0))
            if thorx >= 9:
                out["Low"] += 1
            elif thorx >= 7:
                out["Medium"] += 1
            else:
                out["High"] += 1
        return out

    @staticmethod
    def capital_efficiency(assets):
        rows = []
        for asset in assets or []:
            rows.append(
                {
                    "asset": row_value(asset, "player", "Unknown Asset"),
                    "roi_percent": roi_percent(
                        row_value(asset, "purchase_price", 0),
                        row_value(asset, "current_value", 0),
                    ),
                    "thorx_score": safe_float(row_value(asset, "thorx_score", 0)),
                    "current_value": safe_float(row_value(asset, "current_value", 0)),
                }
            )
        return sorted(rows, key=lambda x: x["roi_percent"], reverse=True)
