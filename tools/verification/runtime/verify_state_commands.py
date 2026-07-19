from aletheus.runtime import runtime_core

expected = [
    "state.bootstrap",
    "state.save",
    "state.load",
    "state.snapshot",
    "state.restore",
    "state.export",
    "state.import",
    "state.statistics",
]

commands = runtime_core.commands.list()

missing = [c for c in expected if c not in commands]

print("Missing:", missing)
