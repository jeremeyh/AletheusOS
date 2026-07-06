from aletheus.runtime.commands.uci_commands import register_uci_commands
from aletheus.runtime.commands.intent_commands import register_intent_commands
from aletheus.runtime.commands.diagnostics_commands import register_diagnostics_commands
from aletheus.runtime.commands.memory_commands import register_memory_commands

__all__ = [
    "register_uci_commands",
    "register_intent_commands",
    "register_diagnostics_commands",
    "register_memory_commands",
]
