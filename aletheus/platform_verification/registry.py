from __future__ import annotations

from typing import Callable, List

from .models import VerificationResult


VerificationCheck = Callable[[], VerificationResult]


class VerificationRegistry:
    def __init__(self) -> None:
        self._checks: List[VerificationCheck] = []

    def register(self, check: VerificationCheck) -> None:
        self._checks.append(check)

    def run_all(self) -> list[VerificationResult]:
        return [check() for check in self._checks]
