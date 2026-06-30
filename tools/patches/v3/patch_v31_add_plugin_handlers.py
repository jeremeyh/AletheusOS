from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "def _cmd_plugin_bootstrap" in text:
    print("Plugin handlers already exist.")
    raise SystemExit(0)

methods = '''

    # ==========================================================
    # v3.1 Plugin Manager
    # ==========================================================

    def _cmd_plugin_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "plugin",
            self.plugins_v3.bootstrap(),
        )
        return context

    def _cmd_plugin_install(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "plugin",
            self.plugins_v3.install(**context.payload),
        )
        return context

    def _cmd_plugin_enable(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "plugin",
            self.plugins_v3.enable(context.payload.get("plugin_id", "")),
        )
        return context

    def _cmd_plugin_disable(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "plugin",
            self.plugins_v3.disable(context.payload.get("plugin_id", "")),
        )
        return context

    def _cmd_plugin_update(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "plugin",
            self.plugins_v3.update(
                context.payload.get("plugin_id", ""),
                context.payload.get("version"),
            ),
        )
        return context

    def _cmd_plugin_remove(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "plugin",
            self.plugins_v3.remove(context.payload.get("plugin_id", "")),
        )
        return context

    def _cmd_plugin_list(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "plugins",
            self.plugins_v3.list(),
        )
        return context

    def _cmd_plugin_status(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "plugin_status",
            self.plugins_v3.status(),
        )
        return context

    def _cmd_plugin_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "plugin_stats",
            self.plugins_v3.statistics(),
        )
        return context

'''

anchor = "    def _job_runtime_pulse(self) -> dict:"

if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, methods + anchor, 1)

core.write_text(text)

print("✔ Plugin runtime handlers added.")
