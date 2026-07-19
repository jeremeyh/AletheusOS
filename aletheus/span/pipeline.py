"""Composable SPAN™ evidence and analysis pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging
from pathlib import Path
from typing import Any, Iterable, Mapping
from uuid import uuid4

from .analyzer import Analyzer, AnalyzerContext, AnalyzerResult
from .evidence_store import EvidenceStore
from .finding import Finding, FindingSet
from .providers.base import Provider, ProviderContext, ProviderResult

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Complete result of one SPAN provider/analyzer pipeline run."""

    run_id: str
    root: str
    started_at: datetime
    completed_at: datetime
    evidence: EvidenceStore
    provider_results: tuple[ProviderResult, ...]
    analyzer_results: tuple[AnalyzerResult, ...]
    findings: tuple[Finding, ...]
    errors: tuple[Mapping[str, Any], ...] = ()

    @property
    def duration_ms(self) -> float:
        return round((self.completed_at - self.started_at).total_seconds() * 1000, 3)

    def to_dict(self, *, include_evidence: bool = False) -> dict[str, Any]:
        payload = {
            "run_id": self.run_id,
            "root": self.root,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat(),
            "duration_ms": self.duration_ms,
            "evidence_summary": self.evidence.summary(),
            "provider_results": [result.to_dict() for result in self.provider_results],
            "analyzer_results": [result.to_dict() for result in self.analyzer_results],
            "findings": [finding.to_dict() for finding in self.findings],
            "errors": [dict(error) for error in self.errors],
        }
        if include_evidence:
            payload["evidence"] = self.evidence.to_dict()["records"]
        return payload


@dataclass(slots=True)
class SPANPipeline:
    """Orchestrates providers, evidence storage, and analyzers."""

    providers: list[Provider] = field(default_factory=list)
    analyzers: list[Analyzer] = field(default_factory=list)
    fail_fast: bool = False

    def add_provider(self, provider: Provider) -> None:
        if any(existing.name == provider.name for existing in self.providers):
            raise ValueError(f"provider already registered: {provider.name}")
        self.providers.append(provider)

    def add_analyzer(self, analyzer: Analyzer) -> None:
        if any(existing.name == analyzer.name for existing in self.analyzers):
            raise ValueError(f"analyzer already registered: {analyzer.name}")
        self.analyzers.append(analyzer)

    def run(
        self,
        root: str | Path,
        *,
        configuration: Mapping[str, Any] | None = None,
        graph: Any | None = None,
    ) -> PipelineResult:
        started = datetime.now(timezone.utc)
        run_id = f"span-{uuid4().hex}"
        resolved_root = Path(root).resolve()
        config = dict(configuration or {})
        evidence = EvidenceStore()
        provider_results: list[ProviderResult] = []
        analyzer_results: list[AnalyzerResult] = []
        findings = FindingSet()
        errors: list[Mapping[str, Any]] = []

        provider_context = ProviderContext(
            root=resolved_root,
            run_id=run_id,
            configuration=config,
        )

        for provider in self.providers:
            try:
                LOGGER.info("Running SPAN provider: %s", provider.name)
                result = provider.run(provider_context)
                evidence.extend(result.records)
                provider_results.append(result)
            except Exception as exc:
                error = {
                    "stage": "provider",
                    "component": provider.name,
                    "error_type": exc.__class__.__name__,
                    "message": str(exc),
                }
                errors.append(error)
                LOGGER.exception("SPAN provider failed: %s", provider.name)
                if self.fail_fast:
                    raise

        analyzer_context = AnalyzerContext(
            root=str(resolved_root),
            run_id=run_id,
            graph=graph,
            configuration=config,
        )

        for analyzer in self.analyzers:
            try:
                LOGGER.info("Running SPAN analyzer: %s", analyzer.name)
                result = analyzer.run(evidence, analyzer_context)
                analyzer_results.append(result)
                findings.extend(result.findings)
            except Exception as exc:
                error = {
                    "stage": "analyzer",
                    "component": analyzer.name,
                    "error_type": exc.__class__.__name__,
                    "message": str(exc),
                }
                errors.append(error)
                LOGGER.exception("SPAN analyzer failed: %s", analyzer.name)
                if self.fail_fast:
                    raise

        completed = datetime.now(timezone.utc)
        return PipelineResult(
            run_id=run_id,
            root=str(resolved_root),
            started_at=started,
            completed_at=completed,
            evidence=evidence,
            provider_results=tuple(provider_results),
            analyzer_results=tuple(analyzer_results),
            findings=tuple(findings.findings),
            errors=tuple(errors),
        )


def default_providers() -> tuple[Provider, ...]:
    """Create the canonical Genesis 11.1 provider set."""

    from .providers import (
        ASTProvider,
        ConfigurationProvider,
        FilesystemProvider,
        GitProvider,
        ImportProvider,
        RegistryProvider,
        RuntimeProvider,
    )

    return (
        FilesystemProvider(),
        ASTProvider(),
        ImportProvider(),
        ConfigurationProvider(),
        GitProvider(),
        RuntimeProvider(),
        RegistryProvider(),
    )
