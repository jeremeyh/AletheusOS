from __future__ import annotations

from typing import ClassVar

from .models import Experience, Node


class Engine:
    """Sanitize UXR experiences through constitutional guardrails."""

    BLOCKED_PROPS: ClassVar[frozenset[str]] = frozenset(
        {
            "rawHtml",
            "script",
            "dangerouslySetInnerHTML",
        }
    )

    def sanitize(
        self,
        experience: Experience,
        catalog: set[str],
    ) -> tuple[Experience, tuple[str, ...]]:
        findings: list[str] = []

        def clean(node: Node) -> Node:
            props = {
                key: value
                for key, value in node.props.items()
                if key not in self.BLOCKED_PROPS
            }
            removed = sorted(set(node.props) - set(props))
            if removed:
                findings.append(
                    "removed blocked props from "
                    f"{node.node_id or node.component}: {removed}"
                )

            component = node.component
            if component not in catalog:
                component = "BannerAlert"
                props = {
                    "message": ("A safe fallback replaced an unknown component."),
                    "severity": "warning",
                }
                findings.append(f"replaced unknown component: {node.component}")

            return Node(
                component=component,
                props=props,
                node_id=node.node_id,
                actions=node.actions,
                children=tuple(clean(child) for child in node.children),
            )

        sanitized = Experience(
            runtime_version=experience.runtime_version,
            meta=experience.meta,
            root=clean(experience.root),
            experience_id=experience.experience_id,
            schema_version=experience.schema_version,
            confidence=experience.confidence,
            provenance=experience.provenance + ("constitutional-guardrails",),
        )
        return sanitized, tuple(findings)
