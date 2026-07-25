class AssetValidationError(ValueError):
    pass

class AssetValidator:
    """
    Asset Validator™

    Prevents incomplete or bad Asset DNA™ records from entering CardHawk OS™.
    """
    @staticmethod
    def validate(asset):
        errors = []

        if not getattr(asset, "player", ""):
            errors.append("Player/name is required.")

        if not getattr(asset, "category", ""):
            errors.append("Category is required.")

        if getattr(asset, "year", 0) and int(asset.year) < 1800:
            errors.append("Year appears invalid.")

        if float(getattr(asset, "purchase_price", 0) or 0) < 0:
            errors.append("Purchase price cannot be negative.")

        if float(getattr(asset, "current_value", 0) or 0) < 0:
            errors.append("Current value cannot be negative.")

        print_run = getattr(asset, "print_run", None)
        if print_run is not None and int(print_run) < 0:
            errors.append("Print run cannot be negative.")

        if errors:
            raise AssetValidationError(" | ".join(errors))

        return True
