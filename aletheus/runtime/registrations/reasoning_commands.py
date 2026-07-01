"""
Reasoning Command Registration

Version 4.7.0
"""


def register_reasoning_commands(runtime):

    commands = runtime.commands

    commands.register(
        "reason.bootstrap",
        runtime._cmd_reason_bootstrap,
    )

    commands.register(
        "reason.rule.add",
        runtime._cmd_reason_rule_add,
    )

    commands.register(
        "reason.evaluate",
        runtime._cmd_reason_evaluate,
    )

    commands.register(
        "reason.history",
        runtime._cmd_reason_history,
    )

    commands.register(
        "reason.explain",
        runtime._cmd_reason_explain,
    )

    commands.register(
        "reason.trace",
        runtime._cmd_reason_trace,
    )

    commands.register(
        "reason.decision",
        runtime._cmd_reason_decision,
    )

    commands.register(
        "reason.confidence",
        runtime._cmd_reason_confidence,
    )

    commands.register(
        "reason.statistics",
        runtime._cmd_reason_statistics,
    )
