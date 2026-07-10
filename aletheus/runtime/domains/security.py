class SecurityDomain:
    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, payload=None):
        return self.runtime.security_v3.bootstrap()

    def authenticate(self, payload):
        return self.runtime.security_v3.authenticate(
            payload.get("identity", "anonymous")
        )

    def authorize(self, payload):
        return self.runtime.security_v3.authorize(
            payload.get("identity", "anonymous"),
            payload.get("permission", ""),
        )

    def policy(self, payload):
        return self.runtime.security_v3.policy(
            payload.get("name", "default"),
            payload.get("definition", {}),
        )

    def role_create(self, payload):
        return self.runtime.security_v3.create_role(
            payload.get("name", "Operator"),
            payload.get("permissions", []),
        )

    def role_assign(self, payload):
        return self.runtime.security_v3.assign_role(
            payload.get("identity", "anonymous"),
            payload.get("role", "Operator"),
        )

    def audit(self, payload):
        return self.runtime.security_v3.audit(
            action=payload.get("action", "runtime"),
            actor=payload.get("actor", "system"),
            status=payload.get("status", "success"),
            metadata=payload.get("metadata", {}),
        )

    def statistics(self, payload=None):
        return self.runtime.security_v3.statistics()
