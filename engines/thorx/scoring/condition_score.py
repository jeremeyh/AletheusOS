class ConditionScore:

    @staticmethod
    def calculate(card):

        grade = str(card.get("grade", "")).lower()

        if "gem" in grade:
            return 100

        if "mint" in grade:
            return 95

        if "9" in grade:
            return 90

        return 75
