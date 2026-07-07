from aletheus.runtime.boot_pipeline.executor import RuntimeBootExecutor
from aletheus.runtime.boot_pipeline.default_pipeline import (
    build_runtime_boot_pipeline,
)


class DummyRuntime:
    pass


runtime = DummyRuntime()

pipeline = build_runtime_boot_pipeline()

executor = RuntimeBootExecutor()

print("========================================================")
print("ALETHEUSOS PARALLEL BOOT")
print("========================================================")
print()

executor.run_serial(runtime, pipeline._phases)

print("Runtime boot simulation complete.")

print()
print("========================================================")
