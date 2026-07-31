from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# ---------------------------------------------------------
# Register commands
# ---------------------------------------------------------

anchor = (
    '        self.commands.register("kernel.statistics", self._cmd_kernel_statistics)\n'
)

if anchor not in text:
    raise SystemExit("Kernel command registration anchor not found.")

registration = """
        self.commands.register("compat.list", self._cmd_compat_list)
        self.commands.register("compat.resolve", self._cmd_compat_resolve)
        self.commands.register("compat.statistics", self._cmd_compat_statistics)
        self.commands.register("compat.contract", self._cmd_compat_contract)
"""

if 'self.commands.register("compat.statistics"' not in text:
    text = text.replace(anchor, anchor + registration, 1)

# ---------------------------------------------------------
# Command handlers
# ---------------------------------------------------------

handlers = """

    # ==========================================================
    # Runtime Compatibility Commands
    # ==========================================================

    def _cmd_compat_list(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "services",
            self.compat.list(),
        )

        return context


    def _cmd_compat_statistics(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "compat_stats",
            self.compat.statistics(),
        )

        return context


    def _cmd_compat_resolve(self, context: RuntimeContext) -> RuntimeContext:

        alias = context.payload.get("alias")

        service = self.compat.resolve(alias)

        context.add_result(
            "service",
            {
                "alias": alias,
                "resolved": True,
                "implementation": type(service).__name__,
            },
        )

        return context


    def _cmd_compat_contract(self, context: RuntimeContext) -> RuntimeContext:

        alias = context.payload.get("alias")

        service = self.compat.resolve(alias)

        context.add_result(
            "contract",
            {
                "name": alias,
                "version": getattr(
                    service,
                    "VERSION",
                    getattr(service, "version", "unknown"),
                ),
                "implementation": type(service).__name__,
            },
        )

        return context

"""

if "def _cmd_compat_statistics" not in text:
    marker = "\n\nruntime_core = AletheusRuntime()"

    if marker not in text:
        raise SystemExit("Could not locate runtime_core instantiation.")

    text = text.replace(marker, handlers + marker)

core.write_text(text)

print("✔ Added Runtime Compatibility command handlers.")
