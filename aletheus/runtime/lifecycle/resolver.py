"""
Runtime lifecycle resolver.

Provides backward-compatible lifecycle resolution without replacing
the canonical RuntimeLifecycleState implementation.
"""

from __future__ import annotations


def resolve_runtime_lifecycle(runtime) -> str:
    lifecycle = getattr(runtime, "lifecycle", None)
    if lifecycle is not None:
        state = getattr(lifecycle, "state", None)
        if state is not None:
            value = getattr(state, "value", state)
            return str(value)

    state = getattr(runtime, "state", None)
    if state is not None:
        return str(state)

    status = getattr(runtime, "status", None)
    if status is not None:
        return str(status)

    return "unknown"
