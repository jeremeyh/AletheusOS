from __future__ import annotations


class Engine:
    def profile(
        self, primary: str, second: str | None, session_age: int
    ) -> dict[str, object]:
        strong = primary.upper() in {"PASSKEY", "WEBAUTHN", "HARDWARE_KEY"}
        return {
            "twoFactorSatisfied": strong or bool(second),
            "phishingResistant": strong,
            "stepUpRequired": session_age > 900,
            "atRest": "AES-256-GCM",
            "transport": "TLS-1.3",
            "passwordStorage": "ARGON2ID",
            "keyCustody": "HSM_OR_KMS",
        }
