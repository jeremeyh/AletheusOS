"""
Memory Command Registration

Genesis 7 Integration
"""

from __future__ import annotations

from aletheus.runtime.domains import MemoryDomain


def register_memory_commands(runtime):
    """
    Register memory command implementations.
    """

    domain = MemoryDomain(runtime)

    runtime.commands.register(
        "memory.remember",
        domain.remember,
    )

    runtime.commands.register(
        "memory.recall",
        domain.recall,
    )

    runtime.commands.register(
        "memory.stats",
        domain.statistics,
    )

    runtime.commands.register(
        "memory.clear_working",
        domain.clear_working,
    )
