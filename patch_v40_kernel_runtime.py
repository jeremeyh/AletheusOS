from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

changed = False

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

imports = """
from aletheus.runtime.kernel import (
    intelligence_orchestrator,
    intelligence_scheduler,
    intelligence_dispatcher,
    intelligence_supervisor,
)
"""

if "intelligence_orchestrator" not in text:

    anchor = "from aletheus.tenancy_v3 import tenancy_core"

    if anchor not in text:
        raise SystemExit("Tenancy import anchor not found.")

    text = text.replace(
        anchor,
        anchor + "\n" + imports.strip(),
        1,
    )

    changed = True

# ------------------------------------------------------------
# Runtime initialization
# ------------------------------------------------------------

if "self.intelligence_orchestrator = intelligence_orchestrator" not in text:

    anchor = "self.tenancy_v3 = tenancy_core"

    if anchor not in text:
        raise SystemExit("Tenancy runtime anchor not found.")

    replacement = anchor + """

        self.intelligence_orchestrator = intelligence_orchestrator
        self.intelligence_scheduler = intelligence_scheduler
        self.intelligence_dispatcher = intelligence_dispatcher
        self.intelligence_supervisor = intelligence_supervisor
"""

    text = text.replace(anchor, replacement, 1)

    changed = True

# ------------------------------------------------------------
# Runtime version
# ------------------------------------------------------------

text = text.replace(
    'self.version = "3.9.0"',
    'self.version = "4.0.0"',
)

# ------------------------------------------------------------
# Command registration
# ------------------------------------------------------------

if 'self.commands.register("kernel.bootstrap"' not in text:

    anchor = 'self.commands.register("tenant.health", self._cmd_tenant_health)'

    if anchor not in text:
        raise SystemExit("Tenant command anchor not found.")

    kernel_commands = '''

        # ======================================================
        # v4.0 Intelligence Kernel
        # ======================================================

        self.commands.register(
            "kernel.bootstrap",
            self._cmd_kernel_bootstrap,
        )

        self.commands.register(
            "kernel.execute",
            self._cmd_kernel_execute,
        )

        self.commands.register(
            "kernel.tasks",
            self._cmd_kernel_tasks,
        )

        self.commands.register(
            "kernel.scheduler",
            self._cmd_kernel_scheduler,
        )

        self.commands.register(
            "kernel.dispatcher",
            self._cmd_kernel_dispatcher,
        )

        self.commands.register(
            "kernel.supervisor",
            self._cmd_kernel_supervisor,
        )

        self.commands.register(
            "kernel.statistics",
            self._cmd_kernel_statistics,
        )
'''

    text = text.replace(anchor, anchor + kernel_commands, 1)

    changed = True

if changed:
    core.write_text(text)
    print("✔ AletheusOS v4.0 Intelligence Kernel runtime integrated.")
else:
    print("✔ Runtime already integrated.")
