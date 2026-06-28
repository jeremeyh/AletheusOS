"""
Runtime Metrics
"""

from datetime import datetime

BOOT_TIME = datetime.utcnow()

def uptime():

    return datetime.utcnow()-BOOT_TIME
