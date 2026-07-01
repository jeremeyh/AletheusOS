"""
Runtime Health Module
Version 4.5.0
"""

from __future__ import annotations


def runtime_health(runtime):
    return {
        "version": runtime.version,
        "status": runtime.status,
        "services": runtime.services.statistics(),
    }
