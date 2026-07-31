from __future__ import annotations

from aletheus.platform_intelligence import (
    ConstitutionalCouncilMember,
    ConstitutionalRuntimeCouncil,
    ConstitutionalRuntimeGovernor,
    ConstitutionalRuntimeKernel,
    CouncilMemberKind,
    CouncilProposal,
    CouncilProposalKind,
    CouncilVoteChoice,
    CouncilVotingStrategy,
    ExecutiveDecision,
    ExecutiveRecoveryPlan,
    GovernorOutcome,
)


def test_governor_escalation_can_be_decided_by_council() -> None:
    kernel = ConstitutionalRuntimeKernel()

    governor = ConstitutionalRuntimeGovernor(kernel=kernel)

    plan = ExecutiveRecoveryPlan.create(
        decision=ExecutiveDecision.STOP_RUNTIME,
        target_services=(),
        ordered_services=(),
        requires_manual_approval=True,
        rationale="Critical runtime condition.",
    )

    governed = governor.evaluate(plan)

    assert governed.outcome is (GovernorOutcome.ESCALATED)

    council = ConstitutionalRuntimeCouncil()

    council.register_member(
        ConstitutionalCouncilMember(
            member_id="founder",
            display_name="Founder",
            kind=CouncilMemberKind.HUMAN,
            authority="Constitutional authority",
            voting_weight=2,
        )
    )
    council.register_member(
        ConstitutionalCouncilMember(
            member_id="architect",
            display_name="Chief Architect",
            kind=CouncilMemberKind.ADVISORY,
            authority="Architecture authority",
        )
    )

    proposal = council.submit(
        CouncilProposal.create(
            title="Authorize runtime stop",
            description=governed.reason,
            kind=(CouncilProposalKind.EMERGENCY_OVERRIDE),
            strategy=(CouncilVotingStrategy.MAJORITY),
            proposer="runtime-governor",
            payload=governed.to_dict(),
        )
    )

    council.cast_vote(
        proposal_id=proposal.proposal_id,
        member_id="founder",
        choice=CouncilVoteChoice.APPROVE,
    )

    decision = council.decide(proposal.proposal_id)

    assert decision.approved is True
