"""Identity and authorization policy for the Experience Gateway."""

from .auth_config import (
    AuthenticationConfig,
    load_authentication_config,
)
from .auth_factory import (
    create_principal_authenticator,
)
from .contracts import (
    AuthorizationDecision,
    AuthorizationPolicy,
    Principal,
    PrincipalRole,
)
from .default_policy import (
    create_default_authorization_policy,
)
from .resolver import PrincipalResolver

__all__ = [
    "AuthenticationConfig",
    "AuthorizationDecision",
    "AuthorizationPolicy",
    "Principal",
    "PrincipalResolver",
    "PrincipalRole",
    "create_default_authorization_policy",
    "create_principal_authenticator",
    "load_authentication_config",
]
