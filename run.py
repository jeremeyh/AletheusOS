"""
CardHawk OS Launcher
"""

from core.application import app
from core.startup import startup

startup()

print(app.info())
