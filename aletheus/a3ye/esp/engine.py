from __future__ import annotations

from dataclasses import replace

from .models import GovernedEvidence, SignalEnvelope


class Engine:
    SENSITIVE_KEYS = frozenset(
        {"ssn", "social_security_number", "credit_card", "cvv", "password"}
    )

    def process(self, signal: SignalEnvelope) -> GovernedEvidence:
        if not signal.consent and signal.modality in {"voice", "biometric", "video"}:
            raise PermissionError("ESP_POLICY_VIOLATION: consent required")
        clean = {
            key: "[REDACTED]" if key.lower() in self.SENSITIVE_KEYS else value
            for key, value in signal.payload.items()
        }
        confidence = min(1.0, max(0.0, signal.confidence))
        return GovernedEvidence(
            f"evidence:{signal.signal_id}",
            signal.modality,
            clean,
            signal.provenance,
            confidence,
            1.0 - confidence,
            ("ESP_ENFORCED", "RAW_SIGNAL_MINIMIZED"),
        )

    def minimize(self, evidence: GovernedEvidence) -> GovernedEvidence:
        blocked = {"raw_pcm", "raw_image", "keystroke_timing"}
        return replace(
            evidence,
            content={k: v for k, v in evidence.content.items() if k not in blocked},
        )
