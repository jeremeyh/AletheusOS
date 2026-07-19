from __future__ import annotations

from dataclasses import dataclass, field
import importlib
import inspect
import pkgutil
from types import ModuleType
from typing import Iterable, Sequence

from .analyzer import Analyzer
from .analyzer_registry import AnalyzerRegistry


@dataclass(frozen=True, slots=True)
class AnalyzerLoadDiagnostic:
    module: str
    component: str | None
    status: str
    message: str = ""


@dataclass(slots=True)
class AnalyzerLoadResult:
    registry: AnalyzerRegistry
    diagnostics: list[AnalyzerLoadDiagnostic] = field(default_factory=list)

    @property
    def loaded_count(self) -> int:
        return sum(d.status == "loaded" for d in self.diagnostics)

    @property
    def skipped_count(self) -> int:
        return sum(d.status == "skipped" for d in self.diagnostics)

    @property
    def failed_count(self) -> int:
        return sum(d.status == "failed" for d in self.diagnostics)


class AnalyzerLoader:
    def __init__(
        self,
        *,
        package: str = "aletheus.span.analyzers",
        excluded_modules: Iterable[str] = ("base",),
        fail_fast: bool = False,
    ) -> None:
        self.package = package
        self.excluded_modules = frozenset(excluded_modules)
        self.fail_fast = fail_fast

    def discover_modules(self) -> tuple[str, ...]:
        package = importlib.import_module(self.package)
        modules = []
        for info in pkgutil.iter_modules(package.__path__):
            if info.ispkg or info.name.startswith("_") or info.name in self.excluded_modules:
                continue
            modules.append(f"{self.package}.{info.name}")
        return tuple(sorted(modules))

    def load(self, *, registry: AnalyzerRegistry | None = None,
             modules: Sequence[str] | None = None) -> AnalyzerLoadResult:
        registry = registry or AnalyzerRegistry()
        diagnostics: list[AnalyzerLoadDiagnostic] = []

        for module_name in (tuple(modules) if modules else self.discover_modules()):
            try:
                module = importlib.import_module(module_name)
            except Exception as exc:
                diagnostics.append(AnalyzerLoadDiagnostic(module_name, None, "failed", str(exc)))
                if self.fail_fast:
                    raise
                continue

            diagnostics.extend(self._load_module(module, registry))

        return AnalyzerLoadResult(registry=registry, diagnostics=diagnostics)

    def load_registry(self) -> AnalyzerRegistry:
        return self.load().registry

    def _load_module(self, module: ModuleType, registry: AnalyzerRegistry):
        out = []
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if cls is Analyzer or cls.__module__ != module.__name__:
                continue
            if not issubclass(cls, Analyzer):
                continue
            if inspect.isabstract(cls):
                out.append(AnalyzerLoadDiagnostic(module.__name__, cls.__name__, "skipped", "abstract"))
                continue
            sig = inspect.signature(cls)
            req = [p for p in sig.parameters.values()
                   if p.default is inspect.Parameter.empty
                   and p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)]
            if req:
                out.append(AnalyzerLoadDiagnostic(module.__name__, cls.__name__, "skipped", "constructor requires arguments"))
                continue
            try:
                inst = cls()
                registry.register(inst, name=getattr(inst, "name", cls.__name__))
                out.append(AnalyzerLoadDiagnostic(module.__name__, cls.__name__, "loaded", ""))
            except Exception as exc:
                out.append(AnalyzerLoadDiagnostic(module.__name__, cls.__name__, "failed", str(exc)))
                if self.fail_fast:
                    raise
        return out
