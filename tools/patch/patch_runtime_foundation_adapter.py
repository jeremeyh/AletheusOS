import re
from pathlib import Path

PATH = Path("aletheus/runtime/adapters/runtime_adapter.py")

text = PATH.read_text(encoding="utf-8")


def replace_method(
    source: str,
    method_name: str,
    replacement: str,
) -> str:
    pattern = re.compile(
        rf"    def {re.escape(method_name)}\(self, context\):\n"
        rf".*?"
        rf"        return context\n",
        flags=re.DOTALL,
    )

    match = pattern.search(source)

    if match is None:
        raise RuntimeError(f"RuntimeCommandAdapter.{method_name} was not found.")

    return source[: match.start()] + replacement.rstrip() + "\n" + source[match.end() :]


selftest = """
    def selftest(self, context):
        health = self.runtime.runtime_facade.health()

        passed = bool(
            health.get("booted", False)
            and health.get("status") in {
                "healthy",
                "online",
            }
        )

        context.add_result(
            "selftest",
            {
                "status": (
                    "pass" if passed else "fail"
                ),
                "health": health,
                "commands": self.runtime.commands.count(),
            },
        )

        return context
"""


dashboard = """
    def dashboard(self, context):
        health = self.runtime.runtime_facade.health()

        context.add_result(
            "dashboard",
            {
                "health": (
                    "pass"
                    if health.get("status")
                    in {"healthy", "online"}
                    else "fail"
                ),
                "runtime": health,
                "registry": self.runtime.registry_snapshot(),
                "commands": self.runtime.commands.count(),
            },
        )

        return context
"""


snapshot = """
    def snapshot(self, context):
        compatibility = {}

        compat = getattr(
            self.runtime,
            "compat",
            None,
        )

        if compat is not None:
            statistics = getattr(
                compat,
                "statistics",
                None,
            )

            if callable(statistics):
                compatibility = statistics()

        kernel = getattr(
            self.runtime,
            "kernel_v2",
            getattr(
                self.runtime,
                "kernel",
                None,
            ),
        )

        kernel_snapshot = {}

        if kernel is not None:
            snapshot_method = getattr(
                kernel,
                "snapshot",
                None,
            )

            if callable(snapshot_method):
                try:
                    kernel_snapshot = snapshot_method()
                except TypeError:
                    kernel_snapshot = {
                        "version": getattr(
                            kernel,
                            "version",
                            "unknown",
                        ),
                        "status": "online",
                    }
            else:
                kernel_snapshot = {
                    "version": getattr(
                        kernel,
                        "version",
                        "unknown",
                    ),
                    "status": "online",
                }

        context.add_result(
            "snapshot",
            {
                "commands": {
                    "count": self.runtime.commands.count(),
                },
                "compatibility": compatibility,
                "kernel": kernel_snapshot,
                "registry": self.runtime.registry_snapshot(),
                "runtime": self.runtime.runtime_facade.health(),
            },
        )

        return context
"""


audit = """
    def audit(self, context):
        health = self.runtime.runtime_facade.health()

        registry = self.runtime.registry_snapshot()

        compatibility = {}

        compat = getattr(
            self.runtime,
            "compat",
            None,
        )

        if compat is not None:
            statistics = getattr(
                compat,
                "statistics",
                None,
            )

            if callable(statistics):
                compatibility = statistics()

        status = (
            "healthy"
            if health.get("booted", False)
            else "warning"
        )

        context.add_result(
            "audit",
            {
                "health": status,
                "runtime": health,
                "registry": registry,
                "compatibility": compatibility,
                "command_count": self.runtime.commands.count(),
            },
        )

        return context
"""


docs = """
    def docs(self, context):
        from pathlib import Path

        payload = context.payload or {}

        output_path = Path(
            payload.get(
                "path",
                "RUNTIME_DOCUMENTATION.md",
            )
        )

        health = self.runtime.runtime_facade.health()
        registry = self.runtime.registry_snapshot()

        content = (
            "# AletheusOS Runtime Documentation\\n\\n"
            f"- Version: `{health.get('version', 'unknown')}`\\n"
            f"- Status: `{health.get('status', 'unknown')}`\\n"
            f"- Booted: `{health.get('booted', False)}`\\n"
            f"- Commands: `{self.runtime.commands.count()}`\\n"
            f"- Registry entries: `{len(registry) if hasattr(registry, '__len__') else 0}`\\n"
        )

        output_path.write_text(
            content,
            encoding="utf-8",
        )

        documentation = {
            "status": "written",
            "path": str(output_path),
            "bytes": len(
                content.encode("utf-8")
            ),
        }

        context.add_result(
            "documentation",
            documentation,
        )
        context.add_result(
            "docs",
            documentation,
        )

        return context
"""


for method_name, replacement in (
    ("selftest", selftest),
    ("dashboard", dashboard),
    ("snapshot", snapshot),
    ("audit", audit),
    ("docs", docs),
):
    text = replace_method(
        text,
        method_name,
        replacement,
    )

PATH.write_text(
    text,
    encoding="utf-8",
)

print("Runtime Engineering Foundation adapter repaired.")
