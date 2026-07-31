from __future__ import annotations

from typing import Protocol

from .contracts import Principal


class PrincipalAuthenticator(Protocol):
    def authenticate(
        self,
        credential: str | None,
    ) -> Principal: ...
