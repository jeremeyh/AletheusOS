from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

if "from aletheus.enterprise import enterprise_core" not in text:
    text = text.replace(
        "from aletheus.workflows_v2 import workflow_v2_core\n",
        "from aletheus.workflows_v2 import workflow_v2_core\nfrom aletheus.enterprise import enterprise_core\n",
    )

text = text.replace('self.version = "2.0.0-d"', 'self.version = "2.1.0"')

if "self.enterprise = enterprise_core" not in text:
    text = text.replace(
        "self.workflow_v2 = workflow_v2_core\n\n        self.boot()",
        "self.workflow_v2 = workflow_v2_core\n        self.enterprise = enterprise_core\n\n        self.boot()",
    )

if 'self.commands.register("enterprise.stats"' not in text:
    anchor = '        self.commands.register("workflow.v2.stats", self._cmd_workflow_v2_stats)\n'
    insert = '''        self.commands.register("enterprise.bootstrap.cardhawk", self._cmd_enterprise_bootstrap_cardhawk)
        self.commands.register("enterprise.create", self._cmd_enterprise_create)
        self.commands.register("enterprise.list", self._cmd_enterprise_list)
        self.commands.register("enterprise.stats", self._cmd_enterprise_stats)
        self.commands.register("department.create", self._cmd_department_create)
        self.commands.register("team.create", self._cmd_team_create)
        self.commands.register("policy.create", self._cmd_policy_create)
        self.commands.register("governance.check", self._cmd_governance_check)
        self.commands.register("audit.history", self._cmd_audit_history)
'''
    if anchor not in text:
        raise SystemExit("Could not find workflow.v2.stats command anchor.")
    text = text.replace(anchor, anchor + insert)

if '"Aletheus Enterprise Intelligence Platform"' not in text:
    anchor = '''        self.services.register(
            "Aletheus v2 Autonomous Workflow Fabric",
            {"status": "online", "version": self.workflow_v2.version},
        )

        self.scheduler.register(
'''
    replacement = '''        self.services.register(
            "Aletheus v2 Autonomous Workflow Fabric",
            {"status": "online", "version": self.workflow_v2.version},
        )
        self.services.register(
            "Aletheus Enterprise Intelligence Platform",
            {"status": "online", "version": self.enterprise.version},
        )

        self.scheduler.register(
'''
    if anchor not in text:
        raise SystemExit("Could not find workflow service registration anchor.")
    text = text.replace(anchor, replacement)

if '"enterprises": self.enterprise.stats()["organizations"]' not in text:
    text = text.replace(
        '''                "v2_workflows": self.workflow_v2.stats()["workflows"],
                "v2_workflow_events": self.workflow_v2.stats()["events"],
            },
        )
        return context
''',
        '''                "v2_workflows": self.workflow_v2.stats()["workflows"],
                "v2_workflow_events": self.workflow_v2.stats()["events"],
                "enterprises": self.enterprise.stats()["organizations"],
                "enterprise_audit_events": self.enterprise.stats()["audit_events"],
                "compliance_score": self.enterprise.stats()["compliance_score"],
            },
        )
        return context
''',
    )

if 'context.add_result("enterprise", self.enterprise.stats())' not in text:
    text = text.replace(
        '''        context.add_result("workflow_v2", self.workflow_v2.stats())
        return context
''',
        '''        context.add_result("workflow_v2", self.workflow_v2.stats())
        context.add_result("enterprise", self.enterprise.stats())
        return context
''',
    )

if "def _cmd_enterprise_bootstrap_cardhawk" not in text:
    anchor = "    def _job_runtime_pulse(self) -> dict:\n"
    methods = '''
    def _cmd_enterprise_bootstrap_cardhawk(self, context: RuntimeContext) -> RuntimeContext:
        org = self.enterprise.bootstrap_cardhawk_enterprise()
        self.kernel_v2.publish(
            event_type="enterprise.cardhawk.bootstrapped",
            source="enterprise_core",
            payload=org.to_dict(),
        )
        context.add_result("enterprise", org.to_dict())
        return context

    def _cmd_enterprise_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        org = self.enterprise.create_organization(
            name=payload.get("name", "Untitled Enterprise"),
            description=payload.get("description", ""),
            applications=payload.get("applications", []),
        )
        context.add_result("enterprise", org.to_dict())
        return context

    def _cmd_enterprise_list(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("enterprises", self.enterprise.list_organizations())
        return context

    def _cmd_enterprise_stats(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("enterprise_stats", self.enterprise.stats())
        return context

    def _cmd_department_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.enterprise.create_department(
            organization_id=payload.get("organization_id", ""),
            name=payload.get("name", "Untitled Department"),
            description=payload.get("description", ""),
        )
        context.add_result("department", result)
        return context

    def _cmd_team_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.enterprise.create_team(
            organization_id=payload.get("organization_id", ""),
            department_id=payload.get("department_id", ""),
            name=payload.get("name", "Untitled Team"),
            description=payload.get("description", ""),
            members=payload.get("members", []),
        )
        context.add_result("team", result)
        return context

    def _cmd_policy_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.enterprise.create_policy(
            organization_id=payload.get("organization_id", ""),
            name=payload.get("name", "Untitled Policy"),
            description=payload.get("description", ""),
            scope=payload.get("scope", "enterprise"),
            rules=payload.get("rules", []),
        )
        context.add_result("policy", result)
        return context

    def _cmd_governance_check(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.enterprise.governed_action(
            actor=payload.get("actor", "founder"),
            action=payload.get("action", ""),
            target=payload.get("target", ""),
            organization_id=payload.get("organization_id", ""),
            metadata=payload.get("metadata", {}),
        )
        context.add_result("governance", result)
        return context

    def _cmd_audit_history(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("audit", self.enterprise.audit_history())
        return context

'''
    if anchor not in text:
        raise SystemExit("Could not find _job_runtime_pulse anchor.")
    text = text.replace(anchor, methods + anchor)

p.write_text(text)
print("v2.1 runtime enterprise patch applied.")
