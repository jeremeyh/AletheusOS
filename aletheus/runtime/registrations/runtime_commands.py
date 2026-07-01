"""
Runtime Command Registration

Version 4.6.0
"""


def register_runtime_commands(runtime):

    commands = runtime.commands

    commands.register(
        "runtime.version",
        runtime._cmd_runtime_version,
    )

    commands.register(
        "runtime.status",
        runtime._cmd_runtime_status,
    )

    commands.register(
        "runtime.health",
        runtime._cmd_runtime_health,
    )

    commands.register(
        "runtime.metrics",
        runtime._cmd_metrics,
    )

    commands.register(
        "runtime.events",
        runtime._cmd_events,
    )

    commands.register(
        "runtime.queue",
        runtime._cmd_queue,
    )

    commands.register(
        "runtime.run_next_job",
        runtime._cmd_run_next_job,
    )

    commands.register(
        "runtime.docs",
        runtime._cmd_runtime_docs,
    )

    commands.register(
        "runtime.doctor",
        runtime._cmd_runtime_doctor,
    )

    commands.register(
        "runtime.invariants",
        runtime._cmd_runtime_invariants,
    )

    commands.register(
        "runtime.boot.validate",
        runtime._cmd_runtime_boot_validate,
    )

    commands.register(
        "runtime.health_report",
        runtime._cmd_runtime_health_report,
    )
