from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Action:
    trigger: str
    action_type: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "trigger": self.trigger,
            "actionType": self.action_type,
            "payload": self.payload,
        }


@dataclass(frozen=True)
class Node:
    component: str
    props: dict[str, Any]
    node_id: str | None = None
    actions: tuple[Action, ...] = ()
    children: tuple[Node, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "component": self.component,
            "props": self.props,
            "children": [c.to_dict() for c in self.children],
        }
        if self.node_id is not None:
            data["id"] = self.node_id
        if self.actions:
            data["actions"] = [a.to_dict() for a in self.actions]
        return data


@dataclass(frozen=True)
class RuntimeMeta:
    title: str
    layout_type: str
    theme_tokens: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Experience:
    runtime_version: str
    meta: RuntimeMeta
    root: Node
    experience_id: str
    schema_version: str
    confidence: float = 1.0
    provenance: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtimeVersion": self.runtime_version,
            "experienceId": self.experience_id,
            "schemaVersion": self.schema_version,
            "confidence": self.confidence,
            "provenance": list(self.provenance),
            "meta": {
                "title": self.meta.title,
                "layoutType": self.meta.layout_type,
                "themeTokens": self.meta.theme_tokens,
            },
            "root": self.root.to_dict(),
        }
