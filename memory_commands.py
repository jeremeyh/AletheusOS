"""
Compatibility bridge.

Legacy Genesis tests imported:
    AletheusOS_FIX.memory_commands

Canonical implementation now lives at:
    aletheus.runtime.registrations.memory_commands
"""

from aletheus.runtime.registrations.memory_commands import (
    register_memory_commands,
)

__all__ = [
    "register_memory_commands",
]
