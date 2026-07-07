from aletheus.runtime.policy import RuntimePolicyEngine

engine = RuntimePolicyEngine()

engine.register(
    "runtime.online",
    lambda runtime: True,
)

engine.register(
    "plugins.enabled",
    lambda runtime: False,
)

print("========================================================")
print("ALETHEUSOS POLICY ENGINE")
print("========================================================")
print()

for policy in engine.policies():
    print(policy)

print()
print("========================================================")
