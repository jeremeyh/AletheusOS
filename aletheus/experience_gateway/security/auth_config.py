from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

AuthenticationMode = Literal[
    "local",
    "oidc",
]


@dataclass(frozen=True, slots=True)
class AuthenticationConfig:
    mode: AuthenticationMode
    issuer: str | None = None
    audience: str | None = None
    jwks_url: str | None = None
    algorithms: tuple[str, ...] = ("RS256",)
    subject_claim: str = "sub"
    display_name_claim: str = "name"
    roles_claim: str = "groups"
    entitlements_claim: str = "scp"
    allow_local_identity: bool = True
    clock_skew_seconds: int = 30

    def __post_init__(self) -> None:
        if self.mode == "oidc":
            required = {
                "issuer": self.issuer,
                "audience": self.audience,
                "jwks_url": self.jwks_url,
            }

            missing = [
                name
                for name, value in required.items()
                if not value
            ]

            if missing:
                raise ValueError(
                    "OIDC authentication requires: "
                    + ", ".join(missing)
                )


def load_authentication_config(
) -> AuthenticationConfig:
    raw_mode = os.getenv(
        "ALETHEUS_AUTH_MODE",
        "local",
    ).strip().lower()

    if raw_mode not in {
        "local",
        "oidc",
    }:
        raise ValueError(
            "ALETHEUS_AUTH_MODE must be "
            "'local' or 'oidc'."
        )

    mode: AuthenticationMode = raw_mode  # type: ignore[assignment]

    algorithms = tuple(
        algorithm.strip()
        for algorithm in os.getenv(
            "ALETHEUS_OIDC_ALGORITHMS",
            "RS256",
        ).split(",")
        if algorithm.strip()
    )

    return AuthenticationConfig(
        mode=mode,
        issuer=_optional_environment(
            "ALETHEUS_OIDC_ISSUER"
        ),
        audience=_optional_environment(
            "ALETHEUS_OIDC_AUDIENCE"
        ),
        jwks_url=_optional_environment(
            "ALETHEUS_OIDC_JWKS_URL"
        ),
        algorithms=algorithms or ("RS256",),
        subject_claim=os.getenv(
            "ALETHEUS_OIDC_SUBJECT_CLAIM",
            "sub",
        ).strip(),
        display_name_claim=os.getenv(
            "ALETHEUS_OIDC_DISPLAY_NAME_CLAIM",
            "name",
        ).strip(),
        roles_claim=os.getenv(
            "ALETHEUS_OIDC_ROLES_CLAIM",
            "groups",
        ).strip(),
        entitlements_claim=os.getenv(
            "ALETHEUS_OIDC_ENTITLEMENTS_CLAIM",
            "scp",
        ).strip(),
        allow_local_identity=_environment_bool(
            "ALETHEUS_ALLOW_LOCAL_IDENTITY",
            default=(mode == "local"),
        ),
        clock_skew_seconds=int(
            os.getenv(
                "ALETHEUS_OIDC_CLOCK_SKEW_SECONDS",
                "30",
            )
        ),
    )


def _optional_environment(
    name: str,
) -> str | None:
    value = os.getenv(name, "").strip()
    return value or None


def _environment_bool(
    name: str,
    *,
    default: bool,
) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    normalized = value.strip().lower()

    if normalized in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return True

    if normalized in {
        "0",
        "false",
        "no",
        "off",
    }:
        return False

    raise ValueError(
        f"{name} must contain a boolean value."
    )
