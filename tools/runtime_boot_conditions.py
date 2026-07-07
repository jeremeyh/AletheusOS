from aletheus.runtime.boot_pipeline.conditions import BootConditions
from aletheus.runtime.boot_pipeline.manifest import BOOT_PHASES


class DummyRuntime:
    pass


runtime = DummyRuntime()

print("========================================================")
print("ALETHEUSOS BOOT CONDITIONS")
print("========================================================")
print()

for phase in BOOT_PHASES:

    enabled = BootConditions.should_run(runtime, phase)

    status = "ENABLED" if enabled else "SKIPPED"

    print(f"{phase:.<45}{status}")

print()
print("========================================================")
