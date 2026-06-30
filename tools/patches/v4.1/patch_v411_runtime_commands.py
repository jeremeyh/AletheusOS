from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

# Import RuntimeHardening
if "from aletheus.runtime.hardening import RuntimeHardening" not in text:
    marker = "from aletheus.runtime.workflow import WorkflowExecutor, WorkflowGraph"
    text = text.replace(
        marker,
        marker + "\nfrom aletheus.runtime.hardening import RuntimeHardening",
        1,
    )

# Initialize hardening after compatibility bootstrap
if "self.hardening = RuntimeHardening(self)" not in text:
    marker = "self._bootstrap_compatibility()"
    text = text.replace(
        marker,
        marker + "\n        self.hardening = RuntimeHardening(self)",
        1,
    )

# Register commands
registration_anchor = '        self.commands.register("runtime.diagnostics", self._cmd_diagnostics)\n'

registrations = '''        self.commands.register("runtime.selftest", self._cmd_runtime_selftest)
        self.commands.register("runtime.dashboard", self._cmd_runtime_dashboard)
        self.commands.register("runtime.snapshot", self._cmd_runtime_snapshot)
        self.commands.register("runtime.audit", self._cmd_runtime_audit)
        self.commands.register("runtime.docs", self._cmd_runtime_docs)
'''

if 'self.commands.register("runtime.selftest"' not in text:
    text = text.replace(registration_anchor, registration_anchor + registrations, 1)

# Add handlers before _job_runtime_pulse
if "def _cmd_runtime_selftest" not in text:
    marker = "    def _job_runtime_pulse(self) -> dict:"
    handlers = '''
    # ==========================================================
    # v4.1.1 Engineering Foundation Commands
    # ==========================================================

    def _cmd_runtime_selftest(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("selftest", self.hardening.selftest())
        return context

    def _cmd_runtime_dashboard(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("dashboard", self.hardening.dashboard())
        return context

    def _cmd_runtime_snapshot(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("snapshot", self.hardening.snapshot())
        return context

    def _cmd_runtime_audit(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("audit", self.hardening.audit())
        return context

    def _cmd_runtime_docs(self, context: RuntimeContext) -> RuntimeContext:
        path = context.payload.get("path", "RUNTIME_DOCUMENTATION.md")
        context.add_result("documentation", self.hardening.write_documentation(path))
        return context


'''
    text = text.replace(marker, handlers + marker, 1)

text = text.replace('self.version = "4.1.0"', 'self.version = "4.1.1"')

path.write_text(text)

print("✔ v4.1.1 runtime commands integrated.")
