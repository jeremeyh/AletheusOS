from __future__ import annotations

from .auth_config import AuthenticationConfig
from .authenticator import PrincipalAuthenticator
from .local_authenticator import (
    LocalPrincipalAuthenticator,
)
from .oidc_authenticator import (
    OIDCPrincipalAuthenticator,
)


def create_principal_authenticator(
    config: AuthenticationConfig,
) -> PrincipalAuthenticator:
    if config.mode == "local":
        return LocalPrincipalAuthenticator()

    return OIDCPrincipalAuthenticator(config)
