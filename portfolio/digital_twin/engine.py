from portfolio.runtime.engine import PortfolioEngine


class PortfolioDigitalTwin:
    """
    Portfolio Digital Twin™

    Compatibility wrapper around the live Portfolio Engine.
    """

    @staticmethod
    def snapshot():

        return PortfolioEngine.snapshot()
