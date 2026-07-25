"""Discovery and loading of SPAN™ evidence providers."""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from types import ModuleType

from .provider_registry import ProviderRegistry
from .providers.base import Provider


@dataclass(frozen=True, slots=True)
class ProviderLoadDiagnostic:
    """One provider discovery or loading diagnostic."""

    module: str
    component: str | None
    status: str
    message: str = ""

    def to_dict(self) -> dict[str, str | None]:
        return {
            "module": self.module,
            "component": self.component,
            "status": self.status,
            "message": self.message,
        }


@dataclass(slots=True)
class ProviderLoadResult:
    """Result envelope for one provider discovery pass."""

    registry: ProviderRegistry
    diagnostics: list[ProviderLoadDiagnostic] = field(default_factory=list)

    @property
    def loaded_count(self) -> int:
        return sum(item.status == "loaded" for item in self.diagnostics)

    @property
    def skipped_count(self) -> int:
        return sum(item.status == "skipped" for item in self.diagnostics)

    @property
    def failed_count(self) -> int:
        return sum(item.status == "failed" for item in self.diagnostics)

    @property
    def succeeded(self) -> bool:
        return self.failed_count == 0

    def to_dict(self) -> dict[str, object]:
        return {
            "loaded_count": self.loaded_count,
            "skipped_count": self.skipped_count,
            "failed_count": self.failed_count,
            "providers": list(self.registry.list()),
            "diagnostics": [item.to_dict() for item in self.diagnostics],
        }


class ProviderLoader:
    """Discover concrete, zero-argument Provider implementations."""

    def __init__(
        self,
        *,
        package: str = "aletheus.span.providers",
        excluded_modules: Iterable[str] = ("base",),
        fail_fast: bool = False,
    ) -> None:
        self.package = package
        self.excluded_modules = frozenset(excluded_modules)
        self.fail_fast = fail_fast

    def discover_modules(self) -> tuple[str, ...]:
        """Return importable provider module names in deterministic order."""

        package = importlib.import_module(self.package)
        package_path = getattr(package, "__path__", None)
        if package_path is None:
            raise TypeError(f"Provider package has no __path__: {self.package}")

        modules = []
        for info in pkgutil.iter_modules(package_path):
            if info.ispkg or info.name.startswith("_"):
                continue
            if info.name in self.excluded_modules:
                continue
            modules.append(f"{self.package}.{info.name}")

        return tuple(sorted(modules))

    def load(
        self,
        *,
        registry: ProviderRegistry | None = None,
        modules: Sequence[str] | None = None,
    ) -> ProviderLoadResult:
        """Discover providers, instantiate them, and register by provider name."""

        target_registry = registry or ProviderRegistry()
        diagnostics: list[ProviderLoadDiagnostic] = []
        module_names = tuple(modules) if modules is not None else self.discover_modules()

        for module_name in module_names:
            try:
                module = importlib.import_module(module_name)
            except Exception as exc:
                diagnostics.append(
                    ProviderLoadDiagnostic(
                        module=module_name,
                        component=None,
                        status="failed",
                        message=f"{exc.__class__.__name__}: {exc}",
                    )
                )
                if self.fail_fast:
                    raise
                continue

            diagnostics.extend(self._load_module(module, target_registry))

        return ProviderLoadResult(
            registry=target_registry,
            diagnostics=diagnostics,
        )

    def load_registry(
        self,
        *,
        registry: ProviderRegistry | None = None,
        modules: Sequence[str] | None = None,
    ) -> ProviderRegistry:
        """Convenience method returning only the populated registry."""

        return self.load(registry=registry, modules=modules).registry

    def _load_module(
        self,
        module: ModuleType,
        registry: ProviderRegistry,
    ) -> list[ProviderLoadDiagnostic]:
        diagnostics: list[ProviderLoadDiagnostic] = []

        for _, provider_type in inspect.getmembers(module, inspect.isclass):
            if provider_type is Provider:
                continue
            if provider_type.__module__ != module.__name__:
                continue
            if not issubclass(provider_type, Provider):
                continue
            if inspect.isabstract(provider_type):
                diagnostics.append(
                    ProviderLoadDiagnostic(
                        module=module.__name__,
                        component=provider_type.__name__,
                        status="skipped",
                        message="abstract provider",
                    )
                )
                continue

            try:
                signature = inspect.signature(provider_type)
            except (TypeError, ValueError):
                signature = None

            if signature is not None:
                required = [
                    parameter
                    for parameter in signature.parameters.values()
                    if parameter.default is inspect.Parameter.empty
                    and parameter.kind
                    not in (
                        inspect.Parameter.VAR_POSITIONAL,
                        inspect.Parameter.VAR_KEYWORD,
                    )
                ]
                if required:
                    diagnostics.append(
                        ProviderLoadDiagnostic(
                            module=module.__name__,
                            component=provider_type.__name__,
                            status="skipped",
                            message="constructor requires arguments",
                        )
                    )
                    continue

            try:
                provider = provider_type()
                key = provider.name
                registry.register(provider, name=key)
            except ValueError as exc:
                diagnostics.append(
                    ProviderLoadDiagnostic(
                        module=module.__name__,
                        component=provider_type.__name__,
                        status="skipped",
                        message=str(exc),
                    )
                )
                continue
            except Exception as exc:
                diagnostics.append(
                    ProviderLoadDiagnostic(
                        module=module.__name__,
                        component=provider_type.__name__,
                        status="failed",
                        message=f"{exc.__class__.__name__}: {exc}",
                    )
                )
                if self.fail_fast:
                    raise
                continue

            diagnostics.append(
                ProviderLoadDiagnostic(
                    module=module.__name__,
                    component=provider_type.__name__,
                    status="loaded",
                    message=key,
                )
            )

        return diagnostics
