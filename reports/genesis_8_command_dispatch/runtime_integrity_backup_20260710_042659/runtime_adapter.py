"""
Runtime Command Adapter

Genesis 7

Extracted from runtime/core.py

Owns runtime inspection and operational commands.
"""


class RuntimeCommandAdapter:

    def __init__(self, runtime):
        self.runtime = runtime


    def selftest(self, context):

        context.add_result(
            "selftest",
            self.runtime.certify_runtime(),
        )

        return context


    def dashboard(self, context):

        context.add_result(
            "dashboard",
            {
                "health": self.runtime.health(),
                "registry": self.runtime.registry_snapshot(),
                "commands": self.runtime.commands.count(),
            },
        )

        return context


    def snapshot(self, context):

        context.add_result(
            "snapshot",
            self.runtime.runtime_readiness(),
        )

        return context


    def audit(self, context):

        context.add_result(
            "audit",
            {
                "health": self.runtime.health(),
                "registry": self.runtime.registry_snapshot(),
                "architecture": self.runtime.architecture_validate(),
            },
        )

        return context


    def docs(self, context):

        context.add_result(
            "docs",
            self.runtime.generate_release_manifest(),
        )

        return context


    def doctor(self, context):

        context.add_result(
            "doctor",
            self.runtime.diagnostics(),
        )

        return context


    def invariants(self, context):

        context.add_result(
            "invariants",
            self.runtime.invariants(),
        )

        return context


    def boot_validate(self, context):

        context.add_result(
            "boot_validation",
            self.runtime.boot_certification_validate(),
        )

        return context


    def health_report(self, context):

        context.add_result(
            "health_report",
            self.runtime.health(),
        )

        return context
