from aletheus.runtime import runtime_core

print("plugins_v3:", hasattr(runtime_core, "plugins_v3"))

if hasattr(runtime_core, "plugins_v3"):
    print("VERSION:", runtime_core.plugins_v3.VERSION)
