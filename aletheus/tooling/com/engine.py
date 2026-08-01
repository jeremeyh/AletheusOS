from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from .models import CognitiveMeshReport, ConsensusRecord, EvidenceContribution
from .reporting import write_reports


class CognitiveMeshEngine:
    def __init__(self, input_path: Path, output: Path) -> None:
        self.input_path = input_path.resolve()
        self.output = output.resolve()

    def analyze(self) -> CognitiveMeshReport:
        payload = json.loads(self.input_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise TypeError("COM input must be a JSON object.")

        contributions: list[EvidenceContribution] = []
        grouped: dict[str, list[EvidenceContribution]] = defaultdict(list)
        raw = payload.get("contributions", [])
        if not isinstance(raw, list):
            raise TypeError("contributions must be a list.")

        for item in raw:
            if not isinstance(item, dict):
                continue
            contribution = EvidenceContribution(
                authority=str(item.get("authority", "unknown")),
                claim=str(item.get("claim", "")),
                confidence=float(item.get("confidence", 0.0)),
                disposition=str(item.get("disposition", "abstain")),
                source=str(item.get("source", "")),
            )
            contributions.append(contribution)
            grouped[contribution.claim].append(contribution)

        consensus: list[ConsensusRecord] = []
        unresolved: list[str] = []
        for topic, items in sorted(grouped.items()):
            support = [item for item in items if item.disposition == "support"]
            oppose = [item for item in items if item.disposition == "oppose"]
            abstain = [item for item in items if item.disposition == "abstain"]
            weighted_support = sum(item.confidence for item in support)
            weighted_oppose = sum(item.confidence for item in oppose)
            total = weighted_support + weighted_oppose

            if total == 0 or abs(weighted_support - weighted_oppose) < 0.15:
                status = "unresolved"
                unresolved.append(topic)
            elif weighted_support > weighted_oppose:
                status = "supported"
            else:
                status = "opposed"

            confidence = (
                abs(weighted_support - weighted_oppose) / total if total else 0.0
            )
            consensus.append(
                ConsensusRecord(
                    topic=topic,
                    status=status,
                    confidence=round(confidence, 3),
                    contributors=tuple(item.authority for item in support),
                    dissenters=tuple(item.authority for item in oppose),
                    abstentions=tuple(item.authority for item in abstain),
                    approval_required=True,
                )
            )

        report = CognitiveMeshReport(
            generated_at=datetime.now(UTC).isoformat(),
            contributions=contributions,
            consensus=consensus,
            unresolved_topics=unresolved,
        )
        write_reports(report, self.output)
        return report
