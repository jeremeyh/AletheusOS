from aletheus.runtime import runtime_core

print("event_bus_v3:", hasattr(runtime_core, "event_bus_v3"))

if hasattr(runtime_core, "event_bus_v3"):
    print("VERSION:", runtime_core.event_bus_v3.VERSION)
