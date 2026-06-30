from aletheus.runtime import runtime_core

print("telemetry_v3:", hasattr(runtime_core, "telemetry_v3"))

if hasattr(runtime_core, "telemetry_v3"):
    print("VERSION:", runtime_core.telemetry_v3.VERSION)

ctx = runtime_core.commands.dispatch("runtime.diagnostics")

print("\nSERVICES")
for s in ctx.results["diagnostics"]["services"]:
    print("-", s)

expected = [
    "telemetry.bootstrap",
    "telemetry.record",
    "telemetry.metric",
    "telemetry.log",
    "telemetry.trace",
    "telemetry.health",
    "telemetry.timeline",
    "telemetry.statistics",
]

missing = [c for c in expected if c not in runtime_core.commands.list()]

print("\nMissing commands:", missing)
