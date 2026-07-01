"""
AletheusOS Runtime Registration Package

Version 4.6.2
"""

from .runtime_commands import register_runtime_commands
from .memory_commands import register_memory_commands

__all__ = [
    "register_runtime_commands",
    "register_memory_commands",
]
