from __future__ import annotations

from abc import ABC, abstractmethod

from .models import VocabularyTerm


class VocabularyEngineBase(ABC):
    @abstractmethod
    def list_terms(self) -> tuple[VocabularyTerm, ...]:
        raise NotImplementedError

    def resolve(self, name: str) -> VocabularyTerm:
        normalized = name.strip().casefold()
        for term in self.list_terms():
            if term.name.casefold() == normalized:
                return term
            if normalized in {alias.casefold() for alias in term.aliases}:
                return term
        raise KeyError(f"Unknown vocabulary term: {name}")
