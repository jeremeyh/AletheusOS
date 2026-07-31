from __future__ import annotations

from aletheus.application_runtime import application_runtime
from aletheus.contracts import PlatformComponentContract
from aletheus.platform_registry import platform_registry
from aletheus.service_manager import service_manager

from .models import BootCandidate, BootPlan


class SelfAssembly:
    """
    Genesis 14.1

    Runtime Self-Assembly™

    Responsibilities

    • Discover platform components
    • Verify platform contracts
    • Register components
    • Produce assembly reports
    • Produce deterministic boot plans

    Future Genesis releases will add:

    • Automatic discovery
    • Dependency resolution
    • Dynamic boot planning
    """

    GENESIS = "14.1"
    VERSION = "0.3.0"

    def __init__(self):
        self._components = []

    # ============================================================
    # Discovery
    # ============================================================

    def discover(self):

        #
        # Canonical deterministic platform inventory.
        #
        # Additional platform components are added here
        # as they become PlatformComponentContract compliant.
        #

        self._components = [
            (
                "aletheus.service_manager",
                "Service Manager",
                service_manager,
            ),
            (
                "aletheus.application_runtime",
                "Application Runtime",
                application_runtime,
            ),
            #
            # Future platform components
            #
            # (
            #     "aletheus.runtime_supervisor",
            #     "Runtime Supervisor",
            #     runtime_supervisor,
            # ),
            #
            # (
            #     "aletheus.platform_governor",
            #     "Platform Governor",
            #     platform_governor,
            # ),
            #
            # (
            #     "aletheus.platform_api",
            #     "Platform API",
            #     platform_api,
            # ),
            #
            # (
            #     "aletheus.integration",
            #     "Integration",
            #     integration_runtime,
            # ),
            #
            # (
            #     "aletheus.orchestrator",
            #     "Orchestrator",
            #     orchestrator,
            # ),
        ]

        return self._components

    # ============================================================
    # Verification
    # ============================================================

    def verify(self):

        self.discover()

        results = []

        for component_id, _, instance in self._components:
            results.append(
                {
                    "component": component_id,
                    "verified": isinstance(
                        instance,
                        PlatformComponentContract,
                    ),
                }
            )

        return results

    # ============================================================
    # Assembly
    # ============================================================

    def assemble(self):

        discovered = self.discover()

        registered = 0

        for component_id, name, instance in discovered:
            if not isinstance(
                instance,
                PlatformComponentContract,
            ):
                continue

            platform_registry.register(
                component_id=component_id,
                instance=instance,
                name=name,
                version=getattr(
                    instance,
                    "VERSION",
                    "0.1.0",
                ),
                genesis=getattr(
                    instance,
                    "GENESIS",
                    "unknown",
                ),
                critical=True,
            )

            registered += 1

        return {
            "status": "PASS",
            "discovered": len(discovered),
            "registered": registered,
            "verified": registered,
            "failed": len(discovered) - registered,
        }

    # ============================================================
    # Boot Planning
    # ============================================================

    def create_boot_plan(self):

        discovered = self.discover()

        plan = BootPlan()

        for index, (
            component_id,
            name,
            instance,
        ) in enumerate(
            discovered,
            start=1,
        ):
            plan.candidates.append(
                BootCandidate(
                    component_id=component_id,
                    name=name,
                    priority=index * 10,
                    dependencies=[],
                    verified=isinstance(
                        instance,
                        PlatformComponentContract,
                    ),
                )
            )

        return plan

    # ============================================================
    # Reporting
    # ============================================================

    def report(self):

        return {
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "platform": platform_registry.statistics(),
        }

    def health(self):

        return {
            "name": "Runtime Self Assembly",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
        }

    def statistics(self):

        return self.report()


self_assembly = SelfAssembly()
