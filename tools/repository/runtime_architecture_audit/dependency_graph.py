from __future__ import annotations

import json
from pathlib import Path


def graph_payload(
    graph: dict[str, set[str]],
    cycles: list[list[str]],
) -> dict[str, object]:
    edges = [
        {
            "source": source,
            "target": target,
        }
        for source in sorted(graph)
        for target in sorted(graph[source])
    ]

    return {
        "nodes": [
            {
                "id": module_name,
                "label": module_name,
            }
            for module_name in sorted(graph)
        ],
        "edges": edges,
        "cycles": cycles,
        "summary": {
            "node_count": len(graph),
            "edge_count": len(edges),
            "cycle_count": len(cycles),
        },
    }


def _mermaid_identifier(module_name: str) -> str:
    return module_name.replace(".", "_").replace("-", "_").replace("/", "_")


def render_mermaid(graph: dict[str, set[str]]) -> str:
    lines = ["flowchart TD"]

    for module_name in sorted(graph):
        identifier = _mermaid_identifier(module_name)
        escaped_label = module_name.replace('"', '\\"')
        lines.append(f'    {identifier}["{escaped_label}"]')

    for source in sorted(graph):
        source_id = _mermaid_identifier(source)

        for target in sorted(graph[source]):
            target_id = _mermaid_identifier(target)
            lines.append(f"    {source_id} --> {target_id}")

    if len(lines) == 1:
        lines.append('    empty["No runtime dependency edges discovered"]')

    return "\n".join(lines)


def write_dependency_graph_reports(
    graph: dict[str, set[str]],
    cycles: list[list[str]],
    output_root: Path,
) -> None:
    output_root.mkdir(parents=True, exist_ok=True)

    payload = graph_payload(graph, cycles)

    (output_root / "runtime-dependency-graph.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    markdown = [
        "# Runtime Dependency Graph",
        "",
        "```mermaid",
        render_mermaid(graph),
        "```",
        "",
        "## Summary",
        "",
        f"- Modules: {payload['summary']['node_count']}",
        f"- Internal dependency edges: {payload['summary']['edge_count']}",
        f"- Dependency cycles: {payload['summary']['cycle_count']}",
        "",
    ]

    if cycles:
        markdown.extend(
            [
                "## Cycles",
                "",
            ]
        )

        for cycle in cycles:
            markdown.append(f"- {' → '.join(cycle)}")

        markdown.append("")

    (output_root / "runtime-dependency-graph.md").write_text(
        "\n".join(markdown),
        encoding="utf-8",
    )
