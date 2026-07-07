from aletheus.runtime.boot_phases import (
    RuntimeAgentBootPhase,
    RuntimeApplicationBootPhase,
    RuntimeCommandBootstrapPhase,
    RuntimeMemoryInitializationPhase,
    RuntimeSchedulerBootPhase,
    RuntimeServiceRegistrationPhase,
    RuntimeStateBootPhase,
)

from .pipeline import RuntimeBootPipeline


def build_runtime_boot_pipeline():

    return (
        RuntimeBootPipeline()
        .add(RuntimeStateBootPhase())
        .add(RuntimeCommandBootstrapPhase())
        .add(RuntimeServiceRegistrationPhase())
        .add(RuntimeSchedulerBootPhase())
        .add(RuntimeApplicationBootPhase())
        .add(RuntimeAgentBootPhase())
        .add(RuntimeMemoryInitializationPhase())
    )
