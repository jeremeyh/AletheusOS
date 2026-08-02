from __future__ import annotations


class Engine:
    def authorize(
        self, mfa: bool, assurance: int, device_trust: float, risk: float, amount: float
    ) -> dict[str, object]:
        reasons = []
        if not mfa:
            reasons.append("MFA_REQUIRED")
        if assurance < 2:
            reasons.append("IDENTITY_ASSURANCE_TOO_LOW")
        if device_trust < 0.6:
            reasons.append("DEVICE_TRUST_TOO_LOW")
        if risk > 0.7:
            reasons.append("TRANSACTION_RISK_TOO_HIGH")
        if amount >= 1000 and assurance < 3:
            reasons.append("STEP_UP_REQUIRED")
        return {"authorized": not reasons, "reasons": tuple(reasons), "conclaveOnFailure": True}
