"""Constitutional Runtime Council."""

from __future__ import annotations

from datetime import UTC, datetime
from threading import RLock
from typing import Any
from uuid import UUID

from .exceptions import (
    CouncilDecisionError,
    CouncilMemberAlreadyExistsError,
    CouncilMemberNotFoundError,
    CouncilProposalAlreadyExistsError,
    CouncilProposalNotFoundError,
    CouncilVotingError,
)
from .models import (
    ConstitutionalCouncilMember,
    CouncilDecision,
    CouncilDecisionOutcome,
    CouncilProposal,
    CouncilProposalState,
    CouncilStatistics,
    CouncilVote,
    CouncilVoteChoice,
    CouncilVotingStrategy,
)


class ConstitutionalRuntimeCouncil:
    """
    Highest constitutional governance authority for runtime proposals.

    CRC owns membership, proposals, weighted voting, decisions, and immutable
    governance history. It never executes runtime actions or mutates policy.
    """

    VERSION = "9.18.0"

    def __init__(
        self,
        *,
        quorum_ratio: float = 0.5,
    ) -> None:
        if not 0.0 < quorum_ratio <= 1.0:
            raise ValueError(
                "quorum_ratio must be between 0 and 1."
            )

        self._quorum_ratio = quorum_ratio
        self._members: dict[
            str,
            ConstitutionalCouncilMember,
        ] = {}
        self._proposals: dict[
            UUID,
            CouncilProposal,
        ] = {}
        self._decisions: dict[
            UUID,
            CouncilDecision,
        ] = {}
        self._history: list[
            dict[str, Any]
        ] = []
        self._lock = RLock()

    @property
    def quorum_ratio(self) -> float:
        return self._quorum_ratio

    def register_member(
        self,
        member: ConstitutionalCouncilMember,
    ) -> ConstitutionalCouncilMember:
        with self._lock:
            if member.member_id in self._members:
                raise CouncilMemberAlreadyExistsError(
                    "Council member already exists: "
                    f"{member.member_id}"
                )

            self._members[
                member.member_id
            ] = member

            self._append_history(
                "member_registered",
                member.to_dict(),
            )

        return member

    def get_member(
        self,
        member_id: str,
    ) -> ConstitutionalCouncilMember:
        resolved = member_id.strip().lower()

        with self._lock:
            member = self._members.get(
                resolved
            )

        if member is None:
            raise CouncilMemberNotFoundError(
                "Council member not found: "
                f"{resolved}"
            )

        return member

    def members(
        self,
    ) -> tuple[
        ConstitutionalCouncilMember,
        ...,
    ]:
        with self._lock:
            return tuple(
                self._members[member_id]
                for member_id
                in sorted(self._members)
            )

    def submit(
        self,
        proposal: CouncilProposal,
    ) -> CouncilProposal:
        with self._lock:
            if proposal.proposal_id in self._proposals:
                raise CouncilProposalAlreadyExistsError(
                    "Council proposal already exists: "
                    f"{proposal.proposal_id}"
                )

            self._proposals[
                proposal.proposal_id
            ] = proposal

            self._append_history(
                "proposal_submitted",
                proposal.to_dict(),
            )

        return proposal

    def get_proposal(
        self,
        proposal_id: UUID,
    ) -> CouncilProposal:
        with self._lock:
            proposal = self._proposals.get(
                proposal_id
            )

        if proposal is None:
            raise CouncilProposalNotFoundError(
                "Council proposal not found: "
                f"{proposal_id}"
            )

        return proposal

    def proposals(
        self,
    ) -> tuple[CouncilProposal, ...]:
        with self._lock:
            return tuple(
                sorted(
                    self._proposals.values(),
                    key=lambda item: (
                        item.created_at,
                        str(item.proposal_id),
                    ),
                )
            )

    def cast_vote(
        self,
        *,
        proposal_id: UUID,
        member_id: str,
        choice: CouncilVoteChoice,
        rationale: str = "",
    ) -> CouncilVote:
        member = self.get_member(member_id)

        if not member.active:
            raise CouncilVotingError(
                "Inactive council members cannot vote."
            )

        with self._lock:
            proposal = self.get_proposal(
                proposal_id
            )

            if proposal.state is not CouncilProposalState.OPEN:
                raise CouncilVotingError(
                    "Votes may only be cast on open proposals."
                )

            vote = CouncilVote.create(
                proposal_id=proposal_id,
                member=member,
                choice=choice,
                rationale=rationale,
            )

            self._proposals[
                proposal_id
            ] = proposal.with_vote(vote)

            self._append_history(
                "vote_cast",
                vote.to_dict(),
            )

        return vote

    def decide(
        self,
        proposal_id: UUID,
    ) -> CouncilDecision:
        with self._lock:
            proposal = self.get_proposal(
                proposal_id
            )

            if proposal.state is not CouncilProposalState.OPEN:
                raise CouncilDecisionError(
                    "Only open proposals may be decided."
                )

            active_members = tuple(
                member
                for member in self._members.values()
                if member.active
            )

            eligible_weight = sum(
                member.voting_weight
                for member in active_members
            )

            if eligible_weight == 0:
                raise CouncilDecisionError(
                    "No active council voting weight is available."
                )

            approve_weight = sum(
                vote.weight
                for vote in proposal.votes
                if vote.choice is CouncilVoteChoice.APPROVE
            )
            reject_weight = sum(
                vote.weight
                for vote in proposal.votes
                if vote.choice is CouncilVoteChoice.REJECT
            )
            abstain_weight = sum(
                vote.weight
                for vote in proposal.votes
                if vote.choice is CouncilVoteChoice.ABSTAIN
            )
            participating_weight = (
                approve_weight
                + reject_weight
                + abstain_weight
            )

            quorum_met = (
                participating_weight
                / eligible_weight
                >= self._quorum_ratio
            )

            if not quorum_met:
                outcome = (
                    CouncilDecisionOutcome
                    .INSUFFICIENT_QUORUM
                )
                approved = False
                rationale = (
                    "Council quorum was not met."
                )
                next_state = (
                    CouncilProposalState.REJECTED
                )
            else:
                approved = self._is_approved(
                    proposal.strategy,
                    approve_weight=approve_weight,
                    reject_weight=reject_weight,
                    participating_weight=(
                        participating_weight
                    ),
                    eligible_weight=eligible_weight,
                )

                if approved:
                    outcome = (
                        CouncilDecisionOutcome.APPROVED
                    )
                    rationale = (
                        "Proposal satisfied its "
                        "voting strategy."
                    )
                    next_state = (
                        CouncilProposalState.APPROVED
                    )
                else:
                    outcome = (
                        CouncilDecisionOutcome.REJECTED
                    )
                    rationale = (
                        "Proposal did not satisfy its "
                        "voting strategy."
                    )
                    next_state = (
                        CouncilProposalState.REJECTED
                    )

            decision = CouncilDecision.create(
                proposal_id=proposal_id,
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

            self._proposals[
                proposal_id
            ] = proposal.with_state(
                next_state
            )
            self._decisions[
                proposal_id
            ] = decision

            self._append_history(
                "proposal_decided",
                decision.to_dict(),
            )

        return decision

    def decision_for(
        self,
        proposal_id: UUID,
    ) -> CouncilDecision:
        with self._lock:
            decision = self._decisions.get(
                proposal_id
            )

        if decision is None:
            raise CouncilDecisionError(
                "No decision exists for proposal: "
                f"{proposal_id}"
            )

        return decision

    def statistics(self) -> CouncilStatistics:
        proposals = self.proposals()

        return CouncilStatistics(
            members=len(self._members),
            active_members=sum(
                member.active
                for member in self._members.values()
            ),
            proposals=len(proposals),
            open_proposals=sum(
                proposal.state
                is CouncilProposalState.OPEN
                for proposal in proposals
            ),
            approved_proposals=sum(
                proposal.state
                is CouncilProposalState.APPROVED
                for proposal in proposals
            ),
            rejected_proposals=sum(
                proposal.state
                is CouncilProposalState.REJECTED
                for proposal in proposals
            ),
            decisions=len(self._decisions),
            votes=sum(
                len(proposal.votes)
                for proposal in proposals
            ),
        )

    def history(
        self,
    ) -> tuple[dict[str, Any], ...]:
        with self._lock:
            return tuple(
                {
                    "sequence": record["sequence"],
                    "recorded_at": record["recorded_at"],
                    "event_type": record["event_type"],
                    "payload": dict(record["payload"]),
                }
                for record in self._history
            )

    def snapshot(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "quorum_ratio": self._quorum_ratio,
            "members": [
                member.to_dict()
                for member in self.members()
            ],
            "proposals": [
                proposal.to_dict()
                for proposal in self.proposals()
            ],
            "decisions": [
                decision.to_dict()
                for _, decision in sorted(
                    self._decisions.items(),
                    key=lambda item: str(
                        item[0]
                    ),
                )
            ],
            "statistics": (
                self.statistics().to_dict()
            ),
            "history": list(self.history()),
        }

    def export(self) -> dict[str, Any]:
        return self.snapshot()

    @staticmethod
    def _is_approved(
        strategy: CouncilVotingStrategy,
        *,
        approve_weight: int,
        reject_weight: int,
        participating_weight: int,
        eligible_weight: int,
    ) -> bool:
        decisive_weight = (
            approve_weight + reject_weight
        )

        if decisive_weight == 0:
            return False

        if strategy is CouncilVotingStrategy.MAJORITY:
            return approve_weight > reject_weight

        if strategy is CouncilVotingStrategy.SUPERMAJORITY:
            return (
                approve_weight / decisive_weight
                >= (2 / 3)
            )

        if strategy is CouncilVotingStrategy.UNANIMOUS:
            return (
                approve_weight == eligible_weight
                and participating_weight
                == eligible_weight
            )

        return False

    def _append_history(
        self,
        event_type: str,
        payload: dict[str, Any],
    ) -> None:
        self._history.append(
            {
                "sequence": len(self._history),
                "recorded_at": (
                    datetime.now(UTC).isoformat()
                ),
                "event_type": event_type,
                "payload": dict(payload),
            }
        )
