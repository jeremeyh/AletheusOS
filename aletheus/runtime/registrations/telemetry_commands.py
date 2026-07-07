"""
Telemetry Command Registration

Genesis 6
"""

def register_telemetry_commands(runtime):

    commands = runtime.commands

    commands.register(
        "telemetry.bootstrap",
        runtime._cmd_telemetry_bootstrap,
    )

    commands.register(
        "telemetry.record",
        runtime._cmd_telemetry_record,
    )

    commands.register(
        "telemetry.metric",
        runtime._cmd_telemetry_metric,
    )

    commands.register(
        "telemetry.log",
        runtime._cmd_telemetry_log,
    )

    commands.register(
        "telemetry.trace",
        runtime._cmd_telemetry_trace,
    )

    commands.register(
        "telemetry.health",
        runtime._cmd_telemetry_health,
    )

    commands.register(
        "telemetry.timeline",
        runtime._cmd_telemetry_timeline,
    )

    commands.register(
        "telemetry.statistics",
        runtime._cmd_telemetry_statistics,
    )
