"""
Compatibility Command Adapter.

Owns command-boundary translation for the runtime compatibility registry.
"""

from __future__ import annotations


class CompatibilityCommandAdapter:
    def __init__(self, runtime):
        self.runtime = runtime

    def list(self, context):
        services = self.runtime.compat.list()

        context.add_result(
            "services",
            services,
        )
        context.add_result(
            "compatibility",
            services,
        )

        return context

    def statistics(self, context):
        statistics = self.runtime.compat.statistics()

        context.add_result(
            "compat_stats",
            statistics,
        )
        context.add_result(
            "compatibility_statistics",
            statistics,
        )

        return context

    def resolve(self, context):
        payload = context.payload or {}

        alias = payload.get(
            "alias",
            payload.get(
                "name",
                payload.get("capability", ""),
            ),
        )

        service = self.runtime.compat.resolve(alias)

        context.add_result(
            "service",
            {
                "alias": alias,
                "resolved": service is not None,
                "type": (
                    f"{type(service).__module__}."
                    f"{type(service).__qualname__}"
                ),
                "version": getattr(
                    service,
                    "VERSION",
                    getattr(
                        service,
                        "version",
                        "unknown",
                    ),
                ),
            },
        )

        context.add_result(
            "compatibility_resolution",
            service,
        )

        return context

    def contract(self, context):
        payload = context.payload or {}

        alias = payload.get(
            "alias",
            payload.get("name", ""),
        )

        service = self.runtime.compat.resolve(alias)

        contract = {
            "name": alias,
            "resolved": service is not None,
            "version": getattr(
                service,
                "VERSION",
                getattr(
                    service,
                    "version",
                    "unknown",
                ),
            ),
            "type": (
                f"{type(service).__module__}."
                f"{type(service).__qualname__}"
            ),
        }

        context.add_result(
            "contract",
            contract,
        )
        context.add_result(
            "compatibility_contract",
            contract,
        )

        return context
