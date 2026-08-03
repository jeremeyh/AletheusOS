from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

from aletheus.span.evidence_store import EvidenceStore
from aletheus.span.provider_registry import ProviderRegistry
from aletheus.span.providers.base import ProviderContext, ProviderResult


@dataclass(frozen=True)
class ProviderExecutionError:
    provider: str
    error_type: str
    message: str


@dataclass(frozen=True)
class ProviderExecutionResult:
    run_id: str
    root: str
    providers_attempted: int
    providers_succeeded: int
    evidence_records: int
    provider_results: tuple[ProviderResult, ...] = ()
    errors: tuple[ProviderExecutionError, ...] = ()

    @property
    def succeeded(self) -> bool:
        return not self.errors


class ProviderExecutor:
    """Execute registered SPAN providers against a canonical context."""

    def __init__(
        self,
        registry: ProviderRegistry | None = None,
        evidence_store: EvidenceStore | None = None,
        *,
        fail_fast: bool = False,
    ) -> None:
        self.registry = registry or ProviderRegistry.default()
        self.evidence_store = evidence_store or EvidenceStore()
        self.fail_fast = fail_fast

    def execute(
        self,
        root: str | Path = ".",
        *,
        run_id: str | None = None,
        configuration: Mapping[str, Any] | None = None,
    ) -> ProviderExecutionResult:
        resolved_root = Path(root).expanduser().resolve()
        actual_run_id = run_id or f"span-{uuid4().hex}"

        context = ProviderContext(
            root=resolved_root,
            run_id=actual_run_id,
            configuration=dict(configuration or {}),
        )

        provider_results: list[ProviderResult] = []
        errors: list[ProviderExecutionError] = []
        providers = self.registry.providers()

        for provider in providers:
            try:
                result = provider.run(context)
                self.evidence_store.extend(result.records)
                provider_results.append(result)
            except Exception as exc:
                errors.append(
                    ProviderExecutionError(
                        provider=getattr(provider, "name", provider.__class__.__name__),
                        error_type=exc.__class__.__name__,
                        message=str(exc),
                    )
                )
                if self.fail_fast:
                    raise

        return ProviderExecutionResult(
            run_id=actual_run_id,
            root=str(resolved_root),
            providers_attempted=len(providers),
            providers_succeeded=len(provider_results),
            evidence_records=self.evidence_store.summary()["total_records"],
            provider_results=tuple(provider_results),
            errors=tuple(errors),
        )
