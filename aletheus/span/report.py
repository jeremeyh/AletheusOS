"""Unified JSON and Markdown reporting for SPAN™."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from .graph import ArchitecturalGraph
from .models import AnalyzerResult, FindingSeverity, utc_now_iso


class SpanReportWriter:
    """Write deterministic SPAN analysis artifacts."""

    def build_payload(
        self,
        *,
        repository_root: Path,
        results: Iterable[AnalyzerResult],
        graph: ArchitecturalGraph,
    ) -> dict[str, Any]:
        result_list = list(results)
        severity_counts = Counter(
            finding.severity.value
            for result in result_list
            for finding in result.findings
        )
        return {
            "schema_version": "1.0",
            "generated_at": utc_now_iso(),
            "repository_root": str(repository_root),
            "summary": {
                "analyzers": len(result_list),
                "successful_analyzers": sum(result.succeeded for result in result_list),
                "failed_analyzers": sum(not result.succeeded for result in result_list),
                "findings": sum(len(result.findings) for result in result_list),
                "evidence": sum(len(result.evidence) for result in result_list),
                "metrics": sum(len(result.metrics) for result in result_list),
                "graph_nodes": len(graph.nodes()),
                "graph_edges": len(graph.edges()),
                "findings_by_severity": dict(sorted(severity_counts.items())),
            },
            "results": [result.to_dict() for result in result_list],
            "graph": graph.to_dict(),
        }

    def write_json(self, payload: dict[str, Any], destination: str | Path) -> Path:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return path

    def write_markdown(self, payload: dict[str, Any], destination: str | Path) -> Path:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        summary = payload["summary"]
        lines = [
            "# SPAN™ Architectural Analysis Report",
            "",
            f"Generated: `{payload['generated_at']}`",
            f"Repository: `{payload['repository_root']}`",
            "",
            "## Summary",
            "",
            f"- Analyzers: **{summary['analyzers']}**",
            f"- Successful analyzers: **{summary['successful_analyzers']}**",
            f"- Failed analyzers: **{summary['failed_analyzers']}**",
            f"- Findings: **{summary['findings']}**",
            f"- Evidence records: **{summary['evidence']}**",
            f"- Graph nodes: **{summary['graph_nodes']}**",
            f"- Graph edges: **{summary['graph_edges']}**",
            "",
        ]
        for result in payload["results"]:
            lines.extend(
                [
                    f"## {result['analyzer']} v{result['version']}",
                    "",
                    f"Status: **{'passed' if result['succeeded'] else 'failed'}**",
                    "",
                ]
            )
            if result["error"]:
                lines.extend([f"Error: `{result['error']}`", ""])
            if not result["findings"]:
                lines.extend(["No findings.", ""])
                continue
            for finding in result["findings"]:
                severity = finding["severity"].upper()
                lines.extend(
                    [
                        f"### [{severity}] {finding['title']}",
                        "",
                        finding["description"],
                        "",
                    ]
                )
                if finding["recommendation"]:
                    lines.extend([f"**Recommendation:** {finding['recommendation']}", ""])
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return path

    def write_all(
        self,
        *,
        repository_root: Path,
        results: Iterable[AnalyzerResult],
        graph: ArchitecturalGraph,
        output_directory: str | Path,
    ) -> dict[str, Path]:
        output = Path(output_directory)
        payload = self.build_payload(
            repository_root=repository_root,
            results=results,
            graph=graph,
        )
        return {
            "json": self.write_json(payload, output / "span.json"),
            "markdown": self.write_markdown(payload, output / "span.md"),
            "graph_json": graph.export_json(output / "atlas.json"),
            "graph_dot": graph.export_dot(output / "atlas.dot"),
        }
