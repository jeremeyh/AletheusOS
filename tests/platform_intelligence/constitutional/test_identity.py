from uuid import UUID

import pytest

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalAddress,
    ConstitutionalIdentity,
    ConstitutionalKind,
)


def test_address_is_normalized() -> None:
    address = ConstitutionalAddress(" Service.Workspace ")

    assert str(address) == "service.workspace"


@pytest.mark.parametrize(
    "address",
    [
        "",
        "Service Workspace",
        ".service",
        "service.",
        "service..workspace",
        "service/workspace",
    ],
)
def test_invalid_addresses_are_rejected(address: str) -> None:
    with pytest.raises(ValueError):
        ConstitutionalAddress(address)


def test_identity_is_created_with_uuid() -> None:
    identity = ConstitutionalIdentity.create(
        address="runtime.core",
        kind=ConstitutionalKind.RUNTIME,
    )

    assert identity.address == ConstitutionalAddress("runtime.core")
    assert isinstance(identity.object_id, UUID)
