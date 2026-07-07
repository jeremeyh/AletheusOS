from .models import BootPipelineReport, BootStage, BootStageResult


class RuntimeBootPipeline:
    """
    Runtime Boot Pipeline™

    Executes the ordered boot stages that bring AletheusOS online.

    The pipeline sequences startup.
    It does not own implementation of runtime services.
    """

    def __init__(self):
        self.stages: list[BootStage] = []
        self.handlers: dict[str, object] = {}

    def register_stage(
        self,
        name: str,
        order: int,
        handler=None,
        critical: bool = True,
        dependencies: list[str] | None = None,
        provides: list[str] | None = None,
        metadata: dict | None = None,
    ):
        stage = BootStage(
            name=name,
            order=order,
            critical=critical,
            dependencies=dependencies or [],
            provides=provides or [],
            metadata=metadata or {},
        )

        self.stages.append(stage)

        if handler is not None:
            self.handlers[name] = handler

        self.stages.sort(key=lambda item: item.order)
        return stage

    def execute(self) -> BootPipelineReport:
        completed = set()
        results = []

        for stage in self.stages:
            missing = [
                dependency
                for dependency in stage.dependencies
                if dependency not in completed
            ]

            if missing:
                stage.status = "blocked"

                result = BootStageResult(
                    name=stage.name,
                    order=stage.order,
                    status="blocked",
                    message="Missing boot dependencies.",
                    metadata={"missing_dependencies": missing},
                )

                results.append(result)

                if stage.critical:
                    return BootPipelineReport(
                        status="failed",
                        stages=results,
                    )

                continue

            handler = self.handlers.get(stage.name)

            try:
                if handler is not None:
                    response = handler(stage)
                else:
                    response = {
                        "message": f"Stage '{stage.name}' completed without handler."
                    }

                stage.status = "completed"
                completed.add(stage.name)

                result = BootStageResult(
                    name=stage.name,
                    order=stage.order,
                    status="completed",
                    message=f"Stage '{stage.name}' completed.",
                    metadata=response if isinstance(response, dict) else {"result": response},
                )

            except Exception as exc:
                stage.status = "failed"

                result = BootStageResult(
                    name=stage.name,
                    order=stage.order,
                    status="failed",
                    message=str(exc),
                )

                results.append(result)

                if stage.critical:
                    return BootPipelineReport(
                        status="failed",
                        stages=results,
                    )

                continue

            results.append(result)

        final_status = (
            "ready"
            if all(result.status == "completed" for result in results)
            else "completed_with_warnings"
        )

        return BootPipelineReport(
            status=final_status,
            stages=results,
        )

    def health(self):
        return {
            "status": "online",
            "registered_stages": len(self.stages),
            "stage_names": [stage.name for stage in self.stages],
        }
