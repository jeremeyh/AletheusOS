"""Successor proof fixture — Release Assurance.

Proves that local RSF assurance passes while final release-certificate
authority remains outside RSF.
"""

from aletheus.rsf.genesis_112_20.assurance import run_package_assurance


def test_release_assurance_passes_without_self_certification_authority():
    result = run_package_assurance()

    assert result["status"] == "PASS"
    assert result["checks"]["contract_standard"] is True
    assert result["checks"]["healthy_continue"] is True
    assert result["checks"]["authority_boundary"] is True
    assert result["checks"]["adversarial"] is True
