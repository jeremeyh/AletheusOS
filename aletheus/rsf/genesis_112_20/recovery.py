from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Awaitable, Callable
from .common import utc_now_iso, sha256_digest

class RecoveryPhase(str, Enum):
    DETECTED = "DETECTED"
    ISOLATED = "ISOLATED"
    RESTORING = "RESTORING"
    VERIFYING = "VERIFYING"
    RECOVERED = "RECOVERED"
    FAILED = "FAILED"

@dataclass(frozen=True)
class RecoveryStep:
    step_id: str
    description: str

@dataclass(frozen=True)
class RecoveryPlan:
    recovery_id: str
    component_id: str
    failure_domain: str
    steps: tuple[RecoveryStep, ...]
    requires_external_authority: bool = False

@dataclass(frozen=True)
class RecoveryResult:
    recovery_id: str
    recovered: bool
    phase: RecoveryPhase
    started_at_iso: str
    completed_at_iso: str
    action_success: bool
    verification_success: bool
    evidence_digest: str
    error: str = ""

class RSFRecoveryContinuityEngine:
    @staticmethod
    async def execute(
        plan: RecoveryPlan,
        remediation: Callable[[], Awaitable[bool]],
        verify: Callable[[], Awaitable[bool]],
        *,
        authority_granted: bool = False,
    ) -> RecoveryResult:
        started = utc_now_iso()
        if plan.requires_external_authority and not authority_granted:
            body = {
                "recoveryId": plan.recovery_id,
                "phase": RecoveryPhase.FAILED.value,
                "reason": "external authority not granted",
            }
            return RecoveryResult(
                plan.recovery_id, False, RecoveryPhase.FAILED, started, utc_now_iso(),
                False, False, sha256_digest(body), "external authority not granted"
            )
        try:
            action_success = bool(await remediation())
        except Exception as exc:
            action_success = False
            error = f"remediation exception: {exc}"
        else:
            error = ""

        verification_success = False
        if action_success:
            try:
                verification_success = bool(await verify())
            except Exception as exc:
                error = f"verification exception: {exc}"

        recovered = action_success and verification_success
        phase = RecoveryPhase.RECOVERED if recovered else RecoveryPhase.FAILED
        completed = utc_now_iso()
        body = {
            "recoveryId": plan.recovery_id,
            "componentId": plan.component_id,
            "failureDomain": plan.failure_domain,
            "actionSuccess": action_success,
            "verificationSuccess": verification_success,
            "phase": phase.value,
        }
        return RecoveryResult(
            plan.recovery_id, recovered, phase, started, completed,
            action_success, verification_success, sha256_digest(body), error
        )
