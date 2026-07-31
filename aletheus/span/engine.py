"""SPAN™ orchestration engine."""

from __future__ import annotations

import argparse
import logging
from collections.abc import Iterable
from pathlib import Path

from .analyzers import DependencyAnalyzer
from .evidence import EvidenceStore
from .graph import ArchitecturalGraph
from .models import AnalysisContext, AnalyzerResult
from .registry import Analyzer, AnalyzerRegistry
from .report import SpanReportWriter

LOGGER = logging.getLogger(__name__)


class SpanEngine:
    """Composition root for SPAN analysis execution."""

    def __init__(
        self,
        *,
        registry: AnalyzerRegistry | None = None,
        evidence: EvidenceStore | None = None,
        graph: ArchitecturalGraph | None = None,
        reporter: SpanReportWriter | None = None,
    ) -> None:
        self.registry = registry or AnalyzerRegistry()
        self.evidence = evidence or EvidenceStore()
        self.graph = graph or ArchitecturalGraph()
        self.reporter = reporter or SpanReportWriter()

    @classmethod
    def with_defaults(cls) -> SpanEngine:
        engine = cls()
        engine.register(DependencyAnalyzer())
        return engine

    def register(self, analyzer: Analyzer, *, replace: bool = False) -> Analyzer:
        return self.registry.register(analyzer, replace=replace)

    def run(
        self,
        context: AnalysisContext,
        *,
        analyzers: Iterable[str] | None = None,
        continue_on_error: bool = True,
    ) -> list[AnalyzerResult]:
        selected = (
            [self.registry.get(name) for name in analyzers]
            if analyzers is not None
            else list(self.registry.all())
        )
        results: list[AnalyzerResult] = []
        for analyzer in selected:
            LOGGER.info("Running SPAN analyzer: %s", analyzer.name)
            try:
                result = analyzer.analyze(context, self.evidence, self.graph)
            except (
                Exception
            ) as exc:  # SPAN must report analyzer failures without hiding them.
                LOGGER.exception("SPAN analyzer failed: %s", analyzer.name)
                result = AnalyzerResult(
                    analyzer=analyzer.name,
                    version=analyzer.version,
                    error=f"{type(exc).__name__}: {exc}",
                ).complete()
                if not continue_on_error:
                    results.append(result)
                    raise
            results.append(result)
        return results

    def analyze_and_report(
        self,
        repository_root: str | Path,
        *,
        output_directory: str | Path | None = None,
        analyzers: Iterable[str] | None = None,
    ) -> tuple[list[AnalyzerResult], dict[str, Path]]:
        context = AnalysisContext.create(repository_root)
        results = self.run(context, analyzers=analyzers)
        output = (
            Path(output_directory)
            if output_directory
            else context.repository_root / "reports/span"
        )
        artifacts = self.reporter.write_all(
            repository_root=context.repository_root,
            results=results,
            graph=self.graph,
            output_directory=output,
        )
        return results, artifacts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the AletheusOS SPAN architectural analyzer"
    )
    parser.add_argument("repository", nargs="?", default=".", help="Repository root")
    parser.add_argument("--output", default=None, help="Report output directory")
    parser.add_argument(
        "--analyzer",
        action="append",
        dest="analyzers",
        help="Analyzer name; repeatable",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    engine = SpanEngine.with_defaults()
    results, artifacts = engine.analyze_and_report(
        args.repository,
        output_directory=args.output,
        analyzers=args.analyzers,
    )
    failed = [result for result in results if not result.succeeded]
    print("SPAN™ analysis complete")
    for name, path in artifacts.items():
        print(f"  {name}: {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
