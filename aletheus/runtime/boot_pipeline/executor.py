from concurrent.futures import ThreadPoolExecutor


class RuntimeBootExecutor:
    """
    Runtime Boot Executor™

    Executes boot phases.
    Future versions will use dependency-aware scheduling.
    """

    def run_serial(self, runtime, phases):

        for phase in phases:
            phase.run(runtime)

    def run_parallel(self, runtime, phases):

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(phase.run, runtime)
                for phase in phases
            ]

            for future in futures:
                future.result()
