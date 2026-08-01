from __future__ import annotations

from dataclasses import dataclass

from .models import DeterminationVector


@dataclass(frozen=True)
class VoicePolicy:
    state_evidence: bool = True
    state_inference: bool = True
    state_uncertainty: bool = True
    preserve_minority_opinions: bool = True


class Engine:
    def compose(
        self,
        *,
        thesis: str,
        determination: DeterminationVector,
        evidence_summary: str,
        uncertainty_summary: str,
        minority_opinions: tuple[str, ...] = (),
        policy: VoicePolicy | None = None,
    ) -> dict[str, object]:
        active = policy or VoicePolicy()
        sections = [thesis]
        if active.state_evidence:
            sections.append(f"Evidence: {evidence_summary}")
        if active.state_inference:
            sections.append(
                "Determination: This is a governed conclusion, not an absolute fact."
            )
        if active.state_uncertainty:
            sections.append(f"Uncertainty: {uncertainty_summary}")
        if active.preserve_minority_opinions and minority_opinions:
            sections.append("Minority views: " + " | ".join(minority_opinions))
        return {
            "voice": "\n\n".join(sections),
            "tone": "CONFIDENT_HUMBLE_CLEAR",
            "unconcealedTruth": True,
            "overallStrength": determination.overall_strength,
        }
