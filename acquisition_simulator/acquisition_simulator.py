from portfolio_digital_twin.digital_twin_service import PortfolioDigitalTwin


class AcquisitionSimulator:
    """Acquisition Simulator™ models impact of a potential purchase."""

    @staticmethod
    def simulate(assets, title, ask_price, estimated_value, thorx_score=0):
        twin = PortfolioDigitalTwin.simulate_add(assets, ask_price, estimated_value)
        recommendation = "Pass"
        if thorx_score >= 9.0 and estimated_value >= ask_price:
            recommendation = "Buy"
        elif thorx_score >= 8.0:
            recommendation = "Watch / Negotiate"

        return {
            "title": title,
            "ask_price": ask_price,
            "estimated_value": estimated_value,
            "thorx_score": thorx_score,
            "recommendation": recommendation,
            "portfolio_impact": twin,
        }
