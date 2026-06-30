from pathlib import Path
import re

core = Path("aletheus/runtime/core.py")
text = core.read_text()

pattern = re.compile(
    r"def _register_compatibility_services\(self\):.*?def _apply_compatibility_aliases",
    re.S,
)

replacement = '''
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

            if service is None:
                continue

            self.compat.register(
                alias=alias,
                implementation=service,
            )


    def _apply_compatibility_aliases'''

text, count = pattern.subn(replacement, text, count=1)

if count != 1:
    raise SystemExit(
        "Could not rebuild _register_compatibility_services()."
    )

core.write_text(text)

print("✔ Compatibility registration rebuilt.")
