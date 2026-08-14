"""Successor proof fixture — Platform Service Fabric.

Proves bounded adapter/assurance behavior and fail-closed dependency gates
without mutating service-fabric implementation.
"""

import pytest

from aletheus.platform_service_fabric.genesis_112_21_master.g112_21_6 import (
    MammothAssurancePort,
    RSFReliabilityPort,
)


class _Gateway:
    def __init__(self):
        self.payloads = []

    def persist_assurance_evidence(self, payload):
        self.payloads.append(payload)
        return {"accepted": True, "payload": payload}


class _Observer:
    def observe(self, service_id):
        return {"service_id": service_id, "status": "HEALTHY"}


def test_service_fabric_requires_certified_mammoth_gateway():
    with pytest.raises(RuntimeError, match="certified Mammoth gateway required"):
        MammothAssurancePort(None)


def test_service_fabric_requires_rsf_observer():
    with pytest.raises(RuntimeError, match="RSF observer required"):
        RSFReliabilityPort(None)


def test_service_fabric_uses_bounded_mammoth_assurance_port():
    gateway = _Gateway()
    port = MammothAssurancePort(gateway)

    receipt = port.persist({"evidence": "successor-proof"})

    assert receipt["accepted"] is True
    assert gateway.payloads == [{"evidence": "successor-proof"}]


def test_service_fabric_consumes_rsf_observation_without_owning_authority():
    port = RSFReliabilityPort(_Observer())
    result = port.observe("service.successor-proof")

    assert result == {
        "service_id": "service.successor-proof",
        "status": "HEALTHY",
    }
