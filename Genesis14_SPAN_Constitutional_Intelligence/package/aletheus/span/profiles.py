from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class RuleProfile:
    name: str
    enabled_categories: tuple[str, ...] = ()
    disabled_rule_ids: tuple[str, ...] = ()
    fail_on: str = "high"
    metadata: dict[str, Any] = field(default_factory=dict)


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return (
            []
            if not inner
            else [item.strip().strip("'\"") for item in inner.split(",")]
        )
    return value.strip("'\"")


def _minimal_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_list: list[str] | None = None
    current_key = ""
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("- ") and current_list is not None:
            current_list.append(stripped[2:].strip().strip("'\""))
            continue
        if ":" not in stripped:
            raise ValueError(f"unsupported profile syntax: {raw}")
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            current_list = []
            data[key] = current_list
            current_key = key
        else:
            current_list = None
            current_key = key
            data[key] = _parse_scalar(value)
    return data


def load_profile(path: str | Path) -> RuleProfile:
    profile_path = Path(path)
    text = profile_path.read_text(encoding="utf-8")
    if profile_path.suffix.lower() == ".json":
        raw = json.loads(text)
    else:
        try:
            import yaml  # type: ignore
        except ImportError:
            raw = _minimal_yaml(text)
        else:
            raw = yaml.safe_load(text) or {}

    return RuleProfile(
        name=str(raw.get("name") or profile_path.stem),
        enabled_categories=tuple(raw.get("enabled_categories") or ()),
        disabled_rule_ids=tuple(raw.get("disabled_rule_ids") or ()),
        fail_on=str(raw.get("fail_on") or "high"),
        metadata=dict(raw.get("metadata") or {}),
    )
