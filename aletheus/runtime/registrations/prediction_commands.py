"""
Prediction Command Registration

Genesis 6
"""

from aletheus.runtime.domains import PredictionDomain


def register_prediction_commands(runtime):

    commands = runtime.commands
    domain = PredictionDomain(runtime)

    commands.register(
        "prediction.forecast",
        domain.forecast,
    )

    commands.register(
        "prediction.scenario",
        domain.scenario,
    )

    commands.register(
        "prediction.risks",
        domain.risks,
    )

    commands.register(
        "prediction.opportunities",
        domain.opportunities,
    )

    commands.register(
        "prediction.recommend",
        domain.recommend,
    )

    commands.register(
        "prediction.timeline",
        domain.timeline,
    )

    commands.register(
        "prediction.statistics",
        domain.statistics,
    )
