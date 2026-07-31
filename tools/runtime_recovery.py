from aletheus.runtime.recovery import RuntimeRecoveryManager

manager = RuntimeRecoveryManager()

manager.recover(
    "memory",
    "Connection timeout",
)

manager.recover(
    "scheduler",
    "Heartbeat failure",
)

print("========================================================")
print("ALETHEUSOS RUNTIME RECOVERY")
print("========================================================")
print()

for event in manager.history():
    print(event)

print()
print(f"Recovery Events...............{manager.count()}")
print("========================================================")
