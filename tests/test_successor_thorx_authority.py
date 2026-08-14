"""Successor proof fixture — THORX authority.

Bounded proof of the fail-closed contradiction gate admitted by Pass 3A-5J.
This test does not alter THORX implementation.
"""

from aletheus.mammoth.lifecycle.authority import contradiction_guard


def test_thorx_contradiction_guard_refuses_contradictory_evidence():
    assert contradiction_guard(
        contradictory_evidence=True,
        otherwise_authorized=True,
    ) is False


def test_thorx_contradiction_guard_preserves_noncontradictory_authority():
    assert contradiction_guard(
        contradictory_evidence=False,
        otherwise_authorized=True,
    ) is True


def test_thorx_contradiction_guard_does_not_invent_authority():
    assert contradiction_guard(
        contradictory_evidence=False,
        otherwise_authorized=False,
    ) is False
