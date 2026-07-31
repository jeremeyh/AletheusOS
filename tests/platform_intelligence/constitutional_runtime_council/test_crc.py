from __future__ import annotations

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalCouncilMember,
    ConstitutionalRuntimeCouncil,
    CouncilDecisionError,
    CouncilDecisionOutcome,
    CouncilMemberAlreadyExistsError,
    CouncilMemberKind,
    CouncilProposal,
    CouncilProposalKind,
    CouncilProposalState,
    CouncilVoteChoice,
    CouncilVotingStrategy,
)


def member(
    member_id: str,
    *,
    weight: int = 1,
) -> ConstitutionalCouncilMember:
    return ConstitutionalCouncilMember(
        member_id=member_id,
        display_name=member_id,
        kind=CouncilMemberKind.HUMAN,
        authority="AletheusOS Constitution",
        voting_weight=weight,
    )


def proposal(
    strategy: CouncilVotingStrategy = (CouncilVotingStrategy.MAJORITY),
) -> CouncilProposal:
    return CouncilProposal.create(
        title="Approve runtime policy",
        description=("Approve a constitutional policy change."),
        kind=CouncilProposalKind.POLICY_CHANGE,
        strategy=strategy,
        proposer="founder",
        payload={"policy_id": "runtime.health"},
    )


def build_council() -> ConstitutionalRuntimeCouncil:
    council = ConstitutionalRuntimeCouncil()

    council.register_member(member("founder", weight=2))
    council.register_member(member("architect"))
    council.register_member(member("security"))

    return council


def test_members_are_registered() -> None:
    council = build_council()

    assert len(council.members()) == 3
    assert council.get_member("founder").voting_weight == 2


def test_duplicate_member_is_rejected() -> None:
    council = ConstitutionalRuntimeCouncil()
    value = member("founder")

    council.register_member(value)

    with pytest.raises(CouncilMemberAlreadyExistsError):
        council.register_member(value)


def test_proposal_is_submitted_open() -> None:
    council = build_council()
    value = council.submit(proposal())

    assert value.state is (CouncilProposalState.OPEN)
    assert council.get_proposal(value.proposal_id) == value


def test_vote_is_recorded() -> None:
    council = build_council()
    value = council.submit(proposal())

    vote = council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="founder",
        choice=CouncilVoteChoice.APPROVE,
    )

    stored = council.get_proposal(value.proposal_id)

    assert vote.member_id == "founder"
    assert len(stored.votes) == 1


def test_member_can_replace_vote() -> None:
    council = build_council()
    value = council.submit(proposal())

    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="architect",
        choice=CouncilVoteChoice.REJECT,
    )
    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="architect",
        choice=CouncilVoteChoice.APPROVE,
    )

    stored = council.get_proposal(value.proposal_id)

    assert len(stored.votes) == 1
    assert stored.votes[0].choice is CouncilVoteChoice.APPROVE


def test_majority_approval() -> None:
    council = build_council()
    value = council.submit(proposal())

    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="founder",
        choice=CouncilVoteChoice.APPROVE,
    )
    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="architect",
        choice=CouncilVoteChoice.REJECT,
    )

    decision = council.decide(value.proposal_id)

    assert decision.outcome is (CouncilDecisionOutcome.APPROVED)
    assert decision.approved is True


def test_majority_rejection() -> None:
    council = build_council()
    value = council.submit(proposal())

    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="architect",
        choice=CouncilVoteChoice.REJECT,
    )
    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="security",
        choice=CouncilVoteChoice.REJECT,
    )

    decision = council.decide(value.proposal_id)

    assert decision.outcome is (CouncilDecisionOutcome.REJECTED)


def test_supermajority_requires_two_thirds() -> None:
    council = build_council()
    value = council.submit(proposal(CouncilVotingStrategy.SUPERMAJORITY))

    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="founder",
        choice=CouncilVoteChoice.APPROVE,
    )
    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="architect",
        choice=CouncilVoteChoice.REJECT,
    )

    decision = council.decide(value.proposal_id)

    assert decision.approved is True


def test_unanimous_requires_all_weight() -> None:
    council = build_council()
    value = council.submit(proposal(CouncilVotingStrategy.UNANIMOUS))

    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="founder",
        choice=CouncilVoteChoice.APPROVE,
    )
    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="architect",
        choice=CouncilVoteChoice.APPROVE,
    )

    decision = council.decide(value.proposal_id)

    assert decision.approved is False


def test_insufficient_quorum() -> None:
    council = ConstitutionalRuntimeCouncil(quorum_ratio=0.75)

    council.register_member(member("founder"))
    council.register_member(member("architect"))
    council.register_member(member("security"))

    value = council.submit(proposal())

    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="founder",
        choice=CouncilVoteChoice.APPROVE,
    )

    decision = council.decide(value.proposal_id)

    assert decision.outcome is (CouncilDecisionOutcome.INSUFFICIENT_QUORUM)
    assert decision.quorum_met is False


def test_decided_proposal_cannot_be_decided_twice() -> None:
    council = build_council()
    value = council.submit(proposal())

    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="founder",
        choice=CouncilVoteChoice.APPROVE,
    )
    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="architect",
        choice=CouncilVoteChoice.APPROVE,
    )

    council.decide(value.proposal_id)

    with pytest.raises(CouncilDecisionError):
        council.decide(value.proposal_id)


def test_history_is_append_only() -> None:
    council = build_council()
    value = council.submit(proposal())

    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="founder",
        choice=CouncilVoteChoice.APPROVE,
    )

    history = council.history()

    assert len(history) == 5
    assert [item["sequence"] for item in history] == list(range(5))


def test_snapshot_is_complete() -> None:
    council = build_council()
    value = council.submit(proposal())

    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="founder",
        choice=CouncilVoteChoice.APPROVE,
    )
    council.cast_vote(
        proposal_id=value.proposal_id,
        member_id="architect",
        choice=CouncilVoteChoice.APPROVE,
    )
    council.decide(value.proposal_id)

    snapshot = council.snapshot()

    assert snapshot["version"] == "9.18.0"
    assert len(snapshot["members"]) == 3
    assert len(snapshot["proposals"]) == 1
    assert len(snapshot["decisions"]) == 1
    assert snapshot["statistics"]["approved_proposals"] == 1


def test_council_never_executes_runtime_actions() -> None:
    council = build_council()

    forbidden = {
        "restart_service",
        "start_platform",
        "stop_platform",
        "transition",
        "report_health",
        "execute",
        "publish",
        "apply_policy",
    }

    assert forbidden.isdisjoint(set(dir(council)))
