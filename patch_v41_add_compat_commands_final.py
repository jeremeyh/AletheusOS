from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

# ---------------------------------------------------------
# 1. Register compat commands after HA registrations
# ---------------------------------------------------------

if 'self.commands.register("compat.statistics"' not in text:
    anchor = '        self.commands.register("ha.statistics", self._cmd_ha_statistics)\n'

    if anchor not in text:
        raise SystemExit("HA statistics registration anchor not found.")

    registration = '''
        # v4.1 Runtime Compatibility Layer
        self.commands.register("compat.list", self._cmd_compat_list)
        self.commands.register("compat.resolve", self._cmd_compat_resolve)
        self.commands.register("compat.statistics", self._cmd_compat_statistics)
        self.commands.register("compat.contract", self._cmd_compat_contract)

'''

    text = text.replace(anchor, anchor + registration, 1)

# ---------------------------------------------------------
# 2. Add handlers before _job_runtime_pulse
# ---------------------------------------------------------

if "def _cmd_compat_statistics" not in text:
    marker = "    def _job_runtime_pulse(self) -> dict:"

    if marker not in text:
        raise SystemExit("_job_runtime_pulse marker not found.")

    handlers = '''
    # ==========================================================
    # v4.1 Runtime Compatibility Commands
    # ==========================================================

    def _cmd_compat_list(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("services", self.compat.list())
        return context

    def _cmd_compat_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("compat_stats", self.compat.statistics())
        return context

    def _cmd_compat_resolve(self, context: RuntimeContext) -> RuntimeContext:
        alias = context.payload.get("alias", "")

        try:
            service = self.compat.resolve(alias)
            context.add_result(
                "service",
                {
                    "alias": alias,
                    "resolved": True,
                    "implementation": type(service).__name__,
                    "version": getattr(service, "VERSION", getattr(service, "version", "unknown")),
                },
            )
        except KeyError:
            context.add_result(
                "service",
                {
                    "alias": alias,
                    "resolved": False,
                    "error": "Service alias not found",
                },
            )

        return context

    def _cmd_compat_contract(self, context: RuntimeContext) -> RuntimeContext:
        alias = context.payload.get("alias", "")

        try:
            service = self.compat.resolve(alias)
            context.add_result(
                "contract",
                {
                    "name": alias,
                    "version": getattr(service, "VERSION", getattr(service, "version", "unknown")),
                    "implementation": type(service).__name__,
                },
            )
        except KeyError:
            context.add_result(
                "contract",
                {
                    "name": alias,
                    "error": "Service alias not found",
                },
            )

        return context


'''

    text = text.replace(marker, handlers + marker, 1)

path.write_text(text)

print("✔ Added v4.1 compat command registrations and handlers.")
