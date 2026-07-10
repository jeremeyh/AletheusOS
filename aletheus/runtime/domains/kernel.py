class KernelDomain:
    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, payload=None):
        return {
            "version": self.runtime.intelligence_orchestrator.version,
            "scheduler": self.runtime.intelligence_scheduler.statistics(),
            "dispatcher": self.runtime.intelligence_dispatcher.statistics(),
            "supervisor": self.runtime.intelligence_supervisor.statistics(),
            "health": "healthy",
        }

    def execute(self, payload):
        return self.runtime.intelligence_orchestrator.execute(
            command=payload.get("command"),
            payload=payload.get("payload", {}),
            runtime=self.runtime,
            priority=payload.get("priority", 5),
        )

    def tasks(self, payload=None):
        return self.runtime.intelligence_orchestrator.list_tasks()

    def scheduler(self, payload):
        if payload.get("task_id"):
            return self.runtime.intelligence_scheduler.schedule(
                payload["task_id"],
                payload.get("priority", 5),
            )

        return self.runtime.intelligence_scheduler.statistics()

    def dispatcher(self, payload):
        if payload.get("command"):
            dispatched = self.runtime.intelligence_dispatcher.dispatch(
                runtime=self.runtime,
                command=payload["command"],
                payload=payload.get("payload", {}),
            )

            return {
                "results": dispatched.results,
                "errors": dispatched.errors,
            }

        return self.runtime.intelligence_dispatcher.statistics()

    def supervisor(self, payload=None):
        return self.runtime.intelligence_supervisor.check(self.runtime)

    def statistics(self, payload=None):
        return {
            "orchestrator": self.runtime.intelligence_orchestrator.statistics(),
            "scheduler": self.runtime.intelligence_scheduler.statistics(),
            "dispatcher": self.runtime.intelligence_dispatcher.statistics(),
            "supervisor": self.runtime.intelligence_supervisor.statistics(),
        }
