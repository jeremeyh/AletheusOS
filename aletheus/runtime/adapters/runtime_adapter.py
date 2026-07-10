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
        health = self.runtime.runtime_facade.health()

        passed = bool(
            health.get("booted", False)
            and health.get("status") in {
                "healthy",
                "online",
            }
        )

        context.add_result(
            "selftest",
            {
                "status": (
                    "pass" if passed else "fail"
                ),
                "health": health,
                "commands": self.runtime.commands.count(),
            },
        )

        return context


    def dashboard(self, context):
        health = self.runtime.runtime_facade.health()

        context.add_result(
            "dashboard",
            {
                "health": (
                    "pass"
                    if health.get("status")
                    in {"healthy", "online"}
                    else "fail"
                ),
                "runtime": health,
                "registry": self.runtime.registry_snapshot(),
                "commands": self.runtime.commands.count(),
            },
        )

        return context


    def snapshot(self, context):
        compatibility = {}

        compat = getattr(
            self.runtime,
            "compat",
            None,
        )

        if compat is not None:
            statistics = getattr(
                compat,
                "statistics",
                None,
            )

            if callable(statistics):
                compatibility = statistics()

        kernel = getattr(
            self.runtime,
            "kernel_v2",
            getattr(
                self.runtime,
                "kernel",
                None,
            ),
        )

        kernel_snapshot = {}

        if kernel is not None:
            snapshot_method = getattr(
                kernel,
                "snapshot",
                None,
            )

            if callable(snapshot_method):
                try:
                    kernel_snapshot = snapshot_method()
                except TypeError:
                    kernel_snapshot = {
                        "version": getattr(
                            kernel,
                            "version",
                            "unknown",
                        ),
                        "status": "online",
                    }
            else:
                kernel_snapshot = {
                    "version": getattr(
                        kernel,
                        "version",
                        "unknown",
                    ),
                    "status": "online",
                }

        context.add_result(
            "snapshot",
            {
                "commands": {
                    "count": self.runtime.commands.count(),
                },
                "compatibility": compatibility,
                "kernel": kernel_snapshot,
                "registry": self.runtime.registry_snapshot(),
                "runtime": self.runtime.runtime_facade.health(),
            },
        )

        return context


    def audit(self, context):
        health = self.runtime.runtime_facade.health()

        registry = self.runtime.registry_snapshot()

        compatibility = {}

        compat = getattr(
            self.runtime,
            "compat",
            None,
        )

        if compat is not None:
            statistics = getattr(
                compat,
                "statistics",
                None,
            )

            if callable(statistics):
                compatibility = statistics()

        status = (
            "healthy"
            if health.get("booted", False)
            else "warning"
        )

        context.add_result(
            "audit",
            {
                "health": status,
                "runtime": health,
                "registry": registry,
                "compatibility": compatibility,
                "command_count": self.runtime.commands.count(),
            },
        )

        return context


    def docs(self, context):
        from pathlib import Path

        payload = context.payload or {}

        output_path = Path(
            payload.get(
                "path",
                "RUNTIME_DOCUMENTATION.md",
            )
        )

        health = self.runtime.runtime_facade.health()
        registry = self.runtime.registry_snapshot()

        content = (
            "# AletheusOS Runtime Documentation\n\n"
            f"- Version: `{health.get('version', 'unknown')}`\n"
            f"- Status: `{health.get('status', 'unknown')}`\n"
            f"- Booted: `{health.get('booted', False)}`\n"
            f"- Commands: `{self.runtime.commands.count()}`\n"
            f"- Registry entries: `{len(registry) if hasattr(registry, '__len__') else 0}`\n"
        )

        output_path.write_text(
            content,
            encoding="utf-8",
        )

        documentation = {
            "status": "written",
            "path": str(output_path),
            "bytes": len(
                content.encode("utf-8")
            ),
        }

        context.add_result(
            "documentation",
            documentation,
        )
        context.add_result(
            "docs",
            documentation,
        )

        return context

    def doctor(self, context):
        result = self._resolve_doctor()

        if isinstance(result, dict):
            result = dict(result)

            status = result.get("status")

            if status in {
                "healthy",
                "online",
                "ok",
                "passed",
                True,
            }:
                result["status"] = "pass"

            elif status in {
                "unhealthy",
                "offline",
                "failed",
                False,
            }:
                result["status"] = "fail"

        context.add_result(
            "doctor",
            result,
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
        runtime_doctor = getattr(
            self.runtime,
            "runtime_doctor",
            None,
        )

        if runtime_doctor is None:
            raise RuntimeError(
                "Runtime health report writer is unavailable."
            )

        write_reports = getattr(
            runtime_doctor,
            "write_reports",
            None,
        )

        if not callable(write_reports):
            raise RuntimeError(
                "Runtime health report writer does not expose "
                "write_reports()."
            )

        report = write_reports()

        context.add_result(
            "health_report",
            report,
        )
        return context
