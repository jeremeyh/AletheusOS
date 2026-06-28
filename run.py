"""
CardHawk OS Launcher
"""

from core.startup import startup
from core.application import app

startup()

print(app.info())
