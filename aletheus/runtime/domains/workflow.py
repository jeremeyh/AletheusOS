from __future__ import annotations


class WorkflowDomain:
    """
    Runtime Workflow capability domain.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, context):
        context.add_result(
            "workflow",
            self.runtime.workflow_v3.bootstrap(),
        )
        return context

    def create(self, context):
        payload = context.payload
        result = self.runtime.workflow_v3.create(
            title=payload.get("title", "Untitled Workflow"),
            description=payload.get("description", ""),
        )
        context.add_result("workflow", result)
        return context

    def start(self, context):
        result = self.runtime.workflow_v3.start(context.payload.get("workflow_id", ""))
        context.add_result("workflow", result)
        return context

    def pause(self, context):
        result = self.runtime.workflow_v3.pause(context.payload.get("workflow_id", ""))
        context.add_result("workflow", result)
        return context

    def resume(self, context):
        result = self.runtime.workflow_v3.resume(context.payload.get("workflow_id", ""))
        context.add_result("workflow", result)
        return context

    def cancel(self, context):
        result = self.runtime.workflow_v3.cancel(context.payload.get("workflow_id", ""))
        context.add_result("workflow", result)
        return context

    def status(self, context):
        context.add_result(
            "workflow_status",
            self.runtime.workflow_v3.status(),
        )
        return context

    def statistics(self, context):
        context.add_result(
            "workflow_stats",
            self.runtime.workflow_v3.statistics(),
        )
        return context
