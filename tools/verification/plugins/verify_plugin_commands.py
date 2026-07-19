from aletheus.runtime import runtime_core

expected = [
    "plugin.bootstrap",
    "plugin.install",
    "plugin.enable",
    "plugin.disable",
    "plugin.update",
    "plugin.remove",
    "plugin.list",
    "plugin.status",
    "plugin.statistics",
]

commands = runtime_core.commands.list()

missing = [c for c in expected if c not in commands]

print("Missing Commands:", missing)
print("Total Commands:", len(commands))
