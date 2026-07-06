from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class LighthouseBootloader:
    """
    Project Lighthouse

    Explicit boot coordinator for AletheusOS.

    Nothing should boot from package imports.
    Runtime startup should happen only through this bootloader
    or through intentional app launch scripts.
    """

    VERSION = "1.0.0"

    def __init__(self, root="."):
        self.root = Path(root).resolve()
        self.report_dir = self.root / "reports" / "lighthouse"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def inspect(self) -> dict:
        checks = [
            self._check_lightweight_init(),
            self._check_runtime_exists(),
            self._check_guardian_exists(),
            self._check_conclave_exists(),
            self._check_watch_tower_exists(),
            self._check_sentinel_exists(),
        ]

        failed = [check for check in checks if not check["passed"]]

        result = {
            "lighthouse": {
                "version": self.VERSION,
                "timestamp": datetime.utcnow().isoformat(),
                "root": str(self.root),
                "status": "healthy" if not failed else "degraded",
                "checks": checks,
                "failed": failed,
            }
        }

        self._write_reports(result)
        return result

    def _check_lightweight_init(self) -> dict:
        path = self.root / "aletheus" / "__init__.py"
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""

        forbidden = [
            "from aletheus.runtime import",
            "runtime_core",
            "streamlit",
            "subprocess.run",
        ]

        passed = path.exists() and not any(item in text for item in forbidden)

        return {
            "name": "lightweight_package_init",
            "passed": passed,
            "message": "aletheus/__init__.py is lightweight." if passed else "aletheus/__init__.py may still trigger runtime boot side effects.",
            "path": str(path),
        }

    def _check_runtime_exists(self) -> dict:
        return self._exists("aletheus_runtime", self.root / "aletheus" / "runtime")

    def _check_guardian_exists(self) -> dict:
        return self._exists("guardian", self.root / "aletheus" / "runtime" / "guardian")

    def _check_conclave_exists(self) -> dict:
        return self._exists("conclave", self.root / "aletheus" / "runtime" / "conclave")

    def _check_watch_tower_exists(self) -> dict:
        return self._exists("watch_tower", self.root / "watch_tower")

    def _check_sentinel_exists(self) -> dict:
        return self._exists("sentinel", self.root / "aletheus" / "runtime" / "sentinel")

    def _exists(self, name: str, path: Path) -> dict:
        return {
            "name": name,
            "passed": path.exists(),
            "message": f"{name} exists." if path.exists() else f"{name} is missing.",
            "path": str(path),
        }

    def _write_reports(self, result: dict):
        json_path = self.report_dir / "lighthouse_report.json"
        md_path = self.report_dir / "lighthouse_report.md"

        json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        md_path.write_text(self._markdown(result), encoding="utf-8")

    def _markdown(self, result: dict) -> str:
        lighthouse = result["lighthouse"]

        lines = [
            "# Project Lighthouse Report",
            "",
            f"Generated: {lighthouse['timestamp']}",
            f"Status: **{lighthouse['status']}**",
            "",
            "## Checks",
            "",
        ]

        for check in lighthouse["checks"]:
            mark = "PASS" if check["passed"] else "FAIL"
            lines.append(f"- **{mark}** — {check['name']}: {check['message']}")

        return "\n".join(lines)
