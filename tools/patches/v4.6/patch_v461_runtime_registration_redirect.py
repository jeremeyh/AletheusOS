from pathlib import Path

CORE = Path("aletheus/runtime/core.py")

if not CORE.exists():
    raise SystemExit("runtime/core.py not found.")

text = CORE.read_text()

old = """
        self.commands.register("runtime.version", self._cmd_runtime_version)
        self.commands.register("runtime.status", self._cmd_runtime_status)
        self.commands.register("runtime.health", self._cmd_runtime_health)
        self.commands.register("runtime.metrics", self._cmd_metrics)
        self.commands.register("runtime.events", self._cmd_events)
        self.commands.register("runtime.queue", self._cmd_queue)
        self.commands.register("runtime.run_next_job", self._cmd_run_next_job)
        self.commands.register("runtime.docs", self._cmd_runtime_docs)
        self.commands.register("runtime.doctor", self._cmd_runtime_doctor)
        self.commands.register("runtime.invariants", self._cmd_runtime_invariants)
        self.commands.register("runtime.boot.validate", self._cmd_runtime_boot_validate)
        self.commands.register("runtime.health_report", self._cmd_runtime_health_report)
"""

new = """
        register_runtime_commands(self)
"""

if old in text:
    text = text.replace(old, new, 1)

import_line = (
    "from aletheus.runtime.registrations import register_runtime_commands\n"
)

if "register_runtime_commands" not in text:
    marker = "from aletheus.runtime.modules import"
    idx = text.find(marker)

    if idx != -1:
        insert = text.find("\n", idx)
        text = text[:insert + 1] + import_line + text[insert + 1:]

CORE.write_text(text)

print("✔ Runtime registration redirected.")
