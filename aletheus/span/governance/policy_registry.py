from .policy import Policy


class PolicyRegistry:
    def __init__(self):
        self._policies=[]

    def register(self, policy:Policy):
        self._policies.append(policy)

    def policies(self):
        return tuple(self._policies)

    @classmethod
    def default(cls):
        r=cls()
        r.register(Policy("Maximum Fan-Out","coupling",25,recommendation="Reduce outgoing dependencies."))
        r.register(Policy("Maximum Fan-In","coupling",40,recommendation="Review ownership and API boundaries."))
        return r
