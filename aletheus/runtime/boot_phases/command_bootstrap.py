from aletheus.runtime.command_bootstrap.bootstrapper import RuntimeCommandBootstrapper


class RuntimeCommandBootstrapPhase:
    """
    Runtime Command Bootstrap Phase™

    Registers runtime command domains through the RuntimeCommandBootstrapper.
    """

    def run(self, runtime):
        RuntimeCommandBootstrapper().bootstrap(runtime)

        return {
            "commands": runtime.commands.count(),
        }
