from __future__ import annotations

from .models import Experience, Node, RuntimeMeta


class Engine:
    def adapt(
        self,
        experience: Experience,
        *,
        viewport_width: int,
        viewport_height: int,
        role: str = "user",
    ) -> Experience:
        if viewport_width < 640:
            spacing, columns = "small", 1
        elif viewport_width < 1100:
            spacing, columns = "medium", 2
        else:
            spacing, columns = "large", (4 if role in {"analyst", "admin"} else 3)
        props = {
            **experience.root.props,
            "direction": "vertical",
            "spacing": spacing,
            "columns": columns,
            "viewportHeight": viewport_height,
        }
        root = Node(
            experience.root.component,
            props,
            experience.root.node_id,
            experience.root.actions,
            experience.root.children,
        )
        meta = RuntimeMeta(
            experience.meta.title,
            experience.meta.layout_type,
            {
                **experience.meta.theme_tokens,
                "density": "compact" if viewport_width < 640 else "comfortable",
            },
        )
        return Experience(
            experience.runtime_version,
            meta,
            root,
            experience.experience_id,
            experience.schema_version,
            experience.confidence,
            experience.provenance + ("adaptive-layout",),
        )
