from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# ------------------------------------------------------------
# Import
# ------------------------------------------------------------

import_line = "from aletheus.runtime.compat import compatibility_registry"

if import_line not in text:
    anchor = "from aletheus.runtime.kernel import"
    idx = text.find(anchor)
    if idx == -1:
        raise SystemExit("Kernel import block not found.")

    end = text.find("\n", idx)
    text = text[:end+1] + import_line + "\n" + text[end+1:]

# ------------------------------------------------------------
# Runtime initialization
# ------------------------------------------------------------

if "self.compat = compatibility_registry" not in text:

    anchor = "self.kernel = KernelExecutor(self)"

    if anchor not in text:
        raise SystemExit("KernelExecutor initialization not found.")

    replacement = anchor + """

        # Runtime Compatibility Layer
        self.compat = compatibility_registry

        self._register_compatibility_services()
        self._apply_compatibility_aliases()
"""

    text = text.replace(anchor, replacement, 1)

# ------------------------------------------------------------
# Minimal registration helpers
# ------------------------------------------------------------

if "def _register_compatibility_services" not in text:

    methods = '''

    # ==========================================================
    # Runtime Compatibility Layer
    # ==========================================================

    def _register_compatibility_services(self):

        mappings = {
            "memory": getattr(self, "memory", None),
            "knowledge": getattr(self, "knowledge", None),
            "reasoning": getattr(self, "reasoning", None),
            "decision": getattr(self, "decision", None),
            "planning": getattr(self, "planning_v2", None),
            "workflow": getattr(self, "workflow_v3", None),
            "agents": getattr(self, "agents_v2", None),
            "plugins": getattr(self, "plugins_v3", None),
            "persistence": getattr(self, "persistence_v3", None),
            "events": getattr(self, "event_bus_v3", None),
            "federation": getattr(self, "federation_v3", None),
            "telemetry": getattr(self, "telemetry_v3", None),
            "security": getattr(self, "security_v3", None),
            "tenancy": getattr(self, "tenancy_v3", None),
            "ha": getattr(self, "high_availability_v3", None),
        }

        for alias, impl in mappings.items():
            if impl is not None:
                self.compat.register(alias, impl)

    def _apply_compatibility_aliases(self):

        aliases = {
            "planning": "planning",
            "workflow": "workflow",
            "agents": "agents",
            "memory": "memory",
            "knowledge": "knowledge",
            "reasoning": "reasoning",
            "decision": "decision",
            "plugins": "plugins",
            "persistence": "persistence",
            "events": "events",
            "federation": "federation",
            "telemetry": "telemetry",
            "security": "security",
            "tenancy": "tenancy",
        }

        for attr, alias in aliases.items():
            try:
                setattr(self, attr, self.compat.resolve(alias))
            except Exception:
                pass

        try:
            self.high_availability = self.compat.resolve("ha")
        except Exception:
            pass

'''

    anchor = "    def _job_runtime_pulse"

    if anchor not in text:
        raise SystemExit("_job_runtime_pulse not found.")

    text = text.replace(anchor, methods + "\n" + anchor, 1)

core.write_text(text)

print("✔ Runtime Compatibility Layer initialized.")
