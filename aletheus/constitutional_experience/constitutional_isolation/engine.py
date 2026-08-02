from dataclasses import dataclass

from ..models import ExperienceView


@dataclass(frozen=True, slots=True)
class AccessDecision:
    allowed: bool
    reason: str


class Engine:
    FOUNDER = frozenset(
        {
            "platform_omniscience",
            "constitutional_root",
            "cross_tenant_observatory",
            "developer_activity_totality",
            "admin_activity_totality",
        }
    )

    def authorize(
        self, view: ExperienceView, capability: str, root_attested: bool
    ) -> AccessDecision:
        if capability not in self.FOUNDER:
            return AccessDecision(True, "bounded-capability")
        if view is ExperienceView.FOUNDER and root_attested:
            return AccessDecision(True, "founder-root-attested")
        return AccessDecision(False, "constitutionally-isolated")
