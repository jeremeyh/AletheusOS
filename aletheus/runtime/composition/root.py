from aletheus.runtime.boot_pipeline import build_runtime_boot_pipeline


class RuntimeCompositionRoot:
    """
    Runtime Composition Root™

    Owns runtime startup handoff.
    """

    def boot(self, runtime):
        build_runtime_boot_pipeline().run(runtime)
        return runtime
