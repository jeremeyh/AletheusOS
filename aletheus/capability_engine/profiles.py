from __future__ import annotations

from .models import CapabilityProfile


class FoundationProfiles:
    """
    Canonical constitutional capability profiles.

    These represent AletheusOS Foundation identities.
    Applications inherit from these profiles rather than
    redefining constitutional authority.
    """

    GENESIS = "21.6"
    VERSION = "1.0.0"

    def __init__(self):
        self._profiles: dict[str, CapabilityProfile] = {}
        self._bootstrap()

    def _bootstrap(self):

        self.register(
            CapabilityProfile(
                profile_id="consumer",
                name="Consumer",
                description="Default constitutional identity.",
            )
        )

        self.register(
            CapabilityProfile(
                profile_id="pro",
                name="Professional",
                description="Professional creator.",
                inherits=["consumer"],
            )
        )

        self.register(
            CapabilityProfile(
                profile_id="business",
                name="Business",
                description="Business owner or operator.",
                inherits=["pro"],
            )
        )

        self.register(
            CapabilityProfile(
                profile_id="enterprise",
                name="Enterprise",
                description="Enterprise organization administrator.",
                inherits=["business"],
            )
        )

        self.register(
            CapabilityProfile(
                profile_id="developer",
                name="Developer",
                description="Application developer.",
                inherits=["pro"],
            )
        )

        self.register(
            CapabilityProfile(
                profile_id="platform_engineer",
                name="Platform Engineer",
                description="Foundation engineering authority.",
                inherits=["developer"],
            )
        )

        self.register(
            CapabilityProfile(
                profile_id="founder",
                name="Founder",
                description="Constitutional platform authority.",
                inherits=["platform_engineer"],
            )
        )

        self.register(
            CapabilityProfile(
                profile_id="platform",
                name="Platform",
                description="Internal runtime identity.",
                inherits=["founder"],
            )
        )

    def register(self, profile: CapabilityProfile):
        self._profiles[profile.profile_id] = profile
        return profile

    def get(self, profile_id: str):
        return self._profiles.get(profile_id)

    def all(self):
        return list(self._profiles.values())

    def to_dict(self):
        return [profile.to_dict() for profile in self.all()]

    def statistics(self):
        return {
            "profiles": len(self._profiles),
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }

    def health(self):
        return {
            "status": "healthy",
            "profiles": len(self._profiles),
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }


foundation_profiles = FoundationProfiles()
