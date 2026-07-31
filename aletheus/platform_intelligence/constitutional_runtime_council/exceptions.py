"""Exceptions for the Constitutional Runtime Council."""

from __future__ import annotations


class ConstitutionalRuntimeCouncilError(Exception):
    """Base exception for CRC failures."""


class CouncilMemberAlreadyExistsError(ConstitutionalRuntimeCouncilError):
    """Raised when a council member already exists."""


class CouncilMemberNotFoundError(ConstitutionalRuntimeCouncilError):
    """Raised when a council member cannot be found."""


class CouncilProposalAlreadyExistsError(ConstitutionalRuntimeCouncilError):
    """Raised when a proposal already exists."""


class CouncilProposalNotFoundError(ConstitutionalRuntimeCouncilError):
    """Raised when a proposal cannot be found."""


class CouncilVotingError(ConstitutionalRuntimeCouncilError):
    """Raised when voting is invalid."""


class CouncilDecisionError(ConstitutionalRuntimeCouncilError):
    """Raised when a proposal cannot be decided."""
