from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

if "def _cmd_agent_spawn" in text:
    print("Agent handlers already exist.")
    raise SystemExit(0)

methods = '''
    def _cmd_agent_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("agents", self.agents_v2.bootstrap())
        return context

    def _cmd_agent_spawn(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.agents_v2.spawn(
            name=payload.get("name", "Unnamed Agent"),
            role=payload.get("role", "General"),
        )
        context.add_result("agent", result)
        return context

    def _cmd_agent_assign(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.agents_v2.assign(
            agent_id=payload.get("agent_id", ""),
            mission=payload.get("mission", ""),
        )
        context.add_result("agent", result)
        return context

    def _cmd_agent_message(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.agents_v2.message(
            sender=payload.get("sender", "Founder"),
            recipient=payload.get("recipient", ""),
            message=payload.get("message", ""),
        )
        context.add_result("message", result)
        return context

    def _cmd_agent_pause(self, context: RuntimeContext) -> RuntimeContext:
        result = self.agents_v2.pause(context.payload.get("agent_id", ""))
        context.add_result("agent", result)
        return context

    def _cmd_agent_resume(self, context: RuntimeContext) -> RuntimeContext:
        result = self.agents_v2.resume(context.payload.get("agent_id", ""))
        context.add_result("agent", result)
        return context

    def _cmd_agent_stop(self, context: RuntimeContext) -> RuntimeContext:
        result = self.agents_v2.stop(context.payload.get("agent_id", ""))
        context.add_result("agent", result)
        return context

    def _cmd_agent_heartbeat(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("heartbeat", self.agents_v2.heartbeat())
        return context

    def _cmd_agent_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("agent_stats", self.agents_v2.statistics())
        return context

'''

anchor = "    def _job_runtime_pulse(self) -> dict:"
if anchor not in text:
    raise SystemExit("Could not find _job_runtime_pulse anchor.")

text = text.replace(anchor, methods + anchor, 1)
path.write_text(text)

print("✔ Missing v2.7 agent handlers added.")
