#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import unittest
from pathlib import Path

REPO = Path(os.environ["ALETHEUSOS_REPO"]).resolve()
MODULE_PATH = Path(os.environ["ALETHEUSOS_A3YE_OBSERVATION_MODULE"]).resolve()
EXPECTED_MANIFEST = os.environ.get("ALETHEUSOS_A3YE_EXPECTED_MANIFEST")

if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

spec = importlib.util.spec_from_file_location("a3ye_runtime_observation_under_test", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class A3yeRuntimeObservationFoundationTests(unittest.TestCase):
    def setUp(self):
        self.source = module.A3yeRuntimeObservationSource()

    def observation(self, **overrides):
        base = dict(
            observed_at="2026-08-25T16:00:00-05:00",
            observation_source=module.SOURCE_IDENTITY,
            health_state="HEALTHY",
            failure_reason="",
            telemetry_payload_schema="aletheus.a3ye.telemetry.v1",
            telemetry_payload={"queue_depth": 0, "council_state": "idle"},
        )
        base.update(overrides)
        return module.A3yeObservation(**base)

    def test_service_identity_is_exact_a3ye(self):
        self.assertEqual(module.SERVICE_IDENTITY, "A3ye")
        self.assertEqual(self.source.service_identity, "A3ye")

    def test_source_is_read_only_foundation_not_live_binding(self):
        self.assertEqual(module.SOURCE_KIND, "IN_PROCESS_READ_ONLY_OBSERVATION_SOURCE_FOUNDATION")
        self.assertEqual(module.EFFECT, "READ_ONLY")
        self.assertFalse(module.RUNTIME_LIVENESS_ESTABLISHED)
        self.assertFalse(module.LIVE_PROBE_BOUND)
        self.assertFalse(module.NETWORK_TRANSPORT_BOUND)

    def test_health_contract_resolves_through_accepted_foundation(self):
        binding = module._resolve_binding("health")
        self.assertTrue(binding["contract_id"])
        self.assertTrue(binding["contract_version"])
        self.assertTrue(binding["adapter_id"])

    def test_telemetry_contract_resolves_through_accepted_foundation(self):
        binding = module._resolve_binding("telemetry")
        self.assertTrue(binding["contract_id"])
        self.assertTrue(binding["contract_version"])
        self.assertTrue(binding["adapter_id"])

    def test_valid_health_observation_produces_read_only_receipt(self):
        receipt = self.source.health(self.observation())
        self.assertNotEqual(receipt.get("status"), "REFUSED")
        self.assertEqual(receipt.get("service"), "A3ye")
        self.assertEqual(receipt.get("health_state"), "HEALTHY")
        self.assertEqual(receipt.get("effect"), "READ_ONLY")

    def test_valid_telemetry_observation_requires_schema_and_is_read_only(self):
        receipt = self.source.telemetry(self.observation())
        self.assertNotEqual(receipt.get("status"), "REFUSED")
        self.assertEqual(receipt.get("service"), "A3ye")
        self.assertEqual(receipt.get("health_state"), "HEALTHY")
        self.assertEqual(receipt.get("effect"), "READ_ONLY")
        self.assertEqual(receipt.get("telemetry_payload_schema"), "aletheus.a3ye.telemetry.v1")

    def test_invalid_health_state_refuses_and_reports_unknown(self):
        receipt = self.source.health(self.observation(health_state="BROKEN"))
        self.assertEqual(receipt.get("status"), "REFUSED")
        self.assertEqual(receipt.get("health_state"), "UNKNOWN")

    def test_missing_timestamp_can_never_report_healthy(self):
        receipt = self.source.health(self.observation(observed_at=""))
        self.assertNotEqual(receipt.get("health_state"), "HEALTHY")

    def test_missing_telemetry_schema_refuses_and_reports_unknown(self):
        receipt = self.source.telemetry(self.observation(telemetry_payload_schema=""))
        self.assertEqual(receipt.get("status"), "REFUSED")
        self.assertEqual(receipt.get("health_state"), "UNKNOWN")

    def test_nonhealthy_states_project_degraded_through_f4h(self):
        for state in ("DEGRADED", "UNAVAILABLE", "UNKNOWN"):
            for activity in ("idle", "focused", "engaged"):
                self.assertEqual(module.foundation.project_f4h_state(state, activity), "degraded")

    def test_f4g_allow_is_not_execution(self):
        for capability in ("health", "telemetry"):
            resolved = module.foundation.resolve_contract("A3ye", capability)
            self.assertEqual(resolved["status"], "RESOLVED")
            self.assertTrue(resolved["f4g_required"])
            self.assertTrue(resolved["allow_is_not_direct_execution"])
            self.assertFalse(resolved["direct_execution_performed"])

    def test_module_contains_no_transport_or_a3ye_command_imports(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        forbidden = [
            r"^\s*(?:from|import)\s+requests\b",
            r"^\s*(?:from|import)\s+urllib\b",
            r"^\s*(?:from|import)\s+http\.client\b",
            r"^\s*(?:from|import)\s+socket\b",
            r"^\s*(?:from|import)\s+websockets?\b",
            r"^\s*(?:from|import)\s+grpc\b",
            r"^\s*(?:from|import)\s+aletheus\.a3ye\.(?:core|council_bridge|balance_engine|constitutional_voice)\b",
        ]
        for pattern in forbidden:
            self.assertIsNone(re.search(pattern, text, re.I | re.M), pattern)

    def test_manifest_declares_exact_producer_authority_and_excludes_tests(self):
        manifest = module.build_manifest()
        self.assertEqual(
            manifest["runtime_producer_authority_paths"],
            ["aletheus/a3ye/runtime_observation.py"],
        )
        self.assertFalse(manifest["test_files_are_runtime_producer_authority"])
        self.assertFalse(manifest["mammoth_binding_implementation_authorized"])

    def test_manifest_declares_no_live_probe_transport_or_mutation(self):
        manifest = module.build_manifest()
        for key in (
            "runtime_liveness_established",
            "repository_evidence_is_liveness",
            "live_probe_binding",
            "network_transport_binding",
            "rpc_binding",
            "websocket_binding",
            "http_endpoint_binding",
            "general_a3ye_command_execution",
            "autonomous_action",
            "write_or_mutating_capability",
            "direct_ungated_subsystem_reach_through",
            "protected_mc84f4i_visual_change",
        ):
            self.assertFalse(manifest[key], key)

    def test_manifest_is_byte_reproducible(self):
        first = json.dumps(module.build_manifest(), indent=2, sort_keys=True) + "\n"
        second = json.dumps(module.build_manifest(), indent=2, sort_keys=True) + "\n"
        self.assertEqual(first, second)
        if EXPECTED_MANIFEST:
            self.assertEqual(first, Path(EXPECTED_MANIFEST).read_text(encoding="utf-8"))

    def test_only_health_and_telemetry_are_public_runtime_observation_callables(self):
        public = {
            name for name in dir(module.A3yeRuntimeObservationSource)
            if not name.startswith("_") and callable(getattr(module.A3yeRuntimeObservationSource, name))
        }
        self.assertEqual(public, {"health", "telemetry"})


if __name__ == "__main__":
    unittest.main()
