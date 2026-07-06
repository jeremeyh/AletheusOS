from __future__ import annotations

from aletheus.platform_registry import platform_registry

from .models import BootReport, BootResult


class BootExecutor:

    GENESIS = "13.9"
    VERSION = "0.1.0"

    def execute(self, plan):

        report = BootReport()

        for candidate in plan.ordered():

            instance = platform_registry.get_instance(
                candidate.component_id
            )

            if instance is None:

                report.results.append(
                    BootResult(
                        component_id=candidate.component_id,
                        name=candidate.name,
                        success=False,
                        message="Component not registered",
                    )
                )

                continue

            try:

                if hasattr(instance, "boot"):
                    instance.boot()

                report.results.append(
                    BootResult(
                        component_id=candidate.component_id,
                        name=candidate.name,
                        success=True,
                        message="Boot successful",
                    )
                )

            except Exception as exc:

                report.results.append(
                    BootResult(
                        component_id=candidate.component_id,
                        name=candidate.name,
                        success=False,
                        message=str(exc),
                    )
                )

        return report
