from __future__ import annotations


class IdentityStatistics:

    GENESIS = "21.7"
    VERSION = "1.0.0"

    def __init__(self):
        self.reset()

    def reset(self):

        self.identities = 0
        self.authentications = 0
        self.authorizations = 0
        self.sessions = 0
        self.alias_resolutions = 0

    def record_identity(self):
        self.identities += 1

    def record_authentication(self):
        self.authentications += 1

    def record_authorization(self):
        self.authorizations += 1

    def record_session(self):
        self.sessions += 1

    def record_alias_resolution(self):
        self.alias_resolutions += 1

    def snapshot(self):

        return {
            "identities": self.identities,
            "authentications": self.authentications,
            "authorizations": self.authorizations,
            "sessions": self.sessions,
            "alias_resolutions": self.alias_resolutions,
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }

    def health(self):

        return {
            "status": "healthy",
            **self.snapshot(),
        }


identity_statistics = IdentityStatistics()
