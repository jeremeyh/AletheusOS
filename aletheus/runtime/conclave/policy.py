from dataclasses import dataclass, field


@dataclass
class ConclavePolicy:
    protected_paths: list[str] = field(default_factory=lambda: [
        "aletheus",
        "cardhawk",
        "watch_tower",
        "runtime_state",
        "vault",
        "backups",
        "config",
        "manifests",
        "VERSION",
        "README.md",
        "CHANGELOG.md",
    ])

    destructive_keywords: list[str] = field(default_factory=lambda: [
        "rm -rf",
        "delete",
        "wipe",
        "destroy",
        "exfiltrate",
        "leak",
        "dump secrets",
        "steal",
        "token",
        "private key",
        "credential",
        "password",
        "secret",
    ])

    decoy_response: dict = field(default_factory=lambda: {
        "status": "shielded",
        "data": {},
        "message": "Conclave shield active. Sensitive payload unavailable.",
    })
