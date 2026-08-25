import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

PINNED_BASELINE = "5204ef93c569ea5d200cd9d3c79631500e566c78"

class MissionControlPlatformReadModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = Path(__file__).resolve().parents[1]
        tool = cls.repo / "tools/mission_control_platform_read_model.py"
        spec = importlib.util.spec_from_file_location("mc_platform_read_model", tool)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        cls.module = module

    def build(self):
        return self.module.build_model(self.repo, PINNED_BASELINE)

    def test_bounded_service_set(self):
        model = self.build()
        self.assertEqual(set(model["services"]), {"Platform Services", "A3ye", "Mammoth"})
        self.assertEqual(model["opus_runtime_binding"], "DEFERRED_PENDING_CONCRETE_RUNTIME_CONTRACT")

    def test_contracts_are_inspect_read_only(self):
        model = self.build()
        for service in model["services"].values():
            self.assertEqual(service["contract"]["capability"], "inspect")
            self.assertEqual(service["contract"]["effect"], "READ_ONLY")
            self.assertFalse(service["adapter"]["direct_subsystem_execution"])
            self.assertFalse(service["adapter"]["network_transport"])

    def test_evidence_is_tracked_clean_and_hashed(self):
        model = self.build()
        for service in model["services"].values():
            for item in service["read_model"]["implementation_evidence"]:
                self.assertTrue(item["tracked"])
                self.assertTrue(item["clean"])
                self.assertEqual(len(item["sha256"]), 64)
                self.assertGreater(item["bytes"], 0)

    def test_mutating_execution_stays_disabled(self):
        model = self.build()
        self.assertFalse(model["network_transport_present"])
        self.assertFalse(model["write_or_mutating_execution_authorized"])
        self.assertFalse(model["a3ye_general_command_execution_authorized"])

    def test_explicit_baseline_is_pinned_not_ambient_head(self):
        model = self.build()
        ambient_head = subprocess.run(
            ["git", "-C", str(self.repo), "rev-parse", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(model["baseline_commit"], PINNED_BASELINE)
        self.assertNotEqual(ambient_head, PINNED_BASELINE)

    def test_invalid_baseline_is_rejected(self):
        with self.assertRaises(RuntimeError):
            self.module.build_model(self.repo, "0" * 40)

if __name__ == "__main__":
    unittest.main()
