import re
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

        raise RuntimeError(f"Expected block not found for {label}: {path}")

    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
    )
    print(f"Patched: {label}")


# =========================================================
# 1. Compatibility adapter owns compat.statistics
# =========================================================

compat_path = Path("aletheus/runtime/adapters/compatibility_adapter.py")

replace_required(
    compat_path,
    """    def statistics(self, context):

        context.add_result(
            "compatibility_statistics",
            self.runtime.compat.statistics(),
        )

        return context
""",
    """    def statistics(self, context):

        statistics = self.runtime.compat.statistics()

        context.add_result(
            "compat_stats",
            statistics,
        )
        context.add_result(
            "compatibility_statistics",
            statistics,
        )

        return context
""",
    "compatibility statistics envelope",
)


# =========================================================
# 2. Canonical DecisionDomain must own decision.history
#
# The planning compatibility registrar currently overrides
# decision.history with cognition.decision_history().
# Remove only that duplicate registration and handler.
# =========================================================

planning_path = Path("aletheus/runtime/registrations/planning_commands.py")
planning_text = planning_path.read_text(encoding="utf-8")

planning_text = re.sub(
    r"\n    def decision_history\(payload=None\):\n"
    r"        return cognition\.decision_history\(\)\n",
    "\n",
    planning_text,
    count=1,
)

planning_text = re.sub(
    r"\n    commands\.register\(\n"
    r'        "decision\.history",\n'
    r"        decision_history,\n"
    r"        replace=True,\n"
    r"    \)\n",
    "\n",
    planning_text,
    count=1,
)

planning_path.write_text(
    planning_text,
    encoding="utf-8",
)

print("Removed planning override for canonical decision.history.")


# Ensure the canonical decision domain exposes both names.
decision_path = Path("aletheus/runtime/domains/decision.py")

replace_required(
    decision_path,
    """    def history(self, context):
        context.add_result(
            "history",
            self.runtime.decision.history(),
        )

        return context
""",
    """    def history(self, context):
        history = self.runtime.decision.history()

        context.add_result("history", history)
        context.add_result("decisions", history)

        return context
""",
    "canonical decision history envelope",
)


# =========================================================
# 3. Locate and normalize the real runtime.health handler
# =========================================================

runtime_candidates = [
    Path("aletheus/runtime/commands/runtime_commands.py"),
    Path("aletheus/runtime/domains/runtime.py"),
    Path("aletheus/runtime/adapters/runtime_adapter.py"),
]

patched_health = False

for path in runtime_candidates:
    if not path.exists():
        continue

    text = path.read_text(encoding="utf-8")

    # Legacy RuntimeCommands implementation.
    old = """    def health(self, context):
        context.add_result(
            "health",
            self.runtime.health(),
        )
        return context
"""

    new = """    def health(self, context):
        health = self.runtime.health()

        if isinstance(health, dict):
            original_status = health.get("status")

            if original_status == "online":
                health = dict(health)
                health["runtime_status"] = original_status
                health["status"] = "healthy"

        context.add_result("health", health)
        return context
"""

    if old in text:
        path.write_text(
            text.replace(old, new, 1),
            encoding="utf-8",
        )
        print(f"Patched runtime health handler: {path}")
        patched_health = True
        break

    # RuntimeDomain implementation.
    domain_pattern = re.compile(
        r"    def health\(self, context\):\n"
        r"(?:        .*\n)*?"
        r"        context\.add_result\(\n"
        r'            "health",\n'
        r"            RuntimeHealthService\(\)\.collect\(self\.runtime\),\n"
        r"        \)\n\n"
        r"        return context\n"
    )

    match = domain_pattern.search(text)

    if match:
        replacement = '''    def health(self, context):
        """
        Runtime health.
        """
        health = RuntimeHealthService().collect(self.runtime)

        if isinstance(health, dict):
            original_status = health.get("status")

            if original_status == "online":
                health = dict(health)
                health["runtime_status"] = original_status
                health["status"] = "healthy"

        context.add_result("health", health)

        return context
'''

        path.write_text(
            text[: match.start()] + replacement + text[match.end() :],
            encoding="utf-8",
        )

        print(f"Patched runtime health domain: {path}")
        patched_health = True
        break

if not patched_health:
    raise RuntimeError("Could not locate the authoritative runtime.health handler.")


print("Authoritative compatibility patch completed.")
