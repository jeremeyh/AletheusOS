from .conditions import BootConditions
from .context import RuntimeBootContext
from .timing import BootTiming


class RuntimeBootPipeline:
    """
    Runtime Boot Pipeline™

    Executes boot phases with conditions, timing, and reporting.
    """

    def __init__(self):
        self._phases = []

    def add(self, phase):
        self._phases.append(phase)
        return self

    def run(self, runtime):
        context = RuntimeBootContext()

        for phase in self._phases:
            phase_name = phase.__class__.__name__

            if not BootConditions.should_run(runtime, phase_name):
                context.skipped.append(phase_name)
                continue

            timer = BootTiming(phase_name)

            phase.run(runtime)

            timer.stop()

            context.timings[phase_name] = timer.milliseconds
            context.executed.append(phase_name)
            context.report.record(phase_name)

        context.report.finish()

        runtime.boot_report = context.report
        runtime.boot_context = context

        return runtime
