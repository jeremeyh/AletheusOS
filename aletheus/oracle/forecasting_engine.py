from .models import Forecast


class ForecastingEngine:
    def forecast(self):
        return Forecast("architecture", 0.80, "No critical structural risk detected.")
