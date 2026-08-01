from __future__ import annotations

import uuid

from .models import Action, Experience, Node, RuntimeMeta


class Engine:
    def compose(
        self,
        *,
        title: str,
        layout_type: str,
        intent_name: str,
        catalog: set[str],
        data: dict[str, object],
    ) -> Experience:
        children = []
        if "MetricsCard" in catalog and "metrics" in data:
            for i, m in enumerate(data["metrics"]):
                children.append(Node("MetricsCard", dict(m), f"metric_{i}"))
        if "DataGrid" in catalog and "rows" in data:
            children.append(
                Node(
                    "DataGrid",
                    {"columns": data.get("columns", []), "rows": data["rows"]},
                    "primary_data_grid",
                    (Action("onSelect", "DISPATCH_INTENT", {"intent": "inspect_row"}),),
                )
            )
        if not children:
            children.append(
                Node(
                    "BannerAlert",
                    {"message": "Structured data is unavailable.", "severity": "info"},
                    "safe_fallback",
                )
            )
        return Experience(
            "23.0.0",
            RuntimeMeta(title, layout_type, {}),
            Node(
                "LayoutContainer",
                {"direction": "vertical", "spacing": "medium"},
                children=tuple(children),
            ),
            str(uuid.uuid4()),
            "1.0.0",
            0.92,
            (f"intent:{intent_name}",),
        )
