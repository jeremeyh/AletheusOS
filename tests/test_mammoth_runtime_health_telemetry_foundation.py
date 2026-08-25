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
MODULE_PATH = Path(os.environ["ALETHEUSOS_MAMMOTH_OBSERVATION_MODULE"]).resolve()
EXPECTED_MANIFEST = os.environ.get("ALETHEUSOS_MAMMOTH_EXPECTED_MANIFEST")

if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

spec = importlib.util.spec_from_file_location(
    "mammoth_runtime_observation_under_test", MODULE_PATH
)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class MammothRuntimeObservationFoundationTests(unittest.TestCase):
    def setUp(self):
        self.source = module.MammothRuntimeObservationSource()

    def observation(self, **overrides):
        base = dict(
            observed_at="2026-08-25T17:25:00-05:00",
            observation_source=module.SOURCE_IDENTITY,
            health_state="HEALTHY",
            failure_reason="",
            telemetry_payload_schema="aletheus.mammoth.telemetry.v1",
            telemetry_payload={
                "persistence_state": "available",
                "index_state": "available",
            },
        )
        base.update(overrides)
        return module.MammothObservation(**base)

    def test_01_service_identity_is_exact_mammoth(self):
        self.assertEqual(module.SERVICE_IDENTITY, "Mammoth")
        self.assertEqual(self.source.service_identity, "Mammoth")

    def test_02_service_role_is_storage_persistence_lifecycle_only(self):
        self.assertEqual(
            module.SERVICE_ROLE,
            "storage,persistence,indexing,replication,archive,recovery,lifecycle",
        )

    def test_03_source_is_read_only_foundation_not_live_binding(self):
        self.assertEqual(
            module.SOURCE_KIND,
            "IN_PROCESS_READ_ONLY_OBSERVATION_SOURCE_FOUNDATION",
        )
        self.assertEqual(module.EFFECT, "READ_ONLY")
        self.assertFalse(module.RUNTIME_LIVENESS_ESTABLISHED)
        self.assertFalse(module.REPOSITORY_EVIDENCE_IS_LIVENESS)
        self.assertFalse(module.LIVE_BINDING_PERFORMED)
        self.assertFalse(module.LIVE_PROBE_BOUND)
        self.assertFalse(module.NETWORK_TRANSPORT_BOUND)

    def test_04_health_contract_resolves_through_accepted_foundation(self):
        binding = module._resolve_binding("health")
        self.assertTrue(binding["contract_id"])
        self.assertTrue(binding["contract_version"])
        self.assertTrue(binding["adapter_id"])
        self.assertTrue(binding["adapter_version"])

    def test_05_telemetry_contract_resolves_through_accepted_foundation(self):
        binding = module._resolve_binding("telemetry")
        self.assertTrue(binding["contract_id"])
        self.assertTrue(binding["contract_version"])
        self.assertTrue(binding["adapter_id"])
        self.assertTrue(binding["adapter_version"])

    def test_06_receipt_schema_version_is_explicit(self):
        self.assertTrue(module._receipt_schema_version())

    def test_07_valid_health_observation_produces_read_only_receipt(self):
        receipt = self.source.health(self.observation())
        self.assertNotEqual(receipt.get("status"), "REFUSED")
        self.assertEqual(receipt.get("service"), "Mammoth")
        self.assertEqual(receipt.get("health_state"), "HEALTHY")
        self.assertEqual(receipt.get("effect"), "READ_ONLY")

    def test_08_valid_telemetry_observation_requires_schema_and_is_read_only(self):
        receipt = self.source.telemetry(self.observation())
        self.assertNotEqual(receipt.get("status"), "REFUSED")
        self.assertEqual(receipt.get("service"), "Mammoth")
        self.assertEqual(receipt.get("health_state"), "HEALTHY")
        self.assertEqual(receipt.get("effect"), "READ_ONLY")
        self.assertEqual(
            receipt.get("telemetry_payload_schema"),
            "aletheus.mammoth.telemetry.v1",
        )

    def test_09_invalid_health_state_refuses_and_reports_unknown(self):
        receipt = self.source.health(self.observation(health_state="BROKEN"))
        self.assertEqual(receipt.get("status"), "REFUSED")
        self.assertEqual(receipt.get("health_state"), "UNKNOWN")

    def test_10_missing_timestamp_can_never_report_healthy(self):
        receipt = self.source.health(self.observation(observed_at=""))
        self.assertNotEqual(receipt.get("health_state"), "HEALTHY")

    def test_11_missing_telemetry_schema_refuses_and_reports_unknown(self):
        receipt = self.source.telemetry(
            self.observation(telemetry_payload_schema="")
        )
        self.assertEqual(receipt.get("status"), "REFUSED")
        self.assertEqual(receipt.get("health_state"), "UNKNOWN")

    def test_12_unknown_service_refuses(self):
        result = module.foundation.resolve_contract(
            "UnknownMammothService", "health"
        )
        self.assertEqual(result.get("status"), "REFUSED")

    def test_13_unknown_contract_refuses_and_cannot_report_healthy(self):
        binding = module._resolve_binding("health")
        receipt = module._call_supported(
            module.foundation.build_health_receipt,
            service="Mammoth",
            contract_id="unknown.mammoth.contract.v0",
            adapter_id=binding["adapter_id"],
            observed_at="2026-08-25T17:25:00-05:00",
            observation_source=module.SOURCE_IDENTITY,
            health_state="HEALTHY",
            failure_reason="",
        )
        self.assertEqual(receipt.get("status"), "REFUSED")
        self.assertNotEqual(receipt.get("health_state"), "HEALTHY")

    def test_14_unknown_adapter_refuses_and_cannot_report_healthy(self):
        binding = module._resolve_binding("health")
        receipt = module._call_supported(
            module.foundation.build_health_receipt,
            service="Mammoth",
            contract_id=binding["contract_id"],
            adapter_id="unknown.mammoth.adapter.v0",
            observed_at="2026-08-25T17:25:00-05:00",
            observation_source=module.SOURCE_IDENTITY,
            health_state="HEALTHY",
            failure_reason="",
        )
        self.assertEqual(receipt.get("status"), "REFUSED")
        self.assertNotEqual(receipt.get("health_state"), "HEALTHY")

    def test_15_nonhealthy_states_project_degraded_through_f4h(self):
        for state in ("DEGRADED", "UNAVAILABLE", "UNKNOWN"):
            for activity in ("idle", "focused", "engaged"):
                self.assertEqual(
                    module.foundation.project_f4h_state(state, activity),
                    "degraded",
                )

    def test_16_f4g_allow_is_not_execution(self):
        for capability in ("health", "telemetry"):
            resolved = module.foundation.resolve_contract(
                "Mammoth", capability
            )
            self.assertEqual(resolved["status"], "RESOLVED")
            self.assertTrue(resolved["f4g_required"])
            self.assertTrue(resolved["allow_is_not_direct_execution"])
            self.assertFalse(resolved["direct_execution_performed"])

    def test_17_module_contains_no_transport_storage_or_command_imports(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        forbidden = [
            r"^\s*(?:from|import)\s+requests\b",
            r"^\s*(?:from|import)\s+urllib\b",
            r"^\s*(?:from|import)\s+http\.client\b",
            r"^\s*(?:from|import)\s+socket\b",
            r"^\s*(?:from|import)\s+websockets?\b",
            r"^\s*(?:from|import)\s+grpc\b",
            r"^\s*(?:from|import)\s+subprocess\b",
            r"^\s*(?:from|import)\s+psutil\b",
            r"^\s*(?:from|import)\s+aletheus\.institutional_civilization\b",
            r"^\s*(?:from|import)\s+aletheus\.strategic\.span\b",
        ]
        for pattern in forbidden:
            self.assertIsNone(re.search(pattern, text, re.I | re.M), pattern)

    def test_18_manifest_declares_service_ownership_and_exact_authority(self):
        manifest = module.build_manifest()
        self.assertEqual(manifest["service_identity"], "Mammoth")
        self.assertEqual(
            manifest["runtime_producer_authority_paths"],
            ["aletheus/mammoth/runtime_observation.py"],
        )
        self.assertEqual(
            manifest["service_ownership_evidence"]["authority_path"],
            "aletheus/mammoth/runtime_observation.py",
        )

    def test_19_manifest_excludes_nonruntime_authority_categories(self):
        manifest = module.build_manifest()
        for key in (
            "test_files_are_runtime_producer_authority",
            "fixture_files_are_runtime_producer_authority",
            "documentation_is_runtime_producer_authority",
            "backup_files_are_runtime_producer_authority",
            "report_files_are_runtime_producer_authority",
        ):
            self.assertFalse(manifest[key], key)

    def test_20_manifest_declares_no_live_transport_mutation_or_other_binding(self):
        manifest = module.build_manifest()
        for key in (
            "runtime_liveness_established",
            "repository_evidence_is_liveness",
            "live_binding_performed",
            "live_probe_binding",
            "network_transport_binding",
            "rpc_binding",
            "websocket_binding",
            "http_endpoint_binding",
            "write_or_mutating_capability",
            "autonomous_action",
            "direct_ungated_subsystem_reach_through",
            "platform_services_binding_implementation",
            "a3ye_binding_implementation",
            "protected_mc84f4i_visual_change",
        ):
            self.assertFalse(manifest[key], key)
        self.assertEqual(
            manifest["opus_runtime_binding"],
            "DEFERRED_PENDING_CONCRETE_RUNTIME_CONTRACT",
        )

    def test_21_manifest_is_byte_reproducible(self):
        first = json.dumps(
            module.build_manifest(), indent=2, sort_keys=True
        ) + "\n"
        second = json.dumps(
            module.build_manifest(), indent=2, sort_keys=True
        ) + "\n"
        self.assertEqual(first, second)
        if EXPECTED_MANIFEST:
            self.assertEqual(
                first,
                Path(EXPECTED_MANIFEST).read_text(encoding="utf-8"),
            )

    def test_22_only_health_and_telemetry_are_public_runtime_methods(self):
        public = {
            name
            for name in dir(module.MammothRuntimeObservationSource)
            if not name.startswith("_")
            and callable(
                getattr(module.MammothRuntimeObservationSource, name)
            )
        }
        self.assertEqual(public, {"health", "telemetry"})


if __name__ == "__main__":
    unittest.main()
