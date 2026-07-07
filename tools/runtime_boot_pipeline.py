from aletheus.runtime.boot_pipeline import (
    RuntimeBootPipeline,
    RuntimeBootPipelineReporter,
)


def simple_handler(stage):
    return {
        "stage": stage.name,
        "provided": stage.provides,
        "status": "ok",
    }


def main():
    pipeline = RuntimeBootPipeline()

    pipeline.register_stage(
        name="foundation",
        order=0,
        handler=simple_handler,
        provides=["runtime_foundation"],
    )

    pipeline.register_stage(
        name="executive_kernel",
        order=1,
        handler=simple_handler,
        dependencies=["foundation"],
        provides=["coordination"],
    )

    pipeline.register_stage(
        name="registries",
        order=2,
        handler=simple_handler,
        dependencies=["executive_kernel"],
        provides=["runtime_registry"],
    )

    pipeline.register_stage(
        name="runtime_anchor_circuits",
        order=3,
        handler=simple_handler,
        dependencies=["registries"],
        provides=["attachment_layer"],
    )

    pipeline.register_stage(
        name="service_mesh",
        order=4,
        handler=simple_handler,
        dependencies=["runtime_anchor_circuits"],
        provides=["runtime_topology"],
    )

    pipeline.register_stage(
        name="relay_network",
        order=5,
        handler=simple_handler,
        dependencies=["service_mesh"],
        provides=["packet_delivery"],
    )

    pipeline.register_stage(
        name="catalyst",
        order=6,
        handler=simple_handler,
        dependencies=["service_mesh"],
        provides=["runtime_optimization"],
    )

    pipeline.register_stage(
        name="platform_services",
        order=7,
        handler=simple_handler,
        dependencies=["relay_network", "catalyst"],
        provides=["memory", "governance", "platform_intelligence"],
    )

    pipeline.register_stage(
        name="applications",
        order=8,
        handler=simple_handler,
        dependencies=["platform_services"],
        provides=["application_runtime"],
    )

    report = pipeline.execute()
    print(RuntimeBootPipelineReporter().render(report))


if __name__ == "__main__":
    main()
