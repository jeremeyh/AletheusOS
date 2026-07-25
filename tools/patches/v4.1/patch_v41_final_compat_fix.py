import re
from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

# Remove all direct bootstrap calls first.
text = re.sub(
    r"\n\s*self\._bootstrap_compatibility\(\)\n",
    "\n",
    text,
)

# Ensure compat object exists before boot.
if "self.compat = compatibility_registry" not in text:
    anchor = "        self.tenancy_v3 = tenancy_core"
    if anchor not in text:
        raise SystemExit("tenancy_v3 anchor not found.")
    text = text.replace(
        anchor,
        anchor + "\n        self.compat = compatibility_registry",
        1,
    )

# Ensure bootstrap runs once after boot, when all engines exist.
anchor = "        self.boot()\n"
if anchor not in text:
    raise SystemExit("self.boot() anchor not found.")

text = text.replace(
    anchor,
    anchor + "        self._bootstrap_compatibility()\n",
    1,
)

# Replace full compatibility block safely.
start = text.find("    # ==========================================================\n    # Runtime Compatibility Layer")
end = text.find("    def _job_runtime_pulse", start)

if start == -1 or end == -1:
    raise SystemExit("Could not find compatibility block boundaries.")

block = '''
    # ==========================================================
    # Runtime Compatibility Layer
    # ==========================================================

    def _bootstrap_compatibility(self):
        self.compat.services.clear()
        self._register_compatibility_services()
        self._apply_compatibility_aliases()

    def _register_compatibility_services(self):
        registry = [
            ("memory", ["memory"]),
            ("knowledge", ["knowledge"]),
            ("reasoning", ["reasoning"]),
            ("decision", ["decision"]),
            ("planning", ["planning_v2", "planning"]),
            ("workflow", ["workflow_v3", "workflow_v2", "workflow"]),
            ("agents", ["agents_v2", "agents"]),
            ("plugins", ["plugins_v3"]),
            ("persistence", ["persistence_v3"]),
            ("events", ["event_bus_v3"]),
            ("federation", ["federation_v3"]),
            ("telemetry", ["telemetry_v3"]),
            ("ha", ["high_availability_v3"]),
            ("security", ["security_v3"]),
            ("tenancy", ["tenancy_v3"]),
        ]

        for alias, attrs in registry:
            service = None

            for attr in attrs:
                candidate = getattr(self, attr, None)
                if candidate is not None:
                    service = candidate
                    break

            if service is not None:
                self.compat.register(
                    alias=alias,
                    implementation=service,
                )

    def _apply_compatibility_aliases(self):
        # Safe canonical aliases only.
        # Do not overwrite core runtime infrastructure like self.events or self.plugins.
        safe_aliases = [
            "memory",
            "knowledge",
            "reasoning",
            "decision",
            "planning",
            "workflow",
            "agents",
            "security",
            "tenancy",
        ]

        for alias in safe_aliases:
            try:
                setattr(self, alias, self.compat.resolve(alias))
            except KeyError:
                pass

        try:
            self.high_availability = self.compat.resolve("ha")
        except KeyError:
            pass

        try:
            self.event_bus = self.compat.resolve("events")
        except KeyError:
            pass

'''

text = text[:start] + block + text[end:]

text = text.replace('self.version = "4.0.0"', 'self.version = "4.1.0"')

path.write_text(text)

print("✔ v4.1 compatibility layer finalized.")
