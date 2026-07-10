from __future__ import annotations


class AgentDomain:
    """
    Runtime Agent capability domain.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, context):
        context.add_result("agents", self.runtime.agents_v2.bootstrap())
        return context

    def spawn(self, context):
        payload = context.payload
        result = self.runtime.agents_v2.spawn(
            name=payload.get("name", "Unnamed Agent"),
            role=payload.get("role", "General"),
        )
        context.add_result("agent", result)
        return context

    def assign(self, context):
        payload = context.payload
        result = self.runtime.agents_v2.assign(
            agent_id=payload.get("agent_id", ""),
            mission=payload.get("mission", ""),
        )
        context.add_result("agent", result)
        return context

    def message(self, context):
        payload = context.payload
        result = self.runtime.agents_v2.message(
            sender=payload.get("sender", "Founder"),
            recipient=payload.get("recipient", ""),
            message=payload.get("message", ""),
        )
        context.add_result("message", result)
        return context

    def pause(self, context):
        result = self.runtime.agents_v2.pause(
            context.payload.get("agent_id", "")
        )
        context.add_result("agent", result)
        return context

    def resume(self, context):
        result = self.runtime.agents_v2.resume(
            context.payload.get("agent_id", "")
        )
        context.add_result("agent", result)
        return context

    def stop(self, context):
        result = self.runtime.agents_v2.stop(
            context.payload.get("agent_id", "")
        )
        context.add_result("agent", result)
        return context

    def heartbeat(self, context):
        context.add_result(
            "heartbeat",
            self.runtime.agents_v2.heartbeat(),
        )
        return context

    def statistics(self, context):
        context.add_result(
            "agent_stats",
            self.runtime.agents_v2.statistics(),
        )
        return context
