from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

start = text.find("    # ==========================================================\n    # Runtime Compatibility Layer")
end = text.find("    def _job_runtime_pulse", start)

if start == -1 or end == -1:
    raise SystemExit("Could not locate compatibility block boundaries.")

block = '''
    # ==========================================================
    # Runtime Compatibility Layer
    # ==========================================================

    def _bootstrap_compatibility(self):
        self._register_compatibility_services()
        self._apply_compatibility_aliases()

    def _register_compatibility_services(self):
        registry = [
            ("memory", "memory"),
            ("knowledge", "knowledge"),
            ("reasoning", "reasoning"),
            ("decision", "decision"),
            ("planning", "planning_v2"),
            ("workflow", "workflow_v3"),
            ("agents", "agents_v2"),
            ("plugins", "plugins_v3"),
            ("persistence", "persistence_v3"),
            ("events", "event_bus_v3"),
            ("federation", "federation_v3"),
            ("telemetry", "telemetry_v3"),
            ("ha", "high_availability_v3"),
            ("security", "security_v3"),
            ("tenancy", "tenancy_v3"),
        ]

        for alias, attr in registry:
            service = getattr(self, attr, None)

            if service is not None:
                self.compat.register(
                    alias=alias,
                    implementation=service,
                )

    def _apply_compatibility_aliases(self):
        aliases = [
            "memory",
            "knowledge",
            "reasoning",
            "decision",
            "planning",
            "workflow",
            "agents",
            "plugins",
            "persistence",
            "events",
            "federation",
            "telemetry",
            "security",
            "tenancy",
        ]

        for alias in aliases:
            try:
                setattr(self, alias, self.compat.resolve(alias))
            except KeyError:
                pass

        try:
            self.high_availability = self.compat.resolve("ha")
        except KeyError:
            pass

'''

text = text[:start] + block + text[end:]

path.write_text(text)

print("✔ Rebuilt v4.1 compatibility block.")
