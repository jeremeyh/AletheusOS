"""
Card Hawk Social Engine

Genesis 14.25
"""

from .communities import CommunityEngine
from .profiles import ProfileManager
from .reputation import ReputationEngine


class SocialEngine:
    def __init__(self):

        self.profiles = ProfileManager()

        self.communities = CommunityEngine()

        self.reputation = ReputationEngine()

    def initialize(self):

        return {"status": "ready"}
