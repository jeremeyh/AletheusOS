from pathlib import Path

from .models import ResponsibilityFinding


class ResponsibilityExtractor:
    """
    Classifies likely responsibility clusters inside runtime/core.py.
    """

    RESPONSIBILITIES = {
        "lifecycle": {
            "keywords": ["boot", "start", "stop", "shutdown", "initialize", "lifecycle"],
            "destination": "Executive Kernel",
        },
        "registration": {
            "keywords": ["register", "registry", "registrar"],
            "destination": "Runtime Registry",
        },
        "services": {
            "keywords": ["service", "services"],
            "destination": "Service Manager / Service Mesh",
        },
        "commands": {
            "keywords": ["command", "commands", "handler"],
            "destination": "Command Registry",
        },
        "events": {
            "keywords": ["event", "events", "publish", "subscribe"],
            "destination": "Relay Network / Event Fabric",
        },
        "governance": {
            "keywords": ["governance", "policy", "principle", "constitution"],
            "destination": "Governance Circuit",
        },
        "memory": {
            "keywords": ["memory", "remember", "recall"],
            "destination": "Memory Circuit",
        },
        "metrics": {
            "keywords": ["metric", "metrics", "telemetry", "health"],
            "destination": "Platform Intelligence",
        },
        "applications": {
            "keywords": ["application", "applications", "app"],
            "destination": "Application Registry / Application Circuit",
        },
        "routing": {
            "keywords": ["route", "router", "dispatch", "relay"],
            "destination": "Service Mesh / Relay Network",
        },
        "optimization": {
            "keywords": ["optimize", "optimization", "cache", "warm"],
            "destination": "Catalyst",
        },
        "workflow": {
            "keywords": ["workflow", "plan", "mission"],
            "destination": "Workflow Circuit / Mission Registry",
        },
    }

    def __init__(self, path: str = "aletheus/runtime/core.py"):
        self.path = Path(path)

    def extract(self):
        text = self.path.read_text(errors="ignore").lower()
        findings = []

        for responsibility, spec in self.RESPONSIBILITIES.items():
            matches = sum(text.count(keyword) for keyword in spec["keywords"])

            if matches:
                confidence = min(0.99, 0.55 + (matches / 100.0))

                findings.append(
                    ResponsibilityFinding(
                        responsibility=responsibility,
                        matches=matches,
                        suggested_destination=spec["destination"],
                        confidence=round(confidence, 2),
                        notes="Keyword-based responsibility signal.",
                    )
                )

        findings.sort(
            key=lambda item: item.matches,
            reverse=True,
        )

        return findings
