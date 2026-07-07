from aletheus.runtime.lifecycle import RuntimeLifecycleManager
from aletheus.runtime.providers import RuntimeServiceProvider
from aletheus.runtime.health import RuntimeHealthMonitor
from aletheus.runtime.recovery import RuntimeRecoveryManager
from aletheus.runtime.capabilities import RuntimeCapabilityRegistry
from aletheus.runtime.policy import RuntimePolicyEngine
from aletheus.runtime.orchestration import RuntimeOrchestrator

policy = RuntimePolicyEngine()

policy.register(
    "runtime.boot",
    lambda runtime: True,
)

policy.register(
    "runtime.health",
    lambda runtime: True,
)

policy.register(
    "runtime.recover",
    lambda runtime: True,
)

orchestrator = RuntimeOrchestrator(
    lifecycle=RuntimeLifecycleManager(),
    service_provider=RuntimeServiceProvider(),
    health_monitor=RuntimeHealthMonitor(),
    recovery_manager=RuntimeRecoveryManager(),
    capability_registry=RuntimeCapabilityRegistry(),
    policy_engine=policy,
)

print("========================================================")
print("ALETHEUSOS POLICY-AWARE ORCHESTRATOR")
print("========================================================")
print()

print("Policies")

for p in policy.policies():
    print(" -", p)

print()
print("========================================================")
