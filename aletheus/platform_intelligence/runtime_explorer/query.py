"""Minimal Constitutional Query Language parser."""

from __future__ import annotations

from dataclasses import dataclass

from .exceptions import ExplorerQueryError

_ALLOWED_FIELDS = frozenset(
    {
        "text",
        "kind",
        "state",
        "health",
        "owner",
        "authority",
        "address",
    }
)


@dataclass(frozen=True, slots=True)
class ExplorerQuery:
    """Parsed conjunction of Runtime Explorer filters."""

    terms: tuple[tuple[str, str], ...]

    @classmethod
    def parse(
        cls,
        expression: str,
    ) -> ExplorerQuery:
        normalized = expression.strip()

        if not normalized:
            raise ExplorerQueryError("Explorer query cannot be empty.")

        raw_terms = [
            item.strip()
            for item in normalized.replace(
                " AND ",
                " ",
            ).split()
            if item.strip()
        ]

        parsed: list[tuple[str, str]] = []

        for term in raw_terms:
            if ":" in term:
                field, value = term.split(
                    ":",
                    1,
                )
                field = field.strip().lower()
                value = value.strip().lower()

                if field not in _ALLOWED_FIELDS:
                    raise ExplorerQueryError(f"Unsupported query field: {field}")

                if not value:
                    raise ExplorerQueryError(f"Query value is missing for: {field}")
            else:
                field = "text"
                value = term.lower()

            parsed.append((field, value))

        return cls(terms=tuple(parsed))
