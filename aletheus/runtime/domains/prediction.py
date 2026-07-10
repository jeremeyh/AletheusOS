from __future__ import annotations


class PredictionDomain:
    """
    Prediction capability domain.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def forecast(self, context):
        forecast = self.runtime.prediction.forecast(
            runtime=self.runtime,
            horizon=context.payload.get("horizon", "next sprint"),
        )
        context.add_result("forecast", forecast.to_dict())
        return context

    def scenario(self, context):
        scenario = self.runtime.prediction.scenario(
            title=context.payload.get("title", "Untitled Scenario"),
            premise=context.payload.get("premise", ""),
            runtime=self.runtime,
        )
        context.add_result("scenario", scenario.to_dict())
        return context

    def risks(self, context):
        context.add_result(
            "risks",
            self.runtime.prediction.risks(self.runtime),
        )
        return context

    def opportunities(self, context):
        context.add_result(
            "opportunities",
            self.runtime.prediction.opportunities(self.runtime),
        )
        return context

    def recommend(self, context):
        recommendations = self.runtime.prediction.recommend(self.runtime)

        self.runtime.memory.remember(
            key="predictive_recommendations",
            value=recommendations,
            namespace="aletheus.prediction",
            memory_type="decision",
            tags=["prediction", "recommendation"],
        )

        context.add_result("recommendations", recommendations)
        return context

    def timeline(self, context):
        context.add_result(
            "timeline",
            self.runtime.prediction.timeline(self.runtime),
        )
        return context

    def statistics(self, context):
        context.add_result(
            "prediction_stats",
            (
                self.runtime.prediction.stats()
                if hasattr(self.runtime.prediction, "stats")
                else self.runtime.prediction.statistics()
            ),
        )
        return context
