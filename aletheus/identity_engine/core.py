from __future__ import annotations

from .authentication import identity_authentication
from .authorization import identity_authorization
from .health import identity_health
from .models import Identity
from .registry import identity_registry
from .resolver import identity_resolver
from .sessions import session_manager
from .statistics import identity_statistics


class IdentityEngine:
    GENESIS = "21.7"
    VERSION = "1.0.0"

    def __init__(self):
        self.registry = identity_registry
        self.resolver = identity_resolver
        self.authentication = identity_authentication
        self.authorization = identity_authorization
        self.sessions = session_manager
        self.statistics = identity_statistics

        self._bootstrap()

    def _bootstrap(self):
        founder = Identity(
            identity_id="identity.founder.master_lord_6ixth",
            identity_type="founder",
            display_name="Master Lord 6iXth",
            profile_id="founder",
            organization="6th Dimension Multimedia",
            application="AletheusOS",
            aliases=[
                "Jeremey",
                "Jeremey Harvey",
                "Master Lord 6iXth",
            ],
        )

        if not self.registry.get(founder.identity_id):
            self.registry.register(founder)
            self.statistics.record_identity()

    def resolve(self, value: str):
        identity = self.resolver.resolve(value)

        if identity:
            self.statistics.record_alias_resolution()

        return identity

    def authenticate(self, value: str):
        identity = self.resolve(value)
        result = self.authentication.authenticate(identity)

        self.statistics.record_authentication()

        return result

    def authorize(
        self,
        value: str,
        required_profile: str,
    ):
        identity = self.resolve(value)
        result = self.authorization.authorize(
            identity,
            required_profile,
        )

        self.statistics.record_authorization()

        return result

    def create_session(self, value: str):
        identity = self.resolve(value)

        if identity is None:
            return None

        session = self.sessions.create(identity.identity_id)
        self.statistics.record_session()

        return session

    def health(self):
        return identity_health.report()


identity_engine = IdentityEngine()
