from aletheus.strategic.runtime import (
    RuntimeCapabilityStatus,
    SPANRuntimeService,
)


class Recorder:
    def __init__(self):
        self.items = []

    def publish(self, event_type, payload):
        self.items.append((event_type, payload))

    def append(self, record):
        self.items.append(record)

    def submit(self, proposal):
        self.items.append(proposal)

    def increment(self, metric, value=1):
        self.items.append((metric, value))

    def observe(self, metric, value):
        self.items.append((metric, value))


def test_lifecycle():
    events = Recorder()
    service = SPANRuntimeService(events=events)

    assert service.status is RuntimeCapabilityStatus.CREATED
    service.initialize()
    assert service.status is RuntimeCapabilityStatus.INITIALIZED
    service.start()
    assert service.status is RuntimeCapabilityStatus.RUNNING
    service.stop()
    assert service.status is RuntimeCapabilityStatus.STOPPED


def test_health_reports_initialized_components():
    service = SPANRuntimeService().initialize()
    health = service.health()

    assert health["name"] == "span"
    assert health["span_ready"] is True
    assert health["spartan_ready"] is True


def test_proposal_flows_to_existing_authorities():
    ledger = Recorder()
    council = Recorder()
    telemetry = Recorder()
    events = Recorder()

    service = SPANRuntimeService(
        ledger=ledger,
        council=council,
        telemetry=telemetry,
        events=events,
    ).start()

    proposal = service.submit_proposal(
        title="Consolidate registration",
        summary="Use the authoritative runtime registry.",
        evidence=({"module": "aletheus.runtime"},),
        confidence=0.94,
    )

    assert proposal.title == "Consolidate registration"
    assert ledger.items
    assert council.items
    assert telemetry.items
    assert any(name == "StrategicRecommendationCreated" for name, _ in events.items)


def test_proposal_requires_running_service():
    service = SPANRuntimeService()

    try:
        service.submit_proposal(title="x", summary="y")
    except RuntimeError as exc:
        assert "must be running" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError")
