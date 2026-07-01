"""
Runtime Command Registration

Version 4.8.1
"""


def register_runtime_commands(runtime):

    commands = runtime.commands

    commands.register(
        "runtime.health",
        runtime._cmd_health,
    )

    commands.register(
        "runtime.diagnostics",
        runtime._cmd_diagnostics,
    )

    commands.register(
        "runtime.selftest",
        runtime._cmd_runtime_selftest,
    )

    commands.register(
        "runtime.dashboard",
        runtime._cmd_runtime_dashboard,
    )

    commands.register(
        "runtime.snapshot",
        runtime._cmd_runtime_snapshot,
    )

    commands.register(
        "runtime.audit",
        runtime._cmd_runtime_audit,
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
