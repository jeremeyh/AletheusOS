class RuntimePolicyEngine:
    """
    Runtime Policy Engine™

    Evaluates runtime orchestration policies.
    """

    def __init__(self):
        self._policies = {}

    def register(self, name, policy):
        self._policies[name] = policy

    def evaluate(self, runtime, policy_name):
        policy = self._policies.get(policy_name)

        if policy is None:
            return True

        return bool(policy(runtime))

    def policies(self):
        return tuple(sorted(self._policies.keys()))
