from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOTSTRAPPER = (
    ROOT
    / "aletheus/runtime/command_bootstrap/bootstrapper.py"
)

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = (
    ROOT
    / "reports/genesis_8_command_dispatch"
    / f"guarded_registration_backup_{stamp}"
)
backup_dir.mkdir(parents=True, exist_ok=True)

shutil.copy2(
    BOOTSTRAPPER,
    backup_dir / "bootstrapper.py",
)

text = BOOTSTRAPPER.read_text(encoding="utf-8")


if "import ast\n" not in text:
    text = "import ast\nimport inspect\n\n" + text


old_class = '''\
class RuntimeCommandBootstrapper:
    def bootstrap(self, runtime):
'''

new_class = '''\
class RuntimeCommandBootstrapper:

    LEGACY_REGISTRATION_FUNCTIONS = (
        register_graph_commands,
        register_mission_commands,
        register_workspace_commands,
        register_application_commands,
        register_semantic_commands,
        register_executive_commands,
        register_agent_commands,
        register_planning_commands,
        register_copilot_commands,
        register_uil_commands,
        register_decision_commands,
        register_compatibility_commands,
    )

    def __init__(self):
        self.compatibility_report = {
            "registered": [],
            "skipped": {},
        }

    @staticmethod
    def _required_runtime_attributes(registration_function):
        """
        Resolve direct runtime.<attribute> dependencies without executing
        the registration function.

        This occurs only during controlled bootstrap and never during
        command dispatch.
        """
        try:
            source = inspect.getsource(registration_function)
            tree = ast.parse(source)
        except (OSError, TypeError, IndentationError, SyntaxError):
            return set()

        required = set()

        for node in ast.walk(tree):
            if not isinstance(node, ast.Attribute):
                continue

            if (
                isinstance(node.value, ast.Name)
                and node.value.id == "runtime"
            ):
                required.add(node.attr)

        return required

    def _register_compatible(self, runtime, registration_function):
        required = self._required_runtime_attributes(
            registration_function
        )

        missing = sorted(
            attribute
            for attribute in required
            if not hasattr(runtime, attribute)
        )

        name = (
            f"{registration_function.__module__}."
            f"{registration_function.__name__}"
        )

        if missing:
            self.compatibility_report["skipped"][name] = {
                "reason": "missing_runtime_attributes",
                "missing": missing,
            }
            return False

        registration_function(runtime)

        self.compatibility_report["registered"].append(name)
        return True

    def bootstrap(self, runtime):
'''

if old_class not in text:
    raise RuntimeError(
        "RuntimeCommandBootstrapper class header was not found."
    )

text = text.replace(old_class, new_class, 1)


old_calls = '''\
        # Legacy and compatibility command families.
        # These remain first-class bootstrap registrations
        # until their public contracts are formally retired.
        register_graph_commands(runtime)
        register_mission_commands(runtime)
        register_workspace_commands(runtime)
        register_application_commands(runtime)
        register_semantic_commands(runtime)
        register_executive_commands(runtime)
        register_agent_commands(runtime)
        register_planning_commands(runtime)
        register_copilot_commands(runtime)
        register_uil_commands(runtime)
        register_decision_commands(runtime)
        register_compatibility_commands(runtime)
'''

new_calls = '''\
        # Legacy and compatibility command families.
        #
        # Preflight dependency validation prevents stale registration
        # modules from partially mutating the registry or blocking boot.
        for registration_function in (
            self.LEGACY_REGISTRATION_FUNCTIONS
        ):
            self._register_compatible(
                runtime,
                registration_function,
            )
'''

if old_calls not in text:
    raise RuntimeError(
        "Legacy registration call block was not found."
    )

text = text.replace(old_calls, new_calls, 1)

BOOTSTRAPPER.write_text(
    text,
    encoding="utf-8",
)

print("Guarded legacy registration catalog installed.")
print(f"Backup: {backup_dir.relative_to(ROOT)}")
print(f"Updated: {BOOTSTRAPPER.relative_to(ROOT)}")
