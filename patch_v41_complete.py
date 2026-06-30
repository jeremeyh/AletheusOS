from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# Import compatibility registry
if "from aletheus.runtime.compat import compatibility_registry" not in text:
    anchor = "from aletheus.runtime.kernel import"
    idx = text.find(anchor)
    if idx == -1:
        raise SystemExit("Kernel import anchor not found.")
    line_end = text.find("\n", idx)
    text = text[:line_end+1] + "from aletheus.runtime.compat import compatibility_registry\n" + text[line_end+1:]

# Add compat initialization after KernelExecutor
if "self.compat = compatibility_registry" not in text:
    anchor = "self.kernel = KernelExecutor(self)"
    if anchor not in text:
        raise SystemExit("KernelExecutor init anchor not found.")
    compat_block = '''
        self.compat = compatibility_registry
        self._register_compatibility_services()
        self._apply_compatibility_aliases()
'''
    text = text.replace(anchor, anchor + compat_block, 1)

# Version
text = text.replace('self.version = "4.0.0"', 'self.version = "4.1.0"')
text = text.replace('self.version = "3.9.0"', 'self.version = "4.1.0"')

# Register compat commands
if 'self.commands.register("compat.list"' not in text:
    anchor = 'self.commands.register("kernel.statistics", self._cmd_kernel_statistics)'
    if anchor not in text:
        raise SystemExit("Kernel command anchor not found.")
    text = text.replace(anchor, anchor + '''

        # v4.1 Runtime Compatibility Layer
        self.commands.register("compat.list", self._cmd_compat_list)
        self.commands.register("compat.resolve", self._cmd_compat_resolve)
        self.commands.register("compat.statistics", self._cmd_compat_statistics)
        self.commands.register("compat.contract", self._cmd_compat_contract)
''', 1)

# Add methods before _job_runtime_pulse
if "def _register_compatibility_services" not in text:
    methods = '''

    # ==========================================================
    # v4.1 Runtime Compatibility Layer
    # ==========================================================

    def _register_compatibility_services(self) -> None:
        mappings = [
            ("memory", getattr(self, "memory", None), ["memory", "storage"]),
            ("knowledge", getattr(self, "knowledge", None), ["knowledge"]),
            ("reasoning", getattr(self, "reasoning", None), ["reasoning"]),
            ("decision", getattr(self, "decision", None), ["decision"]),
            ("planning", getattr(self, "planning_v2", None), ["planning"]),
            ("workflow", getattr(self, "workflow_v3", None), ["workflow"]),
            ("agents", getattr(self, "agents_v2", None), ["agents"]),
            ("plugins", getattr(self, "plugins_v3", None), ["plugins"]),
            ("persistence", getattr(self, "persistence_v3", None), ["persistence"]),
            ("events", getattr(self, "event_bus_v3", None), ["events"]),
            ("federation", getattr(self, "federation_v3", None), ["federation"]),
            ("telemetry", getattr(self, "telemetry_v3", None), ["telemetry"]),
            ("ha", getattr(self, "high_availability_v3", None), ["ha", "replication"]),
            ("security", getattr(self, "security_v3", None), ["security", "policy"]),
            ("tenancy", getattr(self, "tenancy_v3", None), ["tenancy"]),
        ]

        for alias, implementation, capabilities in mappings:
            if implementation is not None:
                self.compat.register(
                    alias=alias,
                    implementation=implementation,
                    capabilities=capabilities,
                )

    def _apply_compatibility_aliases(self) -> None:
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

    def _cmd_compat_list(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("compat", self.compat.list())
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
                    "implementation": service.__class__.__name__,
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

    def _cmd_compat_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("compat_stats", self.compat.statistics())
        return context

    def _cmd_compat_contract(self, context: RuntimeContext) -> RuntimeContext:
        alias = context.payload.get("alias", "")
        try:
            service = self.compat.services[alias]
            context.add_result(
                "contract",
                {
                    "name": service.alias,
                    "version": service.version,
                    "capabilities": service.capabilities,
                    "implementation": service.implementation.__class__.__name__,
                },
            )
        except KeyError:
            context.add_result(
                "contract",
                {
                    "alias": alias,
                    "error": "Service alias not found",
                },
            )
        return context

'''
    anchor = "    def _job_runtime_pulse(self) -> dict:"
    if anchor not in text:
        raise SystemExit("_job_runtime_pulse anchor not found.")
    text = text.replace(anchor, methods + anchor, 1)

Path("aletheus/runtime/core.py").write_text(text)
print("✔ v4.1 Runtime Compatibility Layer integrated.")
