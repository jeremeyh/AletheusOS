from aletheus.runtime import runtime_core

print("\n===== REGISTERED AGENT COMMANDS =====")

for command in sorted(runtime_core.commands.commands.keys()):
    if command.startswith("agent."):
        print(command)

print("\n===== TOTAL COMMANDS =====")
print(len(runtime_core.commands.commands))
