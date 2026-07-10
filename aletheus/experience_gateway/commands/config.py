from __future__ import annotations

import os
from pathlib import Path


def command_database_path() -> Path:
    configured = os.getenv(
        "ALETHEUS_COMMAND_DB",
        "",
    ).strip()

    if configured:
        return Path(
            configured
        ).expanduser().resolve()

    return (
        Path.cwd()
        / "var"
        / "experience_gateway"
        / "command_audit.sqlite3"
    ).resolve()
