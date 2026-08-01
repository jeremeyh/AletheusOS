from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    namespace: str
    name: str
    value: str
    semantic_role: str


class Engine:
    def resolve(self, tokens: tuple[Token, ...], *, namespace: str, name: str) -> str:
        for token in tokens:
            if token.namespace == namespace and token.name == name:
                return token.value
        raise KeyError(f"Unknown token: {namespace}.{name}")

    def validate(self, tokens: tuple[Token, ...]) -> dict[str, object]:
        keys = [(item.namespace, item.name) for item in tokens]
        duplicates = sorted({f"{n}.{k}" for n, k in keys if keys.count((n, k)) > 1})
        return {"valid": not duplicates, "duplicates": duplicates, "count": len(tokens)}
