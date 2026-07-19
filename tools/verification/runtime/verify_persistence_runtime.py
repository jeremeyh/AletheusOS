from aletheus.runtime import runtime_core

print("persistence_v3:", hasattr(runtime_core, "persistence_v3"))

if hasattr(runtime_core, "persistence_v3"):
    print("VERSION:", runtime_core.persistence_v3.VERSION)
