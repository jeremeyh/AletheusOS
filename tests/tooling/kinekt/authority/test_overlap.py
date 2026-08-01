from aletheus.tooling.kinekt.authority.analysis import (
    detect_claim_overlaps,
    parse_authorities,
)


def test_overlap():
    a = parse_authorities(
        {
            "capabilities": [
                {
                    "name": "One",
                    "runtime_role": "one",
                    "owns": ["repository intelligence"],
                },
                {
                    "name": "Two",
                    "runtime_role": "two",
                    "owns": ["repository intelligence"],
                },
            ]
        }
    )
    f = detect_claim_overlaps(a)
    assert len(f) == 1
    assert f[0].code == "SOVEREIGN_AUTHORITY_OVERLAP"
