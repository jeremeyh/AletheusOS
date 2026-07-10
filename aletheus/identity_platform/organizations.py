"""
Organization Identity

Genesis 13.44
"""


class OrganizationRegistry:


    def __init__(self):

        self.organizations = {}



    def register(
        self,
        organization
    ):

        self.organizations[
            organization.identity_id
        ] = organization

