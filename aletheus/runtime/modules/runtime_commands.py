"""
AletheusOS Runtime Command Registration
Version 4.5.0
"""

from __future__ import annotations


def register_core_commands(runtime):
    """
    Register runtime-level commands.

    Additional registration groups will migrate here
    incrementally during v4.5.
    """

    runtime.commands.register("runtime.version", runtime._cmd_runtime_version)
    runtime.commands.register("runtime.status", runtime._cmd_runtime_status)
    runtime.commands.register("runtime.health", runtime._cmd_runtime_health)
    runtime.commands.register("runtime.metrics", runtime._cmd_metrics)
    runtime.commands.register("runtime.events", runtime._cmd_events)

    runtime.commands.register("runtime.doctor", runtime._cmd_runtime_doctor)
    runtime.commands.register(
        "runtime.invariants",
        runtime._cmd_runtime_invariants,
    )
    runtime.commands.register(
        "runtime.boot.validate",
        runtime._cmd_runtime_boot_validate,
    )
