from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path


class CouncilEngine:
    """
    Council™

    Governance coordinator for AletheusOS.

    Council does not replace Atlas, Sentinel, Guardian, Watch Tower,
    Conclave, Lighthouse, or Platform Layer.

    It reviews their reports and produces one traceable recommendation.
    """

    VERSION = "1.0.0"

    def __init__(self, root="."):
        self.root = Path(root).resolve()
        self.report_dir = self.root / "reports" / "council"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def review(self, proposal: str, source: str = "manual") -> dict:
        inputs = {
            "lighthouse": self._load_json("reports/lighthouse/lighthouse_report.json"),
            "platform": self._load_json("reports/platform/platform_report.json"),
            "sentinel": self._load_json("reports/sentinel/sentinel_report.json"),
            "atlas": self._load_json("reports/atlas/atlas_report.json"),
            "watch_tower": self._load_json("reports/watch_tower/watch_tower_report.json"),
            "guardian": self._load_json("reports/guardian/guardian_report.json"),
        }

        assessments = self._assess(inputs)

        decision = self._decision(assessments, proposal)

        result = {
            "council": {
                "version": self.VERSION,
                "timestamp": datetime.utcnow().isoformat(),
                "root": str(self.root),
                "source": source,
                "proposal": proposal,
                "assessments": assessments,
                "decision": decision,
            }
        }

        self._write_reports(result)
        return result

    def _load_json(self, relative_path: str) -> dict:
        path = self.root / relative_path

        if not path.exists():
            return {
                "available": False,
                "path": str(path),
                "message": "Report not found.",
            }

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            return {
                "available": False,
                "path": str(path),
                "message": f"Unable to read report: {exc}",
            }

    def _assess(self, inputs: dict) -> dict:
        return {
            "lighthouse": self._status_score(inputs, "lighthouse"),
            "platform": self._status_score(inputs, "platform"),
            "sentinel": self._status_score(inputs, "sentinel"),
            "atlas": self._status_score(inputs, "atlas"),
            "watch_tower": self._status_score(inputs, "watch_tower"),
            "guardian": self._guardian_status(inputs.get("guardian", {})),
        }

    def _status_score(self, inputs: dict, key: str) -> dict:
        payload = inputs.get(key, {})

        if not payload.get("available", True):
            return {
                "available": False,
                "status": "missing",
                "score": 0,
                "message": payload.get("message", "Missing report."),
            }

        data = payload.get(key, payload)

        return {
            "available": True,
            "status": data.get("status", "unknown"),
            "score": data.get("score", None),
            "message": "Report loaded.",
        }

    def _guardian_status(self, payload: dict) -> dict:
        if not payload.get("available", True):
            return {
                "available": False,
                "status": "missing",
                "allowed": None,
                "risk": "unknown",
                "message": payload.get("message", "Missing Guardian report."),
            }

        guardian = payload.get("guardian", payload)
        decision = guardian.get("decision", {})
        event = guardian.get("event", {})

        return {
            "available": True,
            "status": "loaded",
            "allowed": decision.get("allowed"),
            "risk": event.get("risk", "unknown"),
            "message": decision.get("message", "Guardian report loaded."),
        }

    def _decision(self, assessments: dict, proposal: str) -> dict:
        blockers = []
        warnings = []

        for name, assessment in assessments.items():
            status = assessment.get("status")
            score = assessment.get("score")

            if not assessment.get("available"):
                warnings.append(f"{name} report missing.")

            if status in {"critical"}:
                blockers.append(f"{name} is critical.")

            if status in {"degraded"}:
                warnings.append(f"{name} is degraded.")

            if isinstance(score, int) and score < 80:
                warnings.append(f"{name} score below 80.")

        guardian = assessments.get("guardian", {})
        if guardian.get("risk") in {"critical", "high"}:
            warnings.append(f"Guardian recent risk is {guardian.get('risk')}.")

        proposal_lower = proposal.lower()

        if any(token in proposal_lower for token in ["delete vault", "wipe", "destroy", "remove protected"]):
            blockers.append("Proposal appears destructive against protected resources.")

        if blockers:
            return {
                "approved": False,
                "mode": "rejected",
                "confidence": 95,
                "blockers": blockers,
                "warnings": warnings,
                "principle_x": True,
                "message": "Council rejects this proposal because one or more blockers were detected.",
            }

        if warnings:
            return {
                "approved": True,
                "mode": "approved_with_warnings",
                "confidence": 82,
                "blockers": blockers,
                "warnings": warnings,
                "principle_x": False,
                "message": "Council approves with warnings. Review before applying major changes.",
            }

        return {
            "approved": True,
            "mode": "approved",
            "confidence": 96,
            "blockers": [],
            "warnings": [],
            "principle_x": False,
            "message": "Council approves this proposal.",
        }

    def _write_reports(self, result: dict):
        json_path = self.report_dir / "council_report.json"
        md_path = self.report_dir / "council_report.md"

        json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        md_path.write_text(self._markdown(result), encoding="utf-8")

    def _markdown(self, result: dict) -> str:
        council = result["council"]
        decision = council["decision"]

        lines = [
            "# Council™ Governance Report",
            "",
            f"Generated: {council['timestamp']}",
            f"Proposal: `{council['proposal']}`",
            "",
            "## Decision",
            "",
            f"- Approved: **{decision['approved']}**",
            f"- Mode: **{decision['mode']}**",
            f"- Confidence: **{decision['confidence']}**",
            f"- Principle X: **{decision['principle_x']}**",
            f"- Message: {decision['message']}",
            "",
            "## Warnings",
            "",
        ]

        if decision["warnings"]:
            for warning in decision["warnings"]:
                lines.append(f"- {warning}")
        else:
            lines.append("- None")

        lines.extend(["", "## Blockers", ""])

        if decision["blockers"]:
            for blocker in decision["blockers"]:
                lines.append(f"- {blocker}")
        else:
            lines.append("- None")

        return "\n".join(lines)
