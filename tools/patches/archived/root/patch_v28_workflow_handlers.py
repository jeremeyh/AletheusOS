from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

if "def _cmd_workflow_bootstrap" in text:
    print("Workflow handlers already exist.")
    raise SystemExit(0)

methods = '''
    def _cmd_workflow_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("workflow", self.workflow_v3.bootstrap())
        return context

    def _cmd_workflow_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.workflow_v3.create(
            title=payload.get("title", "Untitled Workflow"),
            description=payload.get("description", ""),
        )
        context.add_result("workflow", result)
        return context

    def _cmd_workflow_start(self, context: RuntimeContext) -> RuntimeContext:
        result = self.workflow_v3.start(
            context.payload.get("workflow_id", "")
        )
        context.add_result("workflow", result)
        return context

    def _cmd_workflow_pause(self, context: RuntimeContext) -> RuntimeContext:
        result = self.workflow_v3.pause(
            context.payload.get("workflow_id", "")
        )
        context.add_result("workflow", result)
        return context

    def _cmd_workflow_resume(self, context: RuntimeContext) -> RuntimeContext:
        result = self.workflow_v3.resume(
            context.payload.get("workflow_id", "")
        )
        context.add_result("workflow", result)
        return context

    def _cmd_workflow_cancel(self, context: RuntimeContext) -> RuntimeContext:
        result = self.workflow_v3.cancel(
            context.payload.get("workflow_id", "")
        )
        context.add_result("workflow", result)
        return context

    def _cmd_workflow_status(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("workflow_status", self.workflow_v3.status())
        return context

    def _cmd_workflow_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("workflow_stats", self.workflow_v3.statistics())
        return context

'''

anchor = "    def _job_runtime_pulse(self) -> dict:"

if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, methods + anchor, 1)

path.write_text(text)

print("✔ v2.8 workflow command handlers added.")
