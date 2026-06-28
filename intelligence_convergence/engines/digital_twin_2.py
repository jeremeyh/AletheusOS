from components.cardhawk_utils import row_value, safe_float

class DigitalTwin2:
    """Digital Twin 2.0™ simulates portfolio futures."""

    SCENARIOS = {
        "Player MVP": 2.5,
        "PSA 10 Grade": 1.85,
        "Championship Run": 1.75,
        "Market Pullback": 0.72,
        "Injury / Thesis Break": 0.45,
        "Base Case": 1.0,
    }

    @staticmethod
    def simulate_asset(asset, scenario="Base Case"):
        multiplier = DigitalTwin2.SCENARIOS.get(scenario, 1.0)
        current = safe_float(row_value(asset, "current_value", 0))
        return {
            "scenario": scenario,
            "current_value": current,
            "simulated_value": round(current * multiplier, 2),
            "delta": round(current * multiplier - current, 2),
            "multiplier": multiplier,
        }

    @staticmethod
    def simulate_portfolio(assets, scenario="Base Case"):
        rows = [DigitalTwin2.simulate_asset(a, scenario) for a in assets or []]
        current = sum(r["current_value"] for r in rows)
        simulated = sum(r["simulated_value"] for r in rows)
        return {
            "scenario": scenario,
            "current_portfolio_value": round(current, 2),
            "simulated_portfolio_value": round(simulated, 2),
            "delta": round(simulated - current, 2),
            "assets": rows,
        }
