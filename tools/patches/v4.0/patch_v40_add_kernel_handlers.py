from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "def _cmd_kernel_bootstrap" in text:
    print("✔ Kernel handlers already installed.")
    raise SystemExit(0)

handlers = """

    # ==========================================================
    # v4.0 Intelligence Kernel
    # ==========================================================

    def _cmd_kernel_bootstrap(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "kernel",
            {
                "version": self.intelligence_orchestrator.version,
                "scheduler": self.intelligence_scheduler.statistics(),
                "dispatcher": self.intelligence_dispatcher.statistics(),
                "supervisor": self.intelligence_supervisor.statistics(),
                "health": "healthy",
            },
        )

        return context


    def _cmd_kernel_execute(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        result = self.intelligence_orchestrator.execute(
            command=payload.get("command"),
            payload=payload.get("payload", {}),
            runtime=self,
            priority=payload.get("priority", 5),
        )

        context.add_result(
            "task",
            result,
        )

        return context


    def _cmd_kernel_tasks(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "tasks",
            self.intelligence_orchestrator.list_tasks(),
        )

        return context


    def _cmd_kernel_scheduler(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        if payload.get("task_id"):

            context.add_result(
                "schedule",
                self.intelligence_scheduler.schedule(
                    payload["task_id"],
                    payload.get("priority", 5),
                ),
            )

        else:

            context.add_result(
                "schedule",
                self.intelligence_scheduler.statistics(),
            )

        return context


    def _cmd_kernel_dispatcher(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        if payload.get("command"):

            dispatched = self.intelligence_dispatcher.dispatch(
                runtime=self,
                command=payload["command"],
                payload=payload.get("payload", {}),
            )

            context.add_result(
                "dispatch",
                {
                    "results": dispatched.results,
                    "errors": dispatched.errors,
                },
            )

        else:

            context.add_result(
                "dispatch",
                self.intelligence_dispatcher.statistics(),
            )

        return context


    def _cmd_kernel_supervisor(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "supervisor",
            self.intelligence_supervisor.check(self),
        )

        return context


    def _cmd_kernel_statistics(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "kernel_stats",
            {
                "orchestrator": self.intelligence_orchestrator.statistics(),
                "scheduler": self.intelligence_scheduler.statistics(),
                "dispatcher": self.intelligence_dispatcher.statistics(),
                "supervisor": self.intelligence_supervisor.statistics(),
            },
        )

        return context

"""

anchor = "    def _job_runtime_pulse(self) -> dict:"

if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, handlers + anchor, 1)

core.write_text(text)

print("✔ v4.0 Intelligence Kernel handlers added.")
