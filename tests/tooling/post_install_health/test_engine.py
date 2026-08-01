from pathlib import Path

from aletheus.tooling.post_install_health.engine import Engine


class FakeMission:
    def __init__(self, *_args: object) -> None:
        pass

    async def execute(
        self,
        *_args: object,
        **_kwargs: object,
    ) -> dict[str, str]:
        return {
            "status": "completed",
            "platform_certification": "READY",
        }


def test_health_report(tmp_path: Path) -> None:
    report = Engine(
        Path("p"),
        Path("b"),
        tmp_path,
        mission_factory=FakeMission,
    ).verify()
    assert report["healthy"] is True
