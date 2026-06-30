from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

if "from aletheus.runtime.integrity import RuntimeDoctor" not in text:
    marker = "from aletheus.runtime.hardening import RuntimeHardening"
    text = text.replace(
        marker,
        marker + "\nfrom aletheus.runtime.integrity import RuntimeDoctor, RuntimeInvariantEngine, RuntimeBootValidator",
        1,
    )

if "self.runtime_doctor = RuntimeDoctor(self)" not in text:
    marker = "self.hardening = RuntimeHardening(self)"
    text = text.replace(
        marker,
        marker + """
        self.runtime_doctor = RuntimeDoctor(self)
        self.runtime_invariants = RuntimeInvariantEngine(self)
        self.boot_validator = RuntimeBootValidator(self)
""",
        1,
    )

registration_anchor = '        self.commands.register("runtime.docs", self._cmd_runtime_docs)\n'

if 'self.commands.register("runtime.doctor"' not in text:
    text = text.replace(
        registration_anchor,
        registration_anchor + '''        self.commands.register("runtime.doctor", self._cmd_runtime_doctor)
        self.commands.register("runtime.invariants", self._cmd_runtime_invariants)
        self.commands.register("runtime.boot.validate", self._cmd_runtime_boot_validate)
        self.commands.register("runtime.health_report", self._cmd_runtime_health_report)
''',
        1,
    )

if "def _cmd_runtime_doctor" not in text:
    marker = "    def _job_runtime_pulse(self) -> dict:"
    handlers = '''
    # ==========================================================
    # v4.2.1 Runtime Integrity Commands
    # ==========================================================

    def _cmd_runtime_doctor(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("doctor", self.runtime_doctor.run())
        return context

    def _cmd_runtime_invariants(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("invariants", self.runtime_invariants.validate())
        return context

    def _cmd_runtime_boot_validate(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("boot_validation", self.boot_validator.validate())
        return context

    def _cmd_runtime_health_report(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("health_report", self.runtime_doctor.write_reports())
        return context


'''
    text = text.replace(marker, handlers + marker, 1)

text = text.replace('self.version = "4.1.1"', 'self.version = "4.2.1"')
text = text.replace('self.version = "4.1.2"', 'self.version = "4.2.1"')
text = text.replace('self.version = "4.1.3"', 'self.version = "4.2.1"')

path.write_text(text)

print("✔ v4.2.1 Runtime Integrity integrated.")
