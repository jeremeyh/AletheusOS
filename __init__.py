"""
AletheusOS compatibility package
"""

from aletheus.runtime.registrations.memory_commands import (
    register_memory_commands,
)

from aletheus.runtime.registrations.reasoning_commands import (
    register_reasoning_commands,
)

from aletheus.runtime.registrations.runtime_commands import (
    register_runtime_commands,
)

__all__ = [
    "register_memory_commands",
    "register_reasoning_commands",
    "register_runtime_commands",
]
