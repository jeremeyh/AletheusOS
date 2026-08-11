"""
CardHawk OS™
Production Job Runner
"""

from datetime import datetime


class JobRunner:
    def run(self, name, payload):

        print()

        print("=" * 60)
        print("RUNNING JOB")
        print("=" * 60)
        print("Job:", name)
        print("Started:", datetime.utcnow().isoformat())
        print("Payload:", payload)
        print("=" * 60)

        return {
            "job": name,
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat(),
        }
