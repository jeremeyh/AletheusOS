from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ADAPTER = ROOT / "aletheus/runtime/adapters/runtime_adapter.py"
REGISTRATIONS = (
    ROOT / "aletheus/runtime/registrations/runtime_commands.py"
)

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = (
    ROOT
    / "reports/genesis_8_command_dispatch"
    / f"runtime_integrity_backup_{stamp}"
)
backup.mkdir(parents=True, exist_ok=True)

shutil.copy2(ADAPTER, backup / "runtime_adapter.py")
shutil.copy2(REGISTRATIONS, backup / "runtime_commands.py")


ADAPTER_SOURCE = '''\
"""
Runtime Command Adapter

Genesis 8 compatibility repair.

Owns runtime inspection and operational command adaptation while binding
commands to the current runtime manager and service surfaces.
"""

from __future__ import annotations

from typing import Any


class RuntimeCommandAdapter:

    def __init__(self, runtime):
        self.runtime = runtime

    @staticmethod
    def _call_or_value(target: Any) -> Any:
        return target() if callable(target) else target

    def _resolve_doctor(self) -> Any:
        doctor = getattr(self.runtime, "doctor", None)

        if doctor is not None:
            report = getattr(doctor, "report", None)

            if report is not None:
                return self._call_or_value(report)

            return self._call_or_value(doctor)

        diagnostics = getattr(
            self.runtime,
            "diagnostics",
            None,
        )

        if diagnostics is not None:
            report = getattr(diagnostics, "report", None)

            if report is not None:
                return self._call_or_value(report)

            if callable(diagnostics):
                return diagnostics()

            health = getattr(diagnostics, "health", None)

            if health is not None:
                return self._call_or_value(health)

        raise RuntimeError(
            "Runtime doctor capability is unavailable."
        )

    def _resolve_invariants(self) -> Any:
        candidates = (
            "invariants",
            "runtime_invariants",
            "invariant_manager",
            "integrity_invariants",
        )

        for name in candidates:
            target = getattr(self.runtime, name, None)

            if target is None:
                continue

            validate = getattr(target, "validate", None)

            if validate is not None:
                return self._call_or_value(validate)

            report = getattr(target, "report", None)

            if report is not None:
                return self._call_or_value(report)

            return self._call_or_value(target)

        integrity = getattr(self.runtime, "integrity", None)

        if integrity is not None:
            invariants = getattr(
                integrity,
                "invariants",
                None,
            )

            if invariants is not None:
                validate = getattr(
                    invariants,
                    "validate",
                    None,
                )

                if validate is not None:
                    return self._call_or_value(validate)

                return self._call_or_value(invariants)

        architecture_validate = getattr(
            self.runtime,
            "architecture_validate",
            None,
        )

        if architecture_validate is not None:
            return self._call_or_value(
                architecture_validate
            )

        raise RuntimeError(
            "Runtime invariant capability is unavailable."
        )

    def _resolve_boot_validation(self) -> Any:
        candidates = (
            "boot_certification_validate",
            "boot_validate",
            "validate_boot",
        )

        for name in candidates:
            target = getattr(self.runtime, name, None)

            if target is not None:
                result = self._call_or_value(target)
                return self._normalize_boot_validation(
                    result
                )

        validator = getattr(
            self.runtime,
            "boot_validator",
            None,
        )

        if validator is not None:
            for method_name in (
                "validate",
                "report",
                "status",
            ):
                method = getattr(
                    validator,
                    method_name,
                    None,
                )

                if method is not None:
                    result = self._call_or_value(
                        method
                    )
                    return self._normalize_boot_validation(
                        result
                    )

        raise RuntimeError(
            "Runtime boot validation capability is unavailable."
        )

    @staticmethod
    def _normalize_boot_validation(
        result: Any,
    ) -> dict[str, Any]:
        if isinstance(result, dict):
            normalized = dict(result)

            if "status" not in normalized:
                healthy = normalized.get(
                    "healthy",
                    normalized.get(
                        "valid",
                        normalized.get(
                            "passed",
                            True,
                        ),
                    ),
                )

                normalized["status"] = (
                    "pass" if healthy else "fail"
                )

            return normalized

        if isinstance(result, bool):
            return {
                "status": (
                    "pass" if result else "fail"
                ),
                "valid": result,
            }

        return {
            "status": "pass",
            "result": result,
        }

    def selftest(self, context):
        context.add_result(
            "selftest",
            self.runtime.certify_runtime(),
        )
        return context

    def dashboard(self, context):
        context.add_result(
            "dashboard",
            {
                "health": self.runtime.health(),
                "registry": self.runtime.registry_snapshot(),
                "commands": self.runtime.commands.count(),
            },
        )
        return context

    def snapshot(self, context):
        context.add_result(
            "snapshot",
            self.runtime.runtime_readiness(),
        )
        return context

    def audit(self, context):
        context.add_result(
            "audit",
            {
                "health": self.runtime.health(),
                "registry": self.runtime.registry_snapshot(),
                "architecture": (
                    self.runtime.architecture_validate()
                ),
            },
        )
        return context

    def docs(self, context):
        context.add_result(
            "docs",
            self.runtime.generate_release_manifest(),
        )
        return context

    def doctor(self, context):
        context.add_result(
            "doctor",
            self._resolve_doctor(),
        )
        return context

    def invariants(self, context):
        context.add_result(
            "invariants",
            self._resolve_invariants(),
        )
        return context

    def boot_validate(self, context):
        context.add_result(
            "boot_validation",
            self._resolve_boot_validation(),
        )
        return context

    def health_report(self, context):
        context.add_result(
            "health_report",
            self.runtime.health(),
        )
        return context
'''

ADAPTER.write_text(
    ADAPTER_SOURCE,
    encoding="utf-8",
)


registration_text = REGISTRATIONS.read_text(
    encoding="utf-8"
)

if '"runtime.health_report"' not in registration_text:
    anchor = '''\
    runtime.commands.register_context_handler(
        "runtime.boot.validate",
        adapter.boot_validate,
        replace=True,
    )
'''

    addition = anchor + '''\

    runtime.commands.register_context_handler(
        "runtime.health_report",
        adapter.health_report,
        replace=True,
    )
'''

    if anchor not in registration_text:
        raise RuntimeError(
            "runtime.boot.validate registration block "
            "was not found."
        )

    registration_text = registration_text.replace(
        anchor,
        addition,
        1,
    )

REGISTRATIONS.write_text(
    registration_text,
    encoding="utf-8",
)

print("Runtime integrity command repair installed.")
print(f"Backup: {backup.relative_to(ROOT)}")
print(f"Updated: {ADAPTER.relative_to(ROOT)}")
print(f"Updated: {REGISTRATIONS.relative_to(ROOT)}")
