from __future__ import annotations

from .models import PrimitiveDefinition


class Engine:
    NAMES = (
        "Surface",
        "Grid",
        "Stack",
        "Cluster",
        "Sidebar",
        "Canvas",
        "Divider",
        "Spacer",
    )

    def catalog(self) -> tuple[PrimitiveDefinition, ...]:
        return tuple(
            PrimitiveDefinition(
                name=n,
                layer="structure",
                purpose=f"Canonical {n} structure primitive.",
                props=("as", "gap", "align", "justify", "responsive"),
            )
            for n in self.NAMES
        )
