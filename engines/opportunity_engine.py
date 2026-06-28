class OpportunityEngine:
    """
    Ranks assets by opportunity.
    """

    @staticmethod
    def rank(assets):

        ranked=sorted(

            assets,

            key=lambda x:(

                x.thorx_score,

                x.ni_score,

                x.current_value

            ),

            reverse=True

        )

        return ranked