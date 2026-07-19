"""Immutable models for the Constitutional Runtime Council."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping
from uuid import UUID, uuid4


class CouncilMemberKind(StrEnum):
    """Canonical council-member kinds."""

    HUMAN = "human"
    SYSTEM = "system"
    ADVISORY = "advisory"


class CouncilProposalKind(StrEnum):
    """Canonical council proposal kinds."""

    POLICY_CHANGE = "policy_change"
    EMERGENCY_OVERRIDE = "emergency_override"
    RUNTIME_ACTION = "runtime_action"
    SERVICE_RETIREMENT = "service_retirement"
    CONSTITUTIONAL_AMENDMENT = "constitutional_amendment"
    GOVERNANCE_REVIEW = "governance_review"


class CouncilProposalState(StrEnum):
    """Canonical proposal lifecycle."""

    OPEN = "open"
    APPROVED = "approved"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class CouncilVoteChoice(StrEnum):
    """Canonical vote choices."""

    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"


class CouncilVotingStrategy(StrEnum):
    """Canonical voting strategies."""

    MAJORITY = "majority"
    SUPERMAJORITY = "supermajority"
    UNANIMOUS = "unanimous"


class CouncilDecisionOutcome(StrEnum):
    """Canonical council decision outcomes."""

    APPROVED = "approved"
    REJECTED = "rejected"
    INSUFFICIENT_QUORUM = "insufficient_quorum"


@dataclass(frozen=True, slots=True)
class ConstitutionalCouncilMember:
    """Immutable constitutional council member."""

    member_id: str
    display_name: str
    kind: CouncilMemberKind
    authority: str
    voting_weight: int = 1
    active: bool = True
    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        resolved = self.member_id.strip().lower()

        if not resolved:
            raise ValueError(
                "member_id cannot be empty."
            )

        if self.voting_weight < 1:
            raise ValueError(
                "voting_weight must be positive."
            )

        object.__setattr__(
            self,
            "member_id",
            resolved,
        )
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(
                dict(self.metadata)
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "member_id": self.member_id,
            "display_name": self.display_name,
            "kind": self.kind.value,
            "authority": self.authority,
            "voting_weight": self.voting_weight,
            "active": self.active,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class CouncilVote:
    """Immutable council vote."""

    vote_id: UUID
    proposal_id: UUID
    member_id: str
    choice: CouncilVoteChoice
    weight: int
    rationale: str
    cast_at: datetime

    @classmethod
    def create(
        cls,
        *,
        proposal_id: UUID,
        member: ConstitutionalCouncilMember,
        choice: CouncilVoteChoice,
        rationale: str = "",
    ) -> "CouncilVote":
        return cls(
            vote_id=uuid4(),
            proposal_id=proposal_id,
            member_id=member.member_id,
            choice=choice,
            weight=member.voting_weight,
            rationale=rationale.strip(),
            cast_at=datetime.now(UTC),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "vote_id": str(self.vote_id),
            "proposal_id": str(
                self.proposal_id
            ),
            "member_id": self.member_id,
            "choice": self.choice.value,
            "weight": self.weight,
            "rationale": self.rationale,
            "cast_at": self.cast_at.isoformat(),
        }


@dataclass(frozen=True, slots=True)
class CouncilProposal:
    """Immutable constitutional proposal."""

    proposal_id: UUID
    created_at: datetime
    title: str
    description: str
    kind: CouncilProposalKind
    strategy: CouncilVotingStrategy
    proposer: str
    state: CouncilProposalState
    payload: Mapping[str, Any]
    votes: tuple[CouncilVote, ...] = ()

    @classmethod
    def create(
        cls,
        *,
        title: str,
        description: str,
        kind: CouncilProposalKind,
        strategy: CouncilVotingStrategy,
        proposer: str,
        payload: Mapping[str, Any] | None = None,
    ) -> "CouncilProposal":
        resolved_title = title.strip()
        resolved_proposer = proposer.strip().lower()

        if not resolved_title:
            raise ValueError(
                "Proposal title cannot be empty."
            )

        if not resolved_proposer:
            raise ValueError(
                "Proposal proposer cannot be empty."
            )

        return cls(
            proposal_id=uuid4(),
            created_at=datetime.now(UTC),
            title=resolved_title,
            description=description.strip(),
            kind=kind,
            strategy=strategy,
            proposer=resolved_proposer,
            state=CouncilProposalState.OPEN,
            payload=MappingProxyType(
                dict(payload or {})
            ),
            votes=(),
        )

    def with_vote(
        self,
        vote: CouncilVote,
    ) -> "CouncilProposal":
        if self.state is not CouncilProposalState.OPEN:
            raise ValueError(
                "Votes may only be cast on open proposals."
            )

        retained = tuple(
            existing
            for existing in self.votes
            if existing.member_id != vote.member_id
        )

        return replace(
            self,
            votes=retained + (vote,),
        )

    def with_state(
        self,
        state: CouncilProposalState,
    ) -> "CouncilProposal":
        return replace(self, state=state)

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": str(
                self.proposal_id
            ),
            "created_at": (
                self.created_at.isoformat()
            ),
            "title": self.title,
            "description": self.description,
            "kind": self.kind.value,
            "strategy": self.strategy.value,
            "proposer": self.proposer,
            "state": self.state.value,
            "payload": dict(self.payload),
            "votes": [
                vote.to_dict()
                for vote in self.votes
            ],
        }


@dataclass(frozen=True, slots=True)
class CouncilDecision:
    """Immutable final council decision."""

    decision_id: UUID
    proposal_id: UUID
    decided_at: datetime
    outcome: CouncilDecisionOutcome
    approved: bool
    rationale: str
    approve_weight: int
    reject_weight: int
    abstain_weight: int
    eligible_weight: int
    participating_weight: int
    quorum_met: bool

    @classmethod
    def create(
        cls,
        *,
        proposal_id: UUID,
        outcome: CouncilDecisionOutcome,
        approved: bool,
        rationale: str,
        approve_weight: int,
        reject_weight: int,
        abstain_weight: int,
        eligible_weight: int,
        participating_weight: int,
        quorum_met: bool,
    ) -> "CouncilDecision":
        return cls(
            decision_id=uuid4(),
            proposal_id=proposal_id,
            decided_at=datetime.now(UTC),
            outcome=outcome,
            approved=approved,
            rationale=rationale,
            approve_weight=approve_weight,
            reject_weight=reject_weight,
            abstain_weight=abstain_weight,
            eligible_weight=eligible_weight,
            participating_weight=(
                participating_weight
            ),
            quorum_met=quorum_met,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": str(
                self.decision_id
            ),
            "proposal_id": str(
                self.proposal_id
            ),
            "decided_at": (
                self.decided_at.isoformat()
            ),
            "outcome": self.outcome.value,
            "approved": self.approved,
            "rationale": self.rationale,
            "approve_weight": self.approve_weight,
            "reject_weight": self.reject_weight,
            "abstain_weight": self.abstain_weight,
            "eligible_weight": self.eligible_weight,
            "participating_weight": (
                self.participating_weight
            ),
            "quorum_met": self.quorum_met,
        }


@dataclass(frozen=True, slots=True)
class CouncilStatistics:
    """Immutable council statistics."""

    members: int
    active_members: int
    proposals: int
    open_proposals: int
    approved_proposals: int
    rejected_proposals: int
    decisions: int
    votes: int

    def to_dict(self) -> dict[str, int]:
        return {
            "members": self.members,
            "active_members": (
                self.active_members
            ),
            "proposals": self.proposals,
            "open_proposals": (
                self.open_proposals
            ),
            "approved_proposals": (
                self.approved_proposals
            ),
            "rejected_proposals": (
                self.rejected_proposals
            ),
            "decisions": self.decisions,
            "votes": self.votes,
        }
