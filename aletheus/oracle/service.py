from .forecasting_engine import ForecastingEngine


class OracleService:
    authority='Oracle™'
    family='Platform Intelligence'
    knows='Architectural Forecasting'
    def __init__(self):
        self.engine=ForecastingEngine()
    def forecast(self):
        return self.engine.forecast()
