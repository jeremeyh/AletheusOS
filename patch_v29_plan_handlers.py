from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "def _cmd_plan_bootstrap" in text:
    print("Planning handlers already exist.")
    raise SystemExit(0)

methods = '''

    # ==========================================================
    # v2.9 Autonomous Planning Engine
    # ==========================================================

    def _cmd_plan_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("planning", self.planning_v2.bootstrap())
        return context

    def _cmd_plan_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.planning_v2.create(
            goal=payload.get("goal", "Untitled Goal"),
        )
        context.add_result("plan", result)
        return context

    def _cmd_plan_execute(self, context: RuntimeContext) -> RuntimeContext:
        result = self.planning_v2.execute(
            context.payload.get("plan_id", "")
        )
        context.add_result("plan", result)
        return context

    def _cmd_plan_progress(self, context: RuntimeContext) -> RuntimeContext:
        result = self.planning_v2.progress(
            context.payload.get("plan_id", "")
        )
        context.add_result("plan", result)
        return context

    def _cmd_plan_replan(self, context: RuntimeContext) -> RuntimeContext:
        result = self.planning_v2.replan(
            context.payload.get("plan_id", "")
        )
        context.add_result("plan", result)
        return context

    def _cmd_plan_complete(self, context: RuntimeContext) -> RuntimeContext:
        result = self.planning_v2.complete(
            context.payload.get("plan_id", "")
        )
        context.add_result("plan", result)
        return context

    def _cmd_plan_status(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "plans",
            self.planning_v2.status(),
        )
        return context

    def _cmd_plan_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "planning_stats",
            self.planning_v2.statistics(),
        )
        return context

'''

anchor = "    def _job_runtime_pulse(self) -> dict:"

if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, methods + anchor, 1)

core.write_text(text)

print("✔ v2.9 planning handlers added.")
