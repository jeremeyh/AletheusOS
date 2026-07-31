"""
User Identity Registry

Genesis 13.44
"""


class UserRegistry:
    def __init__(self):

        self.users = {}

    def register(self, user):

        self.users[user.identity_id] = user
