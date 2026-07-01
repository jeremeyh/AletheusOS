"""
AletheusOS Runtime Registration Package

Version 4.7.0
"""

from .runtime_commands import register_runtime_commands
from .memory_commands import register_memory_commands
from .reasoning_commands import register_reasoning_commands

__all__ = [
    "register_runtime_commands",
    "register_memory_commands",
    "register_reasoning_commands",
]

