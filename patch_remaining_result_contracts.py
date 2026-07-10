from pathlib import Path


def replace_required(
    path: Path,
    old: str,
    new: str,
    label: str,
) -> None:
    text = path.read_text(encoding="utf-8")

    if old not in text:
        if new in text:
            print(f"Already patched: {label}")
            return

        raise RuntimeError(
            f"Could not locate expected block for {label}: {path}"
        )

    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
    )

    print(f"Patched: {label}")


# ---------------------------------------------------------
# Enterprise audit.history
# ---------------------------------------------------------

replace_required(
    Path("aletheus/runtime/domains/enterprise.py"),
    '''    def audit_history(self, context):
        context.add_result(
            "audit_history",
            self.runtime.enterprise.audit_history(),
        )
        return context
''',
    '''    def audit_history(self, context):
        history = self.runtime.enterprise.audit_history()

        # Canonical v2.1 result plus historical compatibility alias.
        context.add_result("audit", history)
        context.add_result("audit_history", history)

        return context
''',
    "enterprise audit envelope",
)


# ---------------------------------------------------------
# Memory Mesh
# ---------------------------------------------------------

memory_path = Path(
    "aletheus/runtime/domains/memory_mesh.py"
)

replace_required(
    memory_path,
    '''        context.add_result("memory", result)
        return context

    def retrieve(self, context):
''',
    '''        context.add_result("memory_object", result)
        context.add_result("memory", result)
        return context

    def retrieve(self, context):
''',
    "memory.mesh.store envelope",
)

replace_required(
    memory_path,
    '''        context.add_result("memory", result)
        return context

    def search(self, context):
''',
    '''        context.add_result("memory_object", result)
        context.add_result("memory", result)
        return context

    def search(self, context):
''',
    "memory.mesh.retrieve envelope",
)

replace_required(
    memory_path,
    '''        context.add_result("memory_search", result)
        return context
''',
    '''        context.add_result("results", result)
        context.add_result("memory_search", result)
        return context
''',
    "memory.mesh.search envelope",
)


# ---------------------------------------------------------
# Decision history
# ---------------------------------------------------------

decision_path = Path(
    "aletheus/runtime/domains/decision.py"
)

replace_required(
    decision_path,
    '''    def history(self, context):
        context.add_result(
            "history",
            self.runtime.decision.history(),
        )

        return context
''',
    '''    def history(self, context):
        history = self.runtime.decision.history()

        context.add_result("history", history)
        context.add_result("decisions", history)

        return context
''',
    "decision history envelope",
)


# ---------------------------------------------------------
# Runtime health
# ---------------------------------------------------------

runtime_path = Path(
    "aletheus/runtime/domains/runtime.py"
)

replace_required(
    runtime_path,
    '''        context.add_result(
            "health",
            RuntimeHealthService().collect(self.runtime),
        )

        return context
''',
    '''        health = RuntimeHealthService().collect(self.runtime)

        # Public runtime.health contract uses "healthy". Preserve the
        # original operational state separately when it reports "online".
        if isinstance(health, dict):
            original_status = health.get("status")

            if original_status == "online":
                health["runtime_status"] = original_status
                health["status"] = "healthy"

        context.add_result("health", health)

        return context
''',
    "runtime health status normalization",
)

print("Remaining result-contract patch completed.")
