from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import jwt
from jwt import (
    ExpiredSignatureError,
    InvalidAudienceError,
    InvalidIssuerError,
    InvalidTokenError,
    PyJWKClient,
)

from .auth_config import AuthenticationConfig
from .contracts import Principal, PrincipalRole


_ALLOWED_ROLES: set[str] = {
    "viewer",
    "operator",
    "administrator",
    "platform_architect",
}


class AuthenticationFailure(Exception):
    """A bearer credential could not be authenticated."""


class OIDCPrincipalAuthenticator:
    def __init__(
        self,
        config: AuthenticationConfig,
    ) -> None:
        if config.mode != "oidc":
            raise ValueError(
                "OIDC authenticator requires OIDC mode."
            )

        assert config.jwks_url is not None

        self._config = config
        self._jwk_client = PyJWKClient(
            config.jwks_url,
            cache_jwk_set=True,
        )

    def authenticate(
        self,
        credential: str | None,
    ) -> Principal:
        if not credential:
            raise AuthenticationFailure(
                "A bearer access token is required."
            )

        try:
            signing_key = (
                self._jwk_client
                .get_signing_key_from_jwt(
                    credential
                )
            )

            claims = jwt.decode(
                credential,
                signing_key.key,
                algorithms=list(
                    self._config.algorithms
                ),
                audience=self._config.audience,
                issuer=self._config.issuer,
                leeway=(
                    self._config
                    .clock_skew_seconds
                ),
                options={
                    "require": [
                        "exp",
                        "iat",
                        "iss",
                        "sub",
                    ],
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iat": True,
                    "verify_iss": True,
                    "verify_aud": True,
                },
            )
        except ExpiredSignatureError as error:
            raise AuthenticationFailure(
                "The access token has expired."
            ) from error
        except InvalidAudienceError as error:
            raise AuthenticationFailure(
                "The access token audience is invalid."
            ) from error
        except InvalidIssuerError as error:
            raise AuthenticationFailure(
                "The access token issuer is invalid."
            ) from error
        except InvalidTokenError as error:
            raise AuthenticationFailure(
                f"The access token is invalid: {error}"
            ) from error
        except Exception as error:
            raise AuthenticationFailure(
                "The signing key could not be resolved."
            ) from error

        return self._principal_from_claims(
            claims
        )

    def _principal_from_claims(
        self,
        claims: Mapping[str, Any],
    ) -> Principal:
        subject = _required_text_claim(
            claims,
            self._config.subject_claim,
        )

        display_name = _optional_text_claim(
            claims,
            self._config.display_name_claim,
        ) or subject

        roles = self._map_roles(
            _claim_values(
                claims.get(
                    self._config.roles_claim
                )
            )
        )

        entitlements = _claim_values(
            claims.get(
                self._config
                .entitlements_claim
            )
        )

        return Principal(
            subject_id=subject,
            display_name=display_name,
            roles=roles,
            entitlements=entitlements,
            authentication_method="oidc_jwt",
            authenticated=True,
            attributes={
                "issuer": str(
                    claims.get("iss", "")
                ),
                "tokenId": str(
                    claims.get("jti", "")
                ),
            },
        )

    @staticmethod
    def _map_roles(
        claim_values: tuple[str, ...],
    ) -> tuple[PrincipalRole, ...]:
        normalized = tuple(
            value.strip().lower()
            for value in claim_values
            if value.strip().lower()
            in _ALLOWED_ROLES
        )

        if not normalized:
            return ("viewer",)

        return normalized  # type: ignore[return-value]


def _required_text_claim(
    claims: Mapping[str, Any],
    claim_name: str,
) -> str:
    value = _optional_text_claim(
        claims,
        claim_name,
    )

    if value is None:
        raise AuthenticationFailure(
            f"Required token claim is missing: "
            f"{claim_name}"
        )

    return value


def _optional_text_claim(
    claims: Mapping[str, Any],
    claim_name: str,
) -> str | None:
    value = claims.get(claim_name)

    if not isinstance(value, str):
        return None

    normalized = value.strip()
    return normalized or None


def _claim_values(
    value: Any,
) -> tuple[str, ...]:
    if value is None:
        return ()

    if isinstance(value, str):
        return tuple(
            entry.strip()
            for entry in value.replace(
                ",",
                " ",
            ).split()
            if entry.strip()
        )

    if isinstance(value, list):
        return tuple(
            str(entry).strip()
            for entry in value
            if str(entry).strip()
        )

    return ()
