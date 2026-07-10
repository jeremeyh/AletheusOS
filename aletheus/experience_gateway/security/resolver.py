from __future__ import annotations

from fastapi import (
    Header,
    HTTPException,
    status,
)

from .authenticator import PrincipalAuthenticator
from .contracts import Principal
from .oidc_authenticator import (
    AuthenticationFailure,
)


class PrincipalResolver:
    def __init__(
        self,
        authenticator: PrincipalAuthenticator,
    ) -> None:
        self._authenticator = authenticator

    def dependency(
        self,
        authorization: str | None = Header(
            default=None
        ),
    ) -> Principal:
        credential = _bearer_token(
            authorization
        )

        try:
            return self._authenticator.authenticate(
                credential
            )
        except AuthenticationFailure as error:
            raise HTTPException(
                status_code=(
                    status.HTTP_401_UNAUTHORIZED
                ),
                detail=str(error),
                headers={
                    "WWW-Authenticate": "Bearer",
                },
            ) from error
        except ValueError as error:
            raise HTTPException(
                status_code=(
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=(
                    "Authentication configuration "
                    f"is invalid: {error}"
                ),
            ) from error


def _bearer_token(
    authorization: str | None,
) -> str | None:
    if authorization is None:
        return None

    scheme, separator, credential = (
        authorization.partition(" ")
    )

    if (
        not separator
        or scheme.lower() != "bearer"
        or not credential.strip()
    ):
        raise HTTPException(
            status_code=401,
            detail=(
                "Authorization must use the "
                "Bearer scheme."
            ),
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    return credential.strip()
