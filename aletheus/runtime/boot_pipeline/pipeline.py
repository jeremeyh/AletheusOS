class RuntimeBootPipeline:
    """
    Runtime Boot Pipeline™

    Executes boot phases in canonical order.
    """

    def __init__(self):
        self._phases = []

    def add(self, phase):
        self._phases.append(phase)
        return self

    def run(self, runtime):

        for phase in self._phases:
            phase.run(runtime)

        return runtime
