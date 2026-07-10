from __future__ import annotations

import os

from .contracts import Principal, PrincipalRole


_ALLOWED_ROLES: set[str] = {
    "viewer",
    "operator",
    "administrator",
    "platform_architect",
}


class LocalPrincipalAuthenticator:
    def authenticate(
        self,
        credential: str | None,
    ) -> Principal:
        del credential

        roles = _parse_roles(
            os.getenv(
                "ALETHEUS_LOCAL_ROLES",
                "platform_architect",
            )
        )

        entitlements = _parse_values(
            os.getenv(
                "ALETHEUS_LOCAL_ENTITLEMENTS",
                (
                    "runtime.read,"
                    "providers.refresh,"
                    "experience.preferences.write"
                ),
            )
        )

        return Principal(
            subject_id=os.getenv(
                "ALETHEUS_LOCAL_SUBJECT",
                "local:jeremey",
            ).strip(),
            display_name=os.getenv(
                "ALETHEUS_LOCAL_DISPLAY_NAME",
                "Jeremey",
            ).strip(),
            roles=roles,
            entitlements=entitlements,
            authentication_method=(
                "local_environment"
            ),
            authenticated=True,
        )


def _parse_roles(
    value: str,
) -> tuple[PrincipalRole, ...]:
    parsed = _parse_values(value)

    invalid = [
        role
        for role in parsed
        if role not in _ALLOWED_ROLES
    ]

    if invalid:
        raise ValueError(
            "Unsupported local role(s): "
            + ", ".join(invalid)
        )

    if not parsed:
        return ("viewer",)

    return tuple(parsed)  # type: ignore[return-value]


def _parse_values(
    value: str,
) -> tuple[str, ...]:
    return tuple(
        entry.strip()
        for entry in value.split(",")
        if entry.strip()
    )
