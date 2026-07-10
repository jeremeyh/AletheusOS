"""
Card Hawk Asset Validator

Genesis 13.20
"""


class AssetValidator:


    def validate(
        self,
        asset
    ):


        errors = []


        if not asset.title:

            errors.append(
                "missing_title"
            )


        if not asset.source_id:

            errors.append(
                "missing_source_id"
            )


        return {

            "valid":
                len(errors) == 0,

            "errors":
                errors

        }

