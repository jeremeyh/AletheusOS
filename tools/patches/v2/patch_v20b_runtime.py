from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

text = text.replace('self.version = "2.0.0-alpha"', 'self.version = "2.0.0-beta"')

if 'self.commands.register("application.install"' not in text:
    anchor = '        self.commands.register("application.stats", self._cmd_application_stats)\n'
    insert = """        self.commands.register("application.install", self._cmd_application_install)
        self.commands.register("application.uninstall", self._cmd_application_uninstall)
        self.commands.register("application.manifest", self._cmd_application_manifest)
        self.commands.register("application.events", self._cmd_application_events)
        self.commands.register("application.bootstrap.defaults", self._cmd_application_bootstrap_defaults)
"""
    if anchor in text:
        text = text.replace(anchor, anchor + insert)
    else:
        raise SystemExit("Could not find application.stats command anchor.")

if "def _cmd_application_install" not in text:
    anchor = "    def _cmd_cardhawk_foundation_bootstrap(self, context: RuntimeContext) -> RuntimeContext:\n"
    methods = """
    def _cmd_application_install(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        app = self.applications.install_application(
            app_id=payload.get("app_id", payload.get("application_id", "")),
            name=payload.get("name", "Unnamed Application"),
            version=payload.get("version", "1.0.0"),
            author=payload.get("author", "6th Dimension Multimedia"),
            description=payload.get("description", ""),
            autostart=bool(payload.get("autostart", False)),
            permissions=payload.get("permissions", []),
            dependencies=payload.get("dependencies", []),
            commands=payload.get("commands", []),
            services=payload.get("services", []),
        )
        self.kernel_v2.publish(
            event_type="application.installed",
            source="application_manager",
            payload=app.to_dict(),
        )
        context.add_result("application", app.to_dict())
        return context

    def _cmd_application_uninstall(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.applications.uninstall_application(
            app_id=payload.get("app_id", payload.get("application_id", "")),
            name=payload.get("name", ""),
        )
        self.kernel_v2.publish(
            event_type="application.uninstalled",
            source="application_manager",
            payload=result,
        )
        context.add_result("application", result)
        return context

    def _cmd_application_manifest(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.applications.manifest(
            app_id=payload.get("app_id", payload.get("application_id", "")),
            name=payload.get("name", ""),
        )
        context.add_result("manifest", result)
        return context

    def _cmd_application_events(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.applications.events(
            app_id=payload.get("app_id", payload.get("application_id", "")),
            name=payload.get("name", ""),
        )
        context.add_result("events", result)
        return context

    def _cmd_application_bootstrap_defaults(self, context: RuntimeContext) -> RuntimeContext:
        apps = self.applications.install_default_applications()
        self.kernel_v2.publish(
            event_type="applications.defaults_bootstrapped",
            source="application_manager",
            payload={"applications": apps},
        )
        context.add_result("applications", apps)
        return context

"""
    if anchor in text:
        text = text.replace(anchor, methods + anchor)
    else:
        raise SystemExit("Could not find cardhawk bootstrap method anchor.")

text = text.replace(
    '"Aletheus v2 Autonomous Kernel",\n            {"status": "online", "version": self.kernel_v2.version},',
    '"Aletheus v2 Autonomous Kernel",\n            {"status": "online", "version": self.kernel_v2.version},',
)

p.write_text(text)
print("v2.0B runtime application framework patch applied.")
