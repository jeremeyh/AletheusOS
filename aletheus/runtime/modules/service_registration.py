"""
AletheusOS Runtime Service Registration
Version 4.5.0
"""

from __future__ import annotations


def register_runtime_services(runtime):
    """
    Register all runtime services.

    Centralizing this logic removes another responsibility
    from runtime/core.py.
    """

    runtime.services.register("commands", runtime.commands)
    runtime.services.register("events", runtime.events)
    runtime.services.register("metrics", runtime.metrics)
    runtime.services.register("compatibility", runtime.compat)
    runtime.services.register("kernel", runtime.kernel)

    runtime.services.register("governance", runtime.governance)
    runtime.services.register("doctor", runtime.runtime_doctor)
    runtime.services.register("boot_validator", runtime.boot_validator)
    runtime.services.register("invariants", runtime.runtime_invariants)

    return runtime.services.statistics()
