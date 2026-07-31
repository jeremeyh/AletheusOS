from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

if "from aletheus.missions_v2 import mission_v2_core" not in text:
    text = text.replace(
        "from aletheus.kernel_v2 import kernel_core\n",
        "from aletheus.kernel_v2 import kernel_core\nfrom aletheus.missions_v2 import mission_v2_core\n",
    )

text = text.replace('self.version = "2.0.0-beta"', 'self.version = "2.0.0-c"')

if "self.mission_v2 = mission_v2_core" not in text:
    text = text.replace(
        "self.kernel_v2 = kernel_core\n\n        self.boot()",
        "self.kernel_v2 = kernel_core\n        self.mission_v2 = mission_v2_core\n\n        self.boot()",
    )

if 'self.commands.register("mission.v2.create"' not in text:
    anchor = '        self.commands.register("kernel.stats", self._cmd_kernel_stats)\n'
    insert = """        self.commands.register("mission.v2.create", self._cmd_mission_v2_create)
        self.commands.register("mission.v2.plan", self._cmd_mission_v2_plan)
        self.commands.register("mission.v2.execute_next", self._cmd_mission_v2_execute_next)
        self.commands.register("mission.v2.execute", self._cmd_mission_v2_execute)
        self.commands.register("mission.v2.pause", self._cmd_mission_v2_pause)
        self.commands.register("mission.v2.resume", self._cmd_mission_v2_resume)
        self.commands.register("mission.v2.cancel", self._cmd_mission_v2_cancel)
        self.commands.register("mission.v2.list", self._cmd_mission_v2_list)
        self.commands.register("mission.v2.telemetry", self._cmd_mission_v2_telemetry)
        self.commands.register("mission.v2.stats", self._cmd_mission_v2_stats)
"""
    if anchor not in text:
        raise SystemExit("Could not find kernel.stats command anchor.")
    text = text.replace(anchor, anchor + insert)

if '"Aletheus v2 Autonomous Mission Engine"' not in text:
    anchor = """        self.services.register(
            "Aletheus v2 Autonomous Kernel",
            {"status": "online", "version": self.kernel_v2.version},
        )

        self.scheduler.register(
"""
    replacement = """        self.services.register(
            "Aletheus v2 Autonomous Kernel",
            {"status": "online", "version": self.kernel_v2.version},
        )
        self.services.register(
            "Aletheus v2 Autonomous Mission Engine",
            {"status": "online", "version": self.mission_v2.version},
        )

        self.scheduler.register(
"""
    if anchor not in text:
        raise SystemExit("Could not find kernel service registration anchor.")
    text = text.replace(anchor, replacement)

if '"v2_missions": self.mission_v2.stats()["missions"]' not in text:
    text = text.replace(
        """                "kernel_events": self.kernel_v2.stats()["events"],
                "kernel_registry_items": self.kernel_v2.stats()["registry_items"],
            },
        )
        return context
""",
        """                "kernel_events": self.kernel_v2.stats()["events"],
                "kernel_registry_items": self.kernel_v2.stats()["registry_items"],
                "v2_missions": self.mission_v2.stats()["missions"],
                "v2_mission_events": self.mission_v2.stats()["telemetry_events"],
            },
        )
        return context
""",
    )

if 'context.add_result("mission_v2", self.mission_v2.stats())' not in text:
    text = text.replace(
        """        context.add_result("kernel_v2", self.kernel_v2.stats())
        return context
""",
        """        context.add_result("kernel_v2", self.kernel_v2.stats())
        context.add_result("mission_v2", self.mission_v2.stats())
        return context
""",
    )

if "def _cmd_mission_v2_create" not in text:
    anchor = "    def _job_runtime_pulse(self) -> dict:\n"
    methods = """
    def _cmd_mission_v2_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        mission = self.mission_v2.create_mission(
            title=payload.get("title", "Untitled Mission"),
            objective=payload.get("objective", ""),
            application=payload.get("application", "AletheusOS"),
            priority=payload.get("priority", "high"),
            tasks=payload.get("tasks"),
        )
        self.kernel_v2.publish(
            event_type="mission.v2.created",
            source="mission_v2",
            payload=mission.to_dict(),
        )
        context.add_result("mission", mission.to_dict())
        return context

    def _cmd_mission_v2_plan(self, context: RuntimeContext) -> RuntimeContext:
        result = self.mission_v2.plan_mission(
            mission_id=context.payload.get("mission_id", ""),
            runtime=self,
        )
        self.kernel_v2.publish(
            event_type="mission.v2.planned",
            source="mission_v2",
            payload=result,
        )
        context.add_result("planning", result)
        return context

    def _cmd_mission_v2_execute_next(self, context: RuntimeContext) -> RuntimeContext:
        result = self.mission_v2.execute_next(
            mission_id=context.payload.get("mission_id", ""),
            runtime=self,
        )
        self.kernel_v2.publish(
            event_type="mission.v2.step_executed",
            source="mission_v2",
            payload=result,
        )
        context.add_result("execution", result)
        return context

    def _cmd_mission_v2_execute(self, context: RuntimeContext) -> RuntimeContext:
        result = self.mission_v2.execute_mission(
            mission_id=context.payload.get("mission_id", ""),
            runtime=self,
        )
        self.kernel_v2.publish(
            event_type="mission.v2.executed",
            source="mission_v2",
            payload=result,
        )
        context.add_result("execution", result)
        return context

    def _cmd_mission_v2_pause(self, context: RuntimeContext) -> RuntimeContext:
        result = self.mission_v2.pause_mission(context.payload.get("mission_id", ""))
        context.add_result("mission", result)
        return context

    def _cmd_mission_v2_resume(self, context: RuntimeContext) -> RuntimeContext:
        result = self.mission_v2.resume_mission(context.payload.get("mission_id", ""))
        context.add_result("mission", result)
        return context

    def _cmd_mission_v2_cancel(self, context: RuntimeContext) -> RuntimeContext:
        result = self.mission_v2.cancel_mission(context.payload.get("mission_id", ""))
        context.add_result("mission", result)
        return context

    def _cmd_mission_v2_list(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("missions", self.mission_v2.list_missions(context.payload.get("status")))
        return context

    def _cmd_mission_v2_telemetry(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "telemetry",
            self.mission_v2.mission_telemetry(context.payload.get("mission_id", "")),
        )
        return context

    def _cmd_mission_v2_stats(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("mission_v2_stats", self.mission_v2.stats())
        return context

"""
    if anchor not in text:
        raise SystemExit("Could not find _job_runtime_pulse anchor.")
    text = text.replace(anchor, methods + anchor)

p.write_text(text)
print("v2.0C runtime mission engine patch applied.")
