from __future__ import annotations

from typing import ClassVar

from .models import Experience, Node


class Engine:
    """Validate schema-driven UXR experience payloads."""

    LAYOUT_TYPES: ClassVar[frozenset[str]] = frozenset(
        {
            "dashboard",
            "detail",
            "workflow",
            "summary",
        }
    )
    ACTION_TYPES: ClassVar[frozenset[str]] = frozenset(
        {
            "DISPATCH_INTENT",
            "NAVIGATE",
            "OPEN_MODAL",
        }
    )
    TRIGGERS: ClassVar[frozenset[str]] = frozenset(
        {
            "onSelect",
            "onSubmit",
            "onChange",
        }
    )

    def validate(
        self,
        experience: Experience,
        catalog: set[str],
    ) -> dict[str, object]:
        findings: list[str] = []

        if experience.meta.layout_type not in self.LAYOUT_TYPES:
            findings.append("invalid layoutType")

        def walk(node: Node, path: str) -> None:
            if node.component not in catalog:
                findings.append(f"unknown component at {path}: {node.component}")

            for action in node.actions:
                if action.action_type not in self.ACTION_TYPES:
                    findings.append(
                        f"invalid action type at {path}: {action.action_type}"
                    )
                if action.trigger not in self.TRIGGERS:
                    findings.append(f"invalid trigger at {path}: {action.trigger}")

            for index, child in enumerate(node.children):
                walk(child, f"{path}.children[{index}]")

        walk(experience.root, "root")
        return {
            "valid": not findings,
            "findings": findings,
            "schemaVersion": experience.schema_version,
        }
