from aletheus.runtime.lifecycle import (
    RuntimeLifecycleEventBus,
    RuntimeLifecycleState,
)

bus = RuntimeLifecycleEventBus()

for state in RuntimeLifecycleState:
    bus.publish(state.value)

print("========================================================")
print("ALETHEUSOS LIFECYCLE EVENTS")
print("========================================================")
print()

for event in bus.events:
    print(f"{event.timestamp}  {event.state}")

print()
print(f"Events........................{len(bus.events)}")
print("========================================================")
