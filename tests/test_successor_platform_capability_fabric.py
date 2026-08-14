"""Successor proof fixture — Platform Capability Fabric.

Proves explicit capability identity/ownership, canonical service attachment,
and fail-closed rejection of forbidden runtime-core attachment.
"""

import pytest

from aletheus.platform_capability_fabric.genesis_112_22_1.attachment import (
    CapabilityAttachment,
    CapabilityAttachmentRegistry,
)
from aletheus.platform_capability_fabric.genesis_112_22_1.contracts import (
    CapabilityIdentity,
    CapabilityKind,
)


def _identity(capability_id="capability.successor-proof"):
    return CapabilityIdentity(
        capability_id=capability_id,
        kind=CapabilityKind.ENGINE,
        authority_owner="ENGINE_OWNER",
        lifecycle_owner="PLATFORM_LIFECYCLE",
    )


def test_capability_identity_preserves_external_authority_boundaries():
    identity = _identity()
    identity.validate()

    assert identity.durable_state_owner == "MAMMOTH"
    assert identity.reliability_observer == "RSF"
    assert identity.final_certification_authority == "EXTERNAL_RAF"


def test_capability_identity_cannot_masquerade_as_service():
    with pytest.raises(ValueError, match="cannot masquerade as a service identity"):
        _identity("service.invalid-capability").validate()


def test_capability_attaches_through_explicit_service_boundary():
    registry = CapabilityAttachmentRegistry()
    attachment = CapabilityAttachment(
        capability=_identity(),
        service_binding="service.successor-proof",
        adapter_id="adapter.successor-proof",
    )

    assert registry.attach(attachment) == attachment
    assert registry.snapshot() == (attachment,)


def test_capability_direct_runtime_core_attachment_is_refused():
    registry = CapabilityAttachmentRegistry()
    attachment = CapabilityAttachment(
        capability=_identity(),
        service_binding="runtime.core",
        adapter_id="adapter.invalid",
    )

    with pytest.raises(ValueError, match="direct runtime-core capability attachment refused"):
        registry.attach(attachment)
