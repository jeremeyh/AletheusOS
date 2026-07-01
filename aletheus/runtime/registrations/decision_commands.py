"""
Decision Command Registration

Version 4.7.1
"""


def register_decision_commands(runtime):

    commands = runtime.commands

    commands.register(
        "decision.bootstrap",
        runtime._cmd_decision_bootstrap,
    )

    commands.register(
        "decision.policy.add",
        runtime._cmd_decision_policy_add,
    )

    commands.register(
        "decision.evaluate",
        runtime._cmd_decision_evaluate,
    )

    commands.register(
        "decision.execute",
        runtime._cmd_decision_execute,
    )

    commands.register(
        "decision.rollback",
        runtime._cmd_decision_rollback,
    )

    commands.register(
        "decision.explain",
        runtime._cmd_decision_explain,
    )

    commands.register(
        "decision.record",
        runtime._cmd_decision_record,
    )

    commands.register(
        "decision.history",
        runtime._cmd_decision_history,
    )

    commands.register(
        "decision.statistics",
        runtime._cmd_decision_statistics,
    )
