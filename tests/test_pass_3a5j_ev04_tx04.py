from aletheus.mammoth.lifecycle.evidence import characterize_evidence_quality
from aletheus.mammoth.lifecycle.authority import contradiction_guard

def test_ev04_quality_is_bounded():
    q = characterize_evidence_quality(0.75, method='test', rationale='bounded')
    assert q.confidence == 0.75
    try:
        characterize_evidence_quality(1.1)
    except ValueError:
        pass
    else:
        raise AssertionError('confidence > 1.0 must fail')

def test_tx04_contradiction_denies_authorization():
    assert contradiction_guard(contradictory_evidence=True, otherwise_authorized=True) is False
    assert contradiction_guard(contradictory_evidence=False, otherwise_authorized=True) is True
    assert contradiction_guard(contradictory_evidence=False, otherwise_authorized=False) is False
