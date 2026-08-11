from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "def _cmd_security_bootstrap" in text:
    print("Security handlers already exist.")
    raise SystemExit(0)

handlers = """

    # ==========================================================
    # v3.7 Security & Policy Engine
    # ==========================================================

    def _cmd_security_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "security",
            self.security_v3.bootstrap(),
        )
        return context

    def _cmd_security_authenticate(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload

        context.add_result(
            "authentication",
            self.security_v3.authenticate(
                payload.get("identity", "anonymous"),
            ),
        )
        return context

    def _cmd_security_authorize(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload

        context.add_result(
            "authorization",
            self.security_v3.authorize(
                payload.get("identity", "anonymous"),
                payload.get("permission", ""),
            ),
        )
        return context

    def _cmd_security_policy(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload

        context.add_result(
            "policy",
            self.security_v3.policy(
                payload.get("name", "default"),
                payload.get("definition", {}),
            ),
        )
        return context

    def _cmd_security_role_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload

        context.add_result(
            "role",
            self.security_v3.create_role(
                payload.get("name", "Operator"),
                payload.get("permissions", []),
            ),
        )
        return context

    def _cmd_security_role_assign(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload

        context.add_result(
            "assignment",
            self.security_v3.assign_role(
                payload.get("identity", "anonymous"),
                payload.get("role", "Operator"),
            ),
        )
        return context

    def _cmd_security_audit(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload

        context.add_result(
            "audit",
            self.security_v3.audit(
                action=payload.get("action", "runtime"),
                actor=payload.get("actor", "system"),
                status=payload.get("status", "success"),
                metadata=payload.get("metadata", {}),
            ),
        )
        return context

    def _cmd_security_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "security_stats",
            self.security_v3.statistics(),
        )
        return context

"""

anchor = "    def _job_runtime_pulse(self) -> dict:"

if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, handlers + anchor, 1)

core.write_text(text)

print("✔ v3.7 Security handlers added.")
