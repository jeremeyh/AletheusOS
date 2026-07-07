from aletheus.runtime.boot_pipeline.conditions import BootConditions
from aletheus.runtime.policy import RuntimePolicyEngine


class DummyRuntime:
    pass


runtime = DummyRuntime()
runtime.policy = RuntimePolicyEngine()

runtime.policy.register(
    "boot.phase.RuntimeStateBootPhase",
    lambda runtime: True,
)

runtime.policy.register(
    "boot.phase.ExperimentalBootPhase",
    lambda runtime: False,
)

print("========================================================")
print("ALETHEUSOS POLICY-AWARE BOOT CONDITIONS")
print("========================================================")
print()

for phase in [
    "RuntimeStateBootPhase",
    "ExperimentalBootPhase",
    "UnregisteredBootPhase",
]:
    status = "RUN" if BootConditions.should_run(runtime, phase) else "SKIP"
    print(f"{phase:.<45}{status}")

print()
print("========================================================")
