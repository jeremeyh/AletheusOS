"""
Prediction Command Registration

Genesis 6
"""

def register_prediction_commands(runtime):

    commands = runtime.commands

    commands.register(
        "predict.forecast",
        runtime._cmd_predict_forecast,
    )

    commands.register(
        "predict.scenario",
        runtime._cmd_predict_scenario,
    )

    commands.register(
        "predict.risks",
        runtime._cmd_predict_risks,
    )

    commands.register(
        "predict.opportunities",
        runtime._cmd_predict_opportunities,
    )

    commands.register(
        "predict.recommend",
        runtime._cmd_predict_recommend,
    )

    commands.register(
        "predict.timeline",
        runtime._cmd_predict_timeline,
    )

    commands.register(
        "predict.stats",
        runtime._cmd_predict_stats,
    )
