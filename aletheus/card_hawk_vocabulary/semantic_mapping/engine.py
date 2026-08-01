from __future__ import annotations

from typing import ClassVar

from .models import CapabilityMapping


class Engine:
    DEFAULT_MAPPINGS: ClassVar[tuple[CapabilityMapping, ...]] = (
        CapabilityMapping(
            "Gathering Mesh",
            "Market Intelligence",
            "Field Vision",
            "Perceive the broader collectible landscape beyond the current asset.",
        ),
        CapabilityMapping(
            "Balance Engine",
            "Portfolio and Market Performance",
            "Scoreboard",
            "Summarize current standing without concealing uncertainty.",
        ),
        CapabilityMapping(
            "Memory Engine",
            "Private Collector Workspace",
            "Locker Room",
            "Preserve user-authorized collection context, plans, and preferences.",
        ),
        CapabilityMapping(
            "Evidence Engine",
            "Asset and Market Investigation",
            "Scouting Report",
            "Present traceable evidence supporting an asset or market thesis.",
        ),
        CapabilityMapping(
            "Temporal Graph",
            "Historical Market Review",
            "Game Film",
            "Reconstruct historical behavior and prior decision outcomes.",
        ),
        CapabilityMapping(
            "Predictive Engine",
            "Forward Market Outlook",
            "Horizon",
            "Project plausible future conditions while preserving the unknown.",
        ),
        CapabilityMapping(
            "THORᵡ",
            "Acquisition Governance",
            "Strike Zone",
            "Define constitutionally acceptable acquisition conditions.",
        ),
        CapabilityMapping(
            "Council",
            "High-Stakes Deliberation",
            "War Room",
            "Convene competing theses and preserve qualified minority views.",
        ),
        CapabilityMapping(
            "A•3ye",
            "Conversational Collectibles Intelligence",
            "Bridge",
            "Transform collector intent into governed, evidence-based understanding.",
        ),
        CapabilityMapping(
            "Knowledge Engine",
            "Comprehensive Market and Collection Map",
            "Atlas",
            "Connect assets, creators, players, franchises, categories, and markets.",
        ),
        CapabilityMapping(
            "Evidence Engine",
            "Continuous Opportunity Monitoring",
            "Radar",
            "Detect listings, changes, risks, and anomalies across the field.",
        ),
        CapabilityMapping(
            "Truth",
            "Provenance and Authenticity",
            "Provenance",
            "Expose origin, ownership, authenticity, and evidentiary lineage.",
        ),
    )

    def mappings(self) -> tuple[CapabilityMapping, ...]:
        return self.DEFAULT_MAPPINGS

    def experience_for(self, platform_capability: str) -> tuple[str, ...]:
        return tuple(
            mapping.experience_name
            for mapping in self.DEFAULT_MAPPINGS
            if mapping.platform_capability == platform_capability
        )
