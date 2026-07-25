"""Constitutional identity and addressing primitives."""

from __future__ import annotations

import re
from dataclasses import dataclass
from uuid import UUID, uuid4

from .enums import ConstitutionalKind

_ADDRESS_PATTERN = re.compile(
    r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$"
)


@dataclass(frozen=True, slots=True, order=True)
class ConstitutionalAddress:
    """
    Globally discoverable constitutional address.

    Examples:
        runtime.core
        service.workspace
        capability.navigation
        application.cardhawk
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if not normalized:
            raise ValueError("Constitutional address cannot be empty.")

        if not _ADDRESS_PATTERN.fullmatch(normalized):
            raise ValueError(
                "Invalid constitutional address. Use lowercase segments "
                "separated by '.', '_' or '-'."
            )

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ConstitutionalIdentity:
    """Immutable identity assigned to every constitutional object."""

    address: ConstitutionalAddress
    kind: ConstitutionalKind
    object_id: UUID

    @classmethod
    def create(
        cls,
        *,
        address: str | ConstitutionalAddress,
        kind: ConstitutionalKind,
        object_id: UUID | None = None,
    ) -> ConstitutionalIdentity:
        constitutional_address = (
            address
            if isinstance(address, ConstitutionalAddress)
            else ConstitutionalAddress(address)
        )

        return cls(
            address=constitutional_address,
            kind=kind,
            object_id=object_id or uuid4(),
        )
