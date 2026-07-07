class RuntimeSchedulerBootPhase:
    """
    Runtime Scheduler Boot Phase™

    Registers recurring runtime jobs with the scheduler.
    """

    def run(self, runtime):

        runtime.scheduler.register(
            "Runtime Pulse",
            "Runtime diagnostic pulse.",
            runtime._job_runtime_pulse,
        )

        return {
            "jobs": 1,
            "registered": [
                "Runtime Pulse",
            ],
        }
