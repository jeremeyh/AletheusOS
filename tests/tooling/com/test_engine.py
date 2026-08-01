import json

from aletheus.tooling.com.engine import CognitiveMeshEngine


def test_consensus_preserves_dissent(tmp_path) -> None:
    source = tmp_path / "input.json"
    source.write_text(
        json.dumps(
            {
                "contributions": [
                    {
                        "authority": "Kinekt",
                        "claim": "refactor-a",
                        "confidence": 0.9,
                        "disposition": "support",
                        "source": "kinekt",
                    },
                    {
                        "authority": "Sentinel",
                        "claim": "refactor-a",
                        "confidence": 0.4,
                        "disposition": "oppose",
                        "source": "sentinel",
                    },
                ]
            }
        )
    )
    report = CognitiveMeshEngine(source, tmp_path / "out").analyze()
    assert report.consensus[0].status == "supported"
    assert report.consensus[0].dissenters == ("Sentinel",)
