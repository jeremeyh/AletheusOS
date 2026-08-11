class GradingWorkflow:
    """Tracks grading lifecycle."""

    def submit(self, asset, company):
        asset.status = "Grading"
        asset.grade_company = company
        return asset

    def receive_grade(self, asset, grade):
        asset.grade = grade
        asset.status = "Portfolio"
        return asset
