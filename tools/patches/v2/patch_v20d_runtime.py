from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

if "from aletheus.workflows_v2 import workflow_v2_core" not in text:
    text = text.replace(
        "from aletheus.missions_v2 import mission_v2_core\n",
        "from aletheus.missions_v2 import mission_v2_core\nfrom aletheus.workflows_v2 import workflow_v2_core\n",
    )

text = text.replace('self.version = "2.0.0-c"', 'self.version = "2.0.0-d"')

if "self.workflow_v2 = workflow_v2_core" not in text:
    text = text.replace(
        "self.mission_v2 = mission_v2_core\n\n        self.boot()",
        "self.mission_v2 = mission_v2_core\n        self.workflow_v2 = workflow_v2_core\n\n        self.boot()",
    )

if 'self.commands.register("workflow.v2.create"' not in text:
    anchor = '        self.commands.register("mission.v2.stats", self._cmd_mission_v2_stats)\n'
    insert = """        self.commands.register("workflow.v2.create", self._cmd_workflow_v2_create)
        self.commands.register("workflow.v2.execute_next", self._cmd_workflow_v2_execute_next)
        self.commands.register("workflow.v2.execute", self._cmd_workflow_v2_execute)
        self.commands.register("workflow.v2.pause", self._cmd_workflow_v2_pause)
        self.commands.register("workflow.v2.resume", self._cmd_workflow_v2_resume)
        self.commands.register("workflow.v2.cancel", self._cmd_workflow_v2_cancel)
        self.commands.register("workflow.v2.list", self._cmd_workflow_v2_list)
        self.commands.register("workflow.v2.history", self._cmd_workflow_v2_history)
        self.commands.register("workflow.v2.stats", self._cmd_workflow_v2_stats)
"""
    if anchor not in text:
        raise SystemExit("Could not find mission.v2.stats command anchor.")
    text = text.replace(anchor, anchor + insert)

if '"Aletheus v2 Autonomous Workflow Fabric"' not in text:
    anchor = """        self.services.register(
            "Aletheus v2 Autonomous Mission Engine",
            {"status": "online", "version": self.mission_v2.version},
        )

        self.scheduler.register(
"""
    replacement = """        self.services.register(
            "Aletheus v2 Autonomous Mission Engine",
            {"status": "online", "version": self.mission_v2.version},
        )
        self.services.register(
            "Aletheus v2 Autonomous Workflow Fabric",
            {"status": "online", "version": self.workflow_v2.version},
        )

        self.scheduler.register(
"""
    if anchor not in text:
        raise SystemExit("Could not find mission service registration anchor.")
    text = text.replace(anchor, replacement)

if '"v2_workflows": self.workflow_v2.stats()["workflows"]' not in text:
    text = text.replace(
        """                "v2_missions": self.mission_v2.stats()["missions"],
                "v2_mission_events": self.mission_v2.stats()["telemetry_events"],
            },
        )
        return context
""",
        """                "v2_missions": self.mission_v2.stats()["missions"],
                "v2_mission_events": self.mission_v2.stats()["telemetry_events"],
                "v2_workflows": self.workflow_v2.stats()["workflows"],
                "v2_workflow_events": self.workflow_v2.stats()["events"],
            },
        )
        return context
""",
    )

if 'context.add_result("workflow_v2", self.workflow_v2.stats())' not in text:
    text = text.replace(
        """        context.add_result("mission_v2", self.mission_v2.stats())
        return context
""",
        """        context.add_result("mission_v2", self.mission_v2.stats())
        context.add_result("workflow_v2", self.workflow_v2.stats())
        return context
""",
    )

if "def _cmd_workflow_v2_create" not in text:
    anchor = "    def _job_runtime_pulse(self) -> dict:\n"
    methods = """
    def _cmd_workflow_v2_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        workflow = self.workflow_v2.create_workflow(
            title=payload.get("title", "Untitled Workflow"),
            objective=payload.get("objective", ""),
            application=payload.get("application", "AletheusOS"),
            nodes=payload.get("nodes"),
        )
        self.kernel_v2.publish(
            event_type="workflow.v2.created",
            source="workflow_fabric",
            payload=workflow.to_dict(),
        )
        context.add_result("workflow", workflow.to_dict())
        return context

    def _cmd_workflow_v2_execute_next(self, context: RuntimeContext) -> RuntimeContext:
        result = self.workflow_v2.execute_next(
            workflow_id=context.payload.get("workflow_id", ""),
            runtime=self,
        )
        self.kernel_v2.publish(
            event_type="workflow.v2.node_executed",
            source="workflow_fabric",
            payload=result,
        )
        context.add_result("execution", result)
        return context

    def _cmd_workflow_v2_execute(self, context: RuntimeContext) -> RuntimeContext:
        result = self.workflow_v2.execute_workflow(
            workflow_id=context.payload.get("workflow_id", ""),
            runtime=self,
        )
        self.kernel_v2.publish(
            event_type="workflow.v2.executed",
            source="workflow_fabric",
            payload=result,
        )
        context.add_result("execution", result)
        return context

    def _cmd_workflow_v2_pause(self, context: RuntimeContext) -> RuntimeContext:
        result = self.workflow_v2.pause(context.payload.get("workflow_id", ""))
        context.add_result("workflow", result)
        return context

    def _cmd_workflow_v2_resume(self, context: RuntimeContext) -> RuntimeContext:
        result = self.workflow_v2.resume(context.payload.get("workflow_id", ""))
        context.add_result("workflow", result)
        return context

    def _cmd_workflow_v2_cancel(self, context: RuntimeContext) -> RuntimeContext:
        result = self.workflow_v2.cancel(context.payload.get("workflow_id", ""))
        context.add_result("workflow", result)
        return context

    def _cmd_workflow_v2_list(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("workflows", self.workflow_v2.list_workflows(context.payload.get("status")))
        return context

    def _cmd_workflow_v2_history(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "history",
            self.workflow_v2.history(context.payload.get("workflow_id", "")),
        )
        return context

    def _cmd_workflow_v2_stats(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("workflow_v2_stats", self.workflow_v2.stats())
        return context

"""
    if anchor not in text:
        raise SystemExit("Could not find _job_runtime_pulse anchor.")
    text = text.replace(anchor, methods + anchor)

p.write_text(text)
print("v2.0D runtime workflow fabric patch applied.")
