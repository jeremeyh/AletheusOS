from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path


class ReleaseManifest:

    def __init__(self, runtime):
        self.runtime = runtime


    def generate(self):

        certification = (
            self.runtime.certify_runtime()
            if hasattr(
                self.runtime,
                "certify_runtime"
            )
            else {
                "status": "UNKNOWN"
            }
        )


        commands = (
            self.runtime.command_surface_audit()
            if hasattr(
                self.runtime,
                "command_surface_audit"
            )
            else {}
        )


        registry = (
            self.runtime.registry_snapshot()
            if hasattr(
                self.runtime,
                "registry_snapshot"
            )
            else {}
        )


        spa = (
            self.runtime.spa.assess()
            if hasattr(
                self.runtime,
                "spa"
            )
            else {}
        )


        return {
            "platform": "AletheusOS",
            "genesis": "Genesis 6",
            "generated": datetime.now(
                timezone.utc
            ).isoformat(),

            "runtime": {
                "version": getattr(
                    self.runtime,
                    "version",
                    "unknown",
                ),
            },

            "certification": certification,

            "command_surface": {
                "total":
                    commands.get(
                        "total_commands",
                        0
                    ),
                "healthy":
                    commands.get(
                        "healthy",
                        False
                    ),
            },

            "registry": registry,

            "spa": spa,

            "release_ready":
                certification.get(
                    "certified",
                    False
                ),
        }


    def write(self, path="release_manifest.json"):

        manifest = self.generate()

        Path(path).write_text(
            json.dumps(
                manifest,
                indent=2,
                default=str,
            )
        )

        return manifest
