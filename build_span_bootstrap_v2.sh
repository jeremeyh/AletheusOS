#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${1:-$(pwd)}"
cd "$ROOT"

TARGET="aletheus/span/bootstrap.py"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_DIR="reports/span/backups/bootstrap_v2_${STAMP}"

required_files=(
  "aletheus/span/provider_registry.py"
  "aletheus/span/provider_loader.py"
  "aletheus/span/analyzer_registry.py"
  "aletheus/span/analyzer_loader.py"
  "aletheus/span/rule_registry.py"
  "aletheus/span/rule_loader.py"
  "aletheus/span/rule_engine.py"
  "aletheus/span/pipeline.py"
)

for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "ERROR: Required SPAN component is missing: $file"
        echo "Run this builder from the AletheusOS project root after Genesis 13.4."
        exit 1
    fi
done

mkdir -p "$BACKUP_DIR"

if [[ -f "$TARGET" ]]; then
    cp "$TARGET" "$BACKUP_DIR/bootstrap.py"
fi

if [[ -f "aletheus/span/__init__.py" ]]; then
    cp "aletheus/span/__init__.py" "$BACKUP_DIR/span___init__.py"
fi

cat > "$TARGET" <<'PY'
"""SPAN™ Bootstrap v2 — canonical subsystem composition root."""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from .analyzer_loader import AnalyzerLoader
from .analyzer_registry import AnalyzerRegistry
from .pipeline import SPANPipeline
from .provider_loader import ProviderLoader
from .provider_registry import ProviderRegistry
from .rule_engine import RuleEngine
from .rule_loader import RuleLoadReport, RuleLoader
from .rule_registry import RuleRegistry


class BootstrapState(str, Enum):
    """Lifecycle states for the SPAN composition root."""

    NEW = "new"
    INITIALIZING = "initializing"
    READY = "ready"
    DEGRADED = "degraded"
    FAILED = "failed"
    SHUTDOWN = "shutdown"


@dataclass(frozen=True, slots=True)
class BootstrapDiagnostic:
    """One structured bootstrap diagnostic."""

    level: str
    component: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "level": self.level,
            "component": self.component,
            "code": self.code,
            "message": self.message,
        }


@dataclass(slots=True)
class BootstrapReport:
    """Structured health report for one SPAN initialization."""

    state: BootstrapState = BootstrapState.NEW
    started_at: str | None = None
    completed_at: str | None = None

    providers: int = 0
    analyzers: int = 0
    rules: int = 0

    provider_loader: str = "not_started"
    analyzer_loader: str = "not_started"
    rule_loader: str = "not_started"
    rule_engine: str = "not_started"
    pipeline: str = "not_started"

    diagnostics: list[BootstrapDiagnostic] = field(default_factory=list)
    loader_reports: dict[str, Any] = field(default_factory=dict)

    @property
    def warnings(self) -> int:
        return sum(item.level == "warning" for item in self.diagnostics)

    @property
    def errors(self) -> int:
        return sum(item.level == "error" for item in self.diagnostics)

    @property
    def ok(self) -> bool:
        return self.state is BootstrapState.READY and self.errors == 0

    def add(
        self,
        level: str,
        component: str,
        code: str,
        message: str,
    ) -> None:
        self.diagnostics.append(
            BootstrapDiagnostic(
                level=level,
                component=component,
                code=code,
                message=message,
            )
        )

    def summary(self) -> dict[str, Any]:
        return {
            "state": self.state.value,
            "providers": self.providers,
            "analyzers": self.analyzers,
            "rules": self.rules,
            "provider_loader": self.provider_loader,
            "analyzer_loader": self.analyzer_loader,
            "rule_loader": self.rule_loader,
            "rule_engine": self.rule_engine,
            "pipeline": self.pipeline,
            "warnings": self.warnings,
            "errors": self.errors,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "diagnostics": [
                diagnostic.to_dict()
                for diagnostic in self.diagnostics
            ],
            "loader_reports": dict(self.loader_reports),
        }


class SPANBootstrap:
    """
    Canonical SPAN subsystem composition root.

    The bootstrap owns construction and lifecycle for:

    - ProviderRegistry and ProviderLoader
    - AnalyzerRegistry and AnalyzerLoader
    - RuleRegistry and RuleLoader
    - RuleEngine
    - SPANPipeline
    """

    def __init__(
        self,
        *,
        provider_package: str | None = None,
        analyzer_package: str | None = None,
        rule_package: str = "aletheus.span.rules",
        strict: bool = False,
    ) -> None:
        self.provider_package = provider_package
        self.analyzer_package = analyzer_package
        self.rule_package = rule_package
        self.strict = bool(strict)

        self.state = BootstrapState.NEW
        self._report = BootstrapReport()

        self.provider_registry: ProviderRegistry | None = None
        self.provider_loader: ProviderLoader | None = None

        self.analyzer_registry: AnalyzerRegistry | None = None
        self.analyzer_loader: AnalyzerLoader | None = None

        self.rule_registry: RuleRegistry | None = None
        self.rule_loader: RuleLoader | None = None
        self.rule_engine: RuleEngine | None = None

        self.pipeline: SPANPipeline | None = None

    @property
    def initialized(self) -> bool:
        return self.state in {
            BootstrapState.READY,
            BootstrapState.DEGRADED,
        }

    @property
    def report(self) -> BootstrapReport:
        return self._report

    def initialize(self, *, force: bool = False) -> BootstrapReport:
        """Build the complete SPAN subsystem and return its health report."""

        if self.initialized and not force:
            return self._report

        self.state = BootstrapState.INITIALIZING
        self._report = BootstrapReport(
            state=self.state,
            started_at=self._timestamp(),
        )

        try:
            self._initialize_providers()
            self._initialize_analyzers()
            self._initialize_rules()
            self._build_rule_engine()
            self._build_pipeline()
            self._finalize_state()
        except Exception as exc:
            self.state = BootstrapState.FAILED
            self._report.state = self.state
            self._report.add(
                "error",
                "bootstrap",
                "initialization_failed",
                f"{type(exc).__name__}: {exc}",
            )
            self._report.completed_at = self._timestamp()

            if self.strict:
                raise

        return self._report

    def shutdown(self) -> None:
        """Release composed references and transition to SHUTDOWN."""

        self.pipeline = None
        self.rule_engine = None
        self.rule_loader = None
        self.rule_registry = None
        self.analyzer_loader = None
        self.analyzer_registry = None
        self.provider_loader = None
        self.provider_registry = None

        self.state = BootstrapState.SHUTDOWN
        self._report.state = self.state
        self._report.completed_at = self._timestamp()

    def health(self) -> dict[str, Any]:
        """Return a serializable snapshot of SPAN startup health."""

        return self._report.to_dict()

    def require_ready(self) -> "SPANBootstrap":
        """Raise unless all required SPAN runtime components are ready."""

        if self.state is not BootstrapState.READY:
            raise RuntimeError(
                "SPAN is not ready; current state is "
                f"{self.state.value!r}. Report: {self._report.summary()}"
            )
        return self

    def _initialize_providers(self) -> None:
        self.provider_registry = ProviderRegistry()
        self.provider_loader = self._construct_loader(
            ProviderLoader,
            self.provider_registry,
            self.provider_package,
        )

        status, loader_report = self._run_loader(
            self.provider_loader,
            component="providers",
        )

        self._report.provider_loader = status
        self._report.providers = self._safe_len(self.provider_registry)

        if loader_report is not None:
            self._report.loader_reports["providers"] = loader_report

    def _initialize_analyzers(self) -> None:
        self.analyzer_registry = AnalyzerRegistry()
        self.analyzer_loader = self._construct_loader(
            AnalyzerLoader,
            self.analyzer_registry,
            self.analyzer_package,
        )

        status, loader_report = self._run_loader(
            self.analyzer_loader,
            component="analyzers",
        )

        self._report.analyzer_loader = status
        self._report.analyzers = self._safe_len(self.analyzer_registry)

        if loader_report is not None:
            self._report.loader_reports["analyzers"] = loader_report

    def _initialize_rules(self) -> None:
        self.rule_registry = RuleRegistry()
        self.rule_loader = RuleLoader(
            self.rule_registry,
            package=self.rule_package,
        )

        try:
            load_report: RuleLoadReport = self.rule_loader.load_all(
                strict=self.strict
            )
        except Exception as exc:
            self._report.rule_loader = "failed"
            self._report.add(
                "error",
                "rules",
                "loader_failed",
                f"{type(exc).__name__}: {exc}",
            )
            if self.strict:
                raise
        else:
            self._report.loader_reports["rules"] = load_report.to_dict()
            self._report.rule_loader = (
                "ready" if load_report.ok else "degraded"
            )

            for diagnostic in load_report.diagnostics:
                if diagnostic.level in {"warning", "error"}:
                    self._report.add(
                        diagnostic.level,
                        "rules",
                        diagnostic.code,
                        diagnostic.message,
                    )

        self._report.rules = self._safe_len(self.rule_registry)

    def _build_rule_engine(self) -> None:
        if self.rule_registry is None:
            raise RuntimeError("rule registry is unavailable")

        self.rule_engine = self.rule_registry.build_engine()
        self._report.rule_engine = "ready"

    def _build_pipeline(self) -> None:
        context = {
            "provider_registry": self.provider_registry,
            "providers": self.provider_registry,
            "analyzer_registry": self.analyzer_registry,
            "analyzers": self.analyzer_registry,
            "rule_registry": self.rule_registry,
            "rules": self.rule_registry,
            "rule_engine": self.rule_engine,
            "engine": self.rule_engine,
        }

        try:
            self.pipeline = self._construct_component(
                SPANPipeline,
                context,
            )
        except Exception as exc:
            self._report.pipeline = "failed"
            self._report.add(
                "error",
                "pipeline",
                "construction_failed",
                f"{type(exc).__name__}: {exc}",
            )
            if self.strict:
                raise
        else:
            self._report.pipeline = "ready"

    def _finalize_state(self) -> None:
        required_ready = (
            self.provider_registry is not None
            and self.analyzer_registry is not None
            and self.rule_registry is not None
            and self.rule_engine is not None
            and self.pipeline is not None
        )

        if self._report.errors:
            self.state = (
                BootstrapState.FAILED
                if not required_ready
                else BootstrapState.DEGRADED
            )
        elif self._report.warnings:
            self.state = BootstrapState.DEGRADED
        elif required_ready:
            self.state = BootstrapState.READY
        else:
            self.state = BootstrapState.FAILED

        self._report.state = self.state
        self._report.completed_at = self._timestamp()

        if self.strict and self.state is not BootstrapState.READY:
            raise RuntimeError(
                "Strict SPAN bootstrap did not reach READY: "
                f"{self._report.summary()}"
            )

    @classmethod
    def _construct_loader(
        cls,
        loader_type: type[Any],
        registry: Any,
        package: str | None,
    ) -> Any:
        context = {
            "registry": registry,
            "provider_registry": registry,
            "analyzer_registry": registry,
        }

        if package:
            context.update(
                {
                    "package": package,
                    "package_name": package,
                    "namespace": package,
                }
            )

        try:
            return cls._construct_component(loader_type, context)
        except TypeError:
            if package is not None:
                try:
                    return loader_type(registry, package)
                except TypeError:
                    pass
            return loader_type(registry)

    def _run_loader(
        self,
        loader: Any,
        *,
        component: str,
    ) -> tuple[str, Any | None]:
        methods = (
            "load_all",
            "load",
            "discover_and_register",
            "initialize",
            "bootstrap",
        )

        for method_name in methods:
            method = getattr(loader, method_name, None)
            if not callable(method):
                continue

            try:
                result = self._invoke_compatible(method)
            except Exception as exc:
                self._report.add(
                    "error",
                    component,
                    "loader_execution_failed",
                    f"{method_name}: {type(exc).__name__}: {exc}",
                )
                if self.strict:
                    raise
                return "failed", None

            normalized = self._normalize_report(result)

            if self._report_indicates_errors(result):
                self._report.add(
                    "error",
                    component,
                    "loader_reported_errors",
                    f"{method_name} completed with reported errors.",
                )
                return "degraded", normalized

            return "ready", normalized

        self._report.add(
            "warning",
            component,
            "loader_method_missing",
            "Loader exposes no recognized execution method; "
            "registry was still created.",
        )
        return "degraded", None

    @staticmethod
    def _invoke_compatible(method: Any) -> Any:
        signature = inspect.signature(method)
        kwargs: dict[str, Any] = {}

        for name, parameter in signature.parameters.items():
            if name == "strict":
                kwargs[name] = False
            elif (
                parameter.default is inspect.Parameter.empty
                and parameter.kind
                in {
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                }
            ):
                raise TypeError(
                    f"Unsupported required loader parameter: {name}"
                )

        return method(**kwargs)

    @staticmethod
    def _construct_component(
        component_type: type[Any],
        context: dict[str, Any],
    ) -> Any:
        signature = inspect.signature(component_type)
        args: list[Any] = []
        kwargs: dict[str, Any] = {}

        for name, parameter in signature.parameters.items():
            if name in {"self", "cls"}:
                continue

            value = context.get(name)

            if value is not None:
                if parameter.kind is inspect.Parameter.POSITIONAL_ONLY:
                    args.append(value)
                else:
                    kwargs[name] = value
                continue

            if parameter.default is not inspect.Parameter.empty:
                continue

            if parameter.kind in {
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            }:
                continue

            raise TypeError(
                f"Cannot resolve required constructor parameter "
                f"{component_type.__name__}.{name}"
            )

        return component_type(*args, **kwargs)

    @staticmethod
    def _normalize_report(value: Any) -> Any:
        if value is None:
            return None

        to_dict = getattr(value, "to_dict", None)
        if callable(to_dict):
            return to_dict()

        summary = getattr(value, "summary", None)
        if callable(summary):
            return summary()

        if isinstance(value, (str, int, float, bool, list, tuple, dict)):
            return value

        return repr(value)

    @staticmethod
    def _report_indicates_errors(value: Any) -> bool:
        if value is None:
            return False

        error_count = getattr(value, "error_count", None)
        if isinstance(error_count, int):
            return error_count > 0

        errors = getattr(value, "errors", None)
        if isinstance(errors, int):
            return errors > 0
        if isinstance(errors, (list, tuple, set, dict)):
            return bool(errors)

        ok = getattr(value, "ok", None)
        if isinstance(ok, bool):
            return not ok

        if isinstance(value, dict):
            if isinstance(value.get("errors"), int):
                return value["errors"] > 0
            if isinstance(value.get("ok"), bool):
                return not value["ok"]

        return False

    @staticmethod
    def _safe_len(value: Any) -> int:
        if value is None:
            return 0

        try:
            return len(value)
        except TypeError:
            pass

        for method_name in ("list", "all", "values", "items"):
            method = getattr(value, method_name, None)
            if callable(method):
                try:
                    return len(tuple(method()))
                except Exception:
                    continue

        return 0

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(timezone.utc).isoformat()


def bootstrap_span(
    *,
    strict: bool = False,
    provider_package: str | None = None,
    analyzer_package: str | None = None,
    rule_package: str = "aletheus.span.rules",
) -> SPANBootstrap:
    """Create and initialize a SPANBootstrap in one call."""

    bootstrap = SPANBootstrap(
        provider_package=provider_package,
        analyzer_package=analyzer_package,
        rule_package=rule_package,
        strict=strict,
    )
    bootstrap.initialize()
    return bootstrap
PY

echo
echo "Compiling SPAN Bootstrap v2..."

python -m py_compile \
    aletheus/span/bootstrap.py \
    aletheus/span/provider_registry.py \
    aletheus/span/provider_loader.py \
    aletheus/span/analyzer_registry.py \
    aletheus/span/analyzer_loader.py \
    aletheus/span/rule_registry.py \
    aletheus/span/rule_loader.py \
    aletheus/span/rule_engine.py \
    aletheus/span/pipeline.py

echo
echo "Checking package exports..."

python - <<'PY'
from pathlib import Path

path = Path("aletheus/span/__init__.py")
text = path.read_text() if path.exists() else ""

exports = """
from .bootstrap import (
    BootstrapDiagnostic,
    BootstrapReport,
    BootstrapState,
    SPANBootstrap,
    bootstrap_span,
)
""".strip()

if "from .bootstrap import (" not in text:
    separator = "\n\n" if text.strip() else ""
    path.write_text(text.rstrip() + separator + exports + "\n")
PY

python -m py_compile aletheus/span/__init__.py

echo
echo "Running Genesis 13.5 composition validation..."

python - <<'PY'
from aletheus.span.bootstrap import (
    BootstrapReport,
    BootstrapState,
    SPANBootstrap,
    bootstrap_span,
)


bootstrap = SPANBootstrap(strict=False)
report = bootstrap.initialize()

assert isinstance(report, BootstrapReport)
assert bootstrap.provider_registry is not None
assert bootstrap.provider_loader is not None
assert bootstrap.analyzer_registry is not None
assert bootstrap.analyzer_loader is not None
assert bootstrap.rule_registry is not None
assert bootstrap.rule_loader is not None
assert bootstrap.rule_engine is not None
assert bootstrap.pipeline is not None

assert report.provider_loader in {"ready", "degraded"}
assert report.analyzer_loader in {"ready", "degraded"}
assert report.rule_loader in {"ready", "degraded"}
assert report.rule_engine == "ready"
assert report.pipeline == "ready"

assert bootstrap.state in {
    BootstrapState.READY,
    BootstrapState.DEGRADED,
}
assert bootstrap.initialized

same_report = bootstrap.initialize()
assert same_report is report

health = bootstrap.health()
assert health["summary"]["pipeline"] == "ready"
assert health["summary"]["rule_engine"] == "ready"

one_call = bootstrap_span(strict=False)
assert one_call.initialized
assert one_call.pipeline is not None
assert one_call.rule_engine is not None

one_call.shutdown()
assert one_call.state is BootstrapState.SHUTDOWN
assert one_call.pipeline is None
assert one_call.rule_engine is None

print("SPANBootstrap import: OK")
print("Provider composition: OK")
print("Analyzer composition: OK")
print("Rule composition: OK")
print("RuleEngine composition: OK")
print("Pipeline composition: OK")
print("Idempotent initialize: OK")
print("Health reporting: OK")
print("One-call bootstrap: OK")
print("Shutdown lifecycle: OK")
print("Bootstrap state:", bootstrap.state.value)
print("Bootstrap summary:", report.summary())

if report.diagnostics:
    print("Diagnostics:")
    for diagnostic in report.diagnostics:
        print(
            f"  [{diagnostic.level}] "
            f"{diagnostic.component}/{diagnostic.code}: "
            f"{diagnostic.message}"
        )
PY

echo
echo "Running existing SPAN integration validation..."

INTEGRATION_LOG="$(mktemp)"
trap 'rm -f "$INTEGRATION_LOG"' EXIT

if ! bash tools/build/build_span_integration.sh \
    >"$INTEGRATION_LOG" 2>&1; then
    cat "$INTEGRATION_LOG"
    echo
    echo "ERROR: Existing SPAN integration command failed."
    exit 1
fi

cat "$INTEGRATION_LOG"

if grep -q "SPAN analyzer failed" "$INTEGRATION_LOG"; then
    echo
    echo "ERROR: Existing integration reported analyzer failures."
    exit 1
fi

if grep -qE "Traceback|TypeError|ImportError|ModuleNotFoundError" \
    "$INTEGRATION_LOG"; then
    echo
    echo "ERROR: Existing integration emitted a Python failure."
    exit 1
fi

echo
echo "Verifying canonical public contracts..."

grep -nE \
    'class BootstrapState|class BootstrapReport|class SPANBootstrap|def initialize|def shutdown|def bootstrap_span' \
    "$TARGET"

echo
echo "=============================================="
echo "Genesis 13.5 SPAN Bootstrap v2"
echo "Installed and fully validated successfully."
echo "=============================================="
echo
echo "Created:"
echo "  $TARGET"
echo
echo "Updated:"
echo "  aletheus/span/__init__.py"
echo
echo "Backup:"
echo "  $BACKUP_DIR"
