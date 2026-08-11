from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable
from .contracts import CapabilityIdentity

FORBIDDEN_ATTACHMENT_TARGETS = frozenset({
    "aletheus.runtime.core",
    "aletheus/runtime/core.py",
    "runtime.core",
})

@dataclass(frozen=True)
class CapabilityAttachment:
    capability: CapabilityIdentity
    service_binding: str
    adapter_id: str

class CapabilityAttachmentRegistry:
    """A bounded registry of capability attachments; it is not a ServiceRegistry."""
    def __init__(self) -> None:
        self._attachments: Dict[str, CapabilityAttachment] = {}

    def attach(self, attachment: CapabilityAttachment) -> CapabilityAttachment:
        attachment.capability.validate()
        if attachment.service_binding in FORBIDDEN_ATTACHMENT_TARGETS:
            raise ValueError("direct runtime-core capability attachment refused")
        if not attachment.service_binding.startswith("service."):
            raise ValueError("capabilities must attach through an explicit canonical service boundary")
        existing = self._attachments.get(attachment.capability.capability_id)
        if existing and existing != attachment:
            raise ValueError("conflicting capability authority/attachment refused")
        self._attachments[attachment.capability.capability_id] = attachment
        return attachment

    def snapshot(self):
        return tuple(self._attachments[k] for k in sorted(self._attachments))
