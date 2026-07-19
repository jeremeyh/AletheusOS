"""Security Civilization institution phase executors."""

from __future__ import annotations

from typing import Any

from aletheus.constitutional_events.security import (
    SecurityEventType,
)

from .contracts import (
    PhaseExecutionRequest,
    PhaseExecutionResult,
)


def _mapping(value: Any) -> dict[str, Any]:
    """Normalize an institutional result into a dictionary."""

    if value is None:
        return {}

    if isinstance(value, dict):
        return dict(value)

    if hasattr(value, "to_dict"):
        result = value.to_dict()

        if isinstance(result, dict):
            return dict(result)

    return {
        "value": value,
    }


class WatchTowerPhaseExecutor:
    """
    Executes the Detect phase.

    IntegrityFindingCreated is emitted by the Civilization Orchestrator because
    it is the originating fact that caused the Case and Mission. This executor
    therefore returns evidence without publishing that event a second time.
    """

    institution_id = "aletheus.watch_tower"

    def __init__(
        self,
        watch_tower: Any | None = None,
    ) -> None:
        self.watch_tower = watch_tower

    def execute(
        self,
        request: PhaseExecutionRequest,
    ) -> PhaseExecutionResult:
        finding = dict(
            request.context.get("finding") or {}
        )

        if self.watch_tower is not None:
            if hasattr(self.watch_tower, "verify"):
                output = _mapping(
                    self.watch_tower.verify()
                )

            elif hasattr(self.watch_tower, "analyze"):
                output = _mapping(
                    self.watch_tower.analyze(
                        request.context
                    )
                )

            else:
                raise TypeError(
                    "Watch Tower exposes no verify or analyze method."
                )

        else:
            output = {
                "verified": True,
                "finding": finding,
                "adapter": "constitutional_default",
            }

        return PhaseExecutionResult(
            institution_id=self.institution_id,
            phase_id=request.phase_id,
            evidence_type="integrity_finding",
            evidence={
                "entity_id": request.context[
                    "entity_id"
                ],
                "severity": request.context[
                    "severity"
                ],
                "finding": finding,
                "watch_tower": output,
            },
        )


class GuardianPhaseExecutor:
    """Execute threat classification through Guardian™."""

    institution_id = "aletheus.guardian"

    def __init__(
        self,
        guardian: Any | None = None,
    ) -> None:
        self.guardian = guardian

    def execute(
        self,
        request: PhaseExecutionRequest,
    ) -> PhaseExecutionResult:
        if self.guardian is not None:
            if hasattr(self.guardian, "classify"):
                output = _mapping(
                    self.guardian.classify(
                        request.inputs
                    )
                )

            elif hasattr(self.guardian, "evaluate"):
                output = _mapping(
                    self.guardian.evaluate(
                        request.inputs
                    )
                )

            else:
                raise TypeError(
                    "Guardian exposes no classify or evaluate method."
                )

        else:
            output = {
                "classification": "unverified_threat",
                "severity": request.context[
                    "severity"
                ],
                "strategy": "contain",
                "adapter": "constitutional_default",
            }

        return PhaseExecutionResult(
            institution_id=self.institution_id,
            phase_id=request.phase_id,
            evidence_type="threat_classification",
            evidence=output,
            domain_event_type=(
                SecurityEventType
                .THREAT_CLASSIFIED
            ),
            domain_event_tags=(
                "security",
                "classification",
                request.context[
                    "severity"
                ].casefold(),
            ),
        )


class ConclavePhaseExecutor:
    """Execute constitutional containment through Conclave™."""

    institution_id = "aletheus.conclave"

    def __init__(
        self,
        conclave: Any | None = None,
    ) -> None:
        self.conclave = conclave

    def execute(
        self,
        request: PhaseExecutionRequest,
    ) -> PhaseExecutionResult:
        if self.conclave is not None:
            if hasattr(self.conclave, "contain"):
                output = _mapping(
                    self.conclave.contain(
                        request.inputs
                    )
                )

            elif hasattr(self.conclave, "isolate"):
                output = _mapping(
                    self.conclave.isolate(
                        request.inputs
                    )
                )

            else:
                raise TypeError(
                    "Conclave exposes no contain or isolate method."
                )

        else:
            output = {
                "contained": True,
                "boundary": (
                    "default_secure_boundary"
                ),
                "entity_id": request.context[
                    "entity_id"
                ],
                "adapter": "constitutional_default",
            }

        return PhaseExecutionResult(
            institution_id=self.institution_id,
            phase_id=request.phase_id,
            evidence_type="containment_result",
            evidence=output,
            domain_event_type=(
                SecurityEventType
                .ENTITY_QUARANTINED
            ),
            domain_event_tags=(
                "security",
                "containment",
                "quarantine",
            ),
        )


class ContainmentVaultPhaseExecutor:
    """Execute forensic preservation through Containment Vault™."""

    institution_id = (
        "aletheus.containment_vault"
    )

    def __init__(
        self,
        containment_vault: Any | None = None,
    ) -> None:
        self.containment_vault = (
            containment_vault
        )

    def execute(
        self,
        request: PhaseExecutionRequest,
    ) -> PhaseExecutionResult:
        if self.containment_vault is not None:
            if hasattr(
                self.containment_vault,
                "preserve",
            ):
                output = _mapping(
                    self.containment_vault.preserve(
                        request.inputs
                    )
                )

            elif hasattr(
                self.containment_vault,
                "store",
            ):
                output = _mapping(
                    self.containment_vault.store(
                        request.inputs
                    )
                )

            else:
                raise TypeError(
                    "Containment Vault exposes no "
                    "preserve or store method."
                )

        else:
            output = {
                "preserved": True,
                "chain_of_custody": True,
                "vault": "containment_vault",
                "adapter": "constitutional_default",
            }

        return PhaseExecutionResult(
            institution_id=self.institution_id,
            phase_id=request.phase_id,
            evidence_type="forensic_preservation",
            evidence=output,
            domain_event_type=(
                SecurityEventType
                .EVIDENCE_PRESERVED
            ),
            domain_event_tags=(
                "security",
                "forensics",
                "chain-of-custody",
            ),
        )


class SentinelPhaseExecutor:
    """Execute operational stabilization through Sentinel™."""

    institution_id = "aletheus.sentinel"

    def __init__(
        self,
        sentinel: Any | None = None,
    ) -> None:
        self.sentinel = sentinel

    def execute(
        self,
        request: PhaseExecutionRequest,
    ) -> PhaseExecutionResult:
        if self.sentinel is not None:
            if hasattr(
                self.sentinel,
                "stabilize",
            ):
                output = _mapping(
                    self.sentinel.stabilize(
                        request.inputs
                    )
                )

            elif hasattr(
                self.sentinel,
                "protect",
            ):
                output = _mapping(
                    self.sentinel.protect(
                        request.inputs
                    )
                )

            else:
                raise TypeError(
                    "Sentinel exposes no stabilize "
                    "or protect method."
                )

        else:
            output = {
                "stabilized": True,
                "monitoring": "active",
                "adapter": "constitutional_default",
            }

        return PhaseExecutionResult(
            institution_id=self.institution_id,
            phase_id=request.phase_id,
            evidence_type="stabilization_result",
            evidence=output,
            domain_event_type=(
                SecurityEventType
                .SECURITY_INCIDENT_STABILIZED
            ),
            domain_event_tags=(
                "security",
                "runtime",
                "stabilized",
            ),
        )


def register_security_executors(
    registry,
    *,
    watch_tower: Any | None = None,
    guardian: Any | None = None,
    conclave: Any | None = None,
    containment_vault: Any | None = None,
    sentinel: Any | None = None,
):
    """Register the canonical Security Civilization phase executors."""

    registry.register(
        WatchTowerPhaseExecutor(
            watch_tower
        )
    )
    registry.register(
        GuardianPhaseExecutor(
            guardian
        )
    )
    registry.register(
        ConclavePhaseExecutor(
            conclave
        )
    )
    registry.register(
        ContainmentVaultPhaseExecutor(
            containment_vault
        )
    )
    registry.register(
        SentinelPhaseExecutor(
            sentinel
        )
    )

    return registry
