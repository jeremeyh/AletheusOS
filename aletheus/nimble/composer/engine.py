from __future__ import annotations

from dataclasses import dataclass

from .models import PrimitiveDefinition


@dataclass(frozen=True)
class ExperienceNode:
    primitive: str
    children: tuple[ExperienceNode, ...] = ()


class Engine:
    def compose(
        self, root: ExperienceNode, catalog: tuple[PrimitiveDefinition, ...]
    ) -> dict[str, object]:
        allowed = {item.name for item in catalog}
        unknown = []

        def walk(node: ExperienceNode) -> int:
            if node.primitive not in allowed:
                unknown.append(node.primitive)
            return 1 + sum(walk(child) for child in node.children)

        count = walk(root)
        return {
            "valid": not unknown,
            "node_count": count,
            "unknown_primitives": sorted(set(unknown)),
            "root": root.primitive,
        }
