"""Minimal hosted proof application for AletheusOS."""

from __future__ import annotations

from typing import Any

from .models import ApplicationManifest


class ConstitutionalProofApplication:
    """
    Small reference application proving lifecycle and service injection.

    This is not Card Hawk™. It establishes the application-hosting contract
    before a flagship application adopts it.
    """

    manifest = ApplicationManifest(
        application_id="aletheus.proof_application",
        canonical_name=(
            "Aletheus Constitutional Proof Application™"
        ),
        version="0.1.0",
        owner="6th Dimension Multimedia",
        purpose=(
            "Prove constitutional application hosting, "
            "service injection, and lifecycle management."
        ),
        required_services=(
            "runtime",
            "security",
            "cases",
            "missions",
            "ledger",
        ),
        provided_capabilities=(
            "constitutional_application_proof",
        ),
        permissions=(
            "runtime:read",
            "security:execute",
            "cases:read",
            "missions:read",
            "ledger:read",
        ),
    )

    def __init__(self) -> None:
        self.services: dict[str, Any] = {}
        self.initialized = False
        self.running = False

    def initialize(
        self,
        services: dict[str, Any],
    ) -> None:
        self.services = dict(services)
        self.initialized = True

    def start(self) -> None:
        if not self.initialized:
            raise RuntimeError(
                "Application must initialize before start."
            )

        self.running = True

    def stop(self) -> None:
        self.running = False

    def health(self) -> dict[str, Any]:
        return {
            "name": self.manifest.canonical_name,
            "status": (
                "online"
                if self.running
                else "stopped"
            ),
            "initialized": self.initialized,
            "running": self.running,
            "services": sorted(
                self.services
            ),
        }
