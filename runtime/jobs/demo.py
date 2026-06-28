from runtime.jobs.job_runner import JobRunner

runner = JobRunner()

runner.run(
    "asset.process",
    {
        "player":"Caleb Williams",
        "set":"Prizm",
        "parallel":"Gold",
        "serial":"10"
    }
)
