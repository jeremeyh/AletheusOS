class PortfolioSimulationLab:
    """7.0C — Portfolio Simulation Lab™."""

    @staticmethod
    def compare(options):
        results = []
        for option in options:
            name = option.get("name", "Scenario")
            current_value = float(option.get("current_value", 0) or 0)
            cost = float(option.get("cost", 0) or 0)
            expected_value = float(option.get("expected_value", current_value) or 0)
            risk = float(option.get("risk", 0.5) or 0.5)
            gain = expected_value - cost
            risk_adjusted = gain * (1 - risk)
            results.append({
                "name": name,
                "cost": cost,
                "expected_value": expected_value,
                "expected_gain": round(gain, 2),
                "risk": risk,
                "risk_adjusted_gain": round(risk_adjusted, 2),
                "recommendation": "Best" if risk_adjusted == max([risk_adjusted]) else "Compare",
            })

        if results:
            best = max(results, key=lambda x: x["risk_adjusted_gain"])
            for r in results:
                r["recommendation"] = "Best" if r is best else "Alternative"

        return results

    @staticmethod
    def grade_vs_raw(raw_value, grading_cost, gem_value, gem_probability):
        raw_value = float(raw_value or 0)
        grading_cost = float(grading_cost or 0)
        gem_value = float(gem_value or 0)
        gem_probability = float(gem_probability or 0)
        expected = gem_value * gem_probability + raw_value * (1 - gem_probability) - grading_cost
        return {
            "sell_raw_value": raw_value,
            "grade_expected_value": round(expected, 2),
            "recommendation": "Grade" if expected > raw_value else "Sell Raw / Hold",
        }
