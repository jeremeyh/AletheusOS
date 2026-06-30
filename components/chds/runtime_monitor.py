import streamlit as st

from cardhawkos.boot.boot_manager import BootManager
from cardhawkos.runtime.registry import EngineRegistry
from cardhawkos.runtime.service_registry import ServiceRegistry
from jobs.runtime.scheduler import JobScheduler
from jobs.runtime.manager import JobManager


def render_runtime_monitor():
    """
    CardHawkOS Runtime Monitor™

    Displays live runtime information for the
    CardHawkOS operating system.
    """

    boot = BootManager.boot()

    engine_count = EngineRegistry.count()
    service_count = ServiceRegistry.count()
    job_count = JobScheduler.count()
    completed_jobs = JobManager.count()

    history = JobManager.history()

    success_count = sum(
        1
        for job in history
        if job.get("status") == "SUCCESS"
    )

    success_rate = 100.0

    if completed_jobs > 0:
        success_rate = (
            success_count / completed_jobs
        ) * 100

    last_runtime = "-"

    if history:
        last_runtime = history[0].get(
            "completed",
            "-"
        )

    st.subheader("🖥 CardHawkOS Runtime™")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Status",
            boot["status"],
        )

        st.metric(
            "Version",
            boot["version"],
        )

    with c2:
        st.metric(
            "Engines",
            engine_count,
        )

        st.metric(
            "Services",
            service_count,
        )

    with c3:
        st.metric(
            "Registered Jobs",
            job_count,
        )

        st.metric(
            "Completed Jobs",
            completed_jobs,
        )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Success Rate",
            f"{success_rate:.0f}%",
        )

    with c2:
        st.metric(
            "Last Runtime",
            last_runtime,
        )

    st.divider()

    st.markdown("### Recent Jobs")

    if not history:

        st.info("No jobs have been executed.")

    else:

        for job in history[:10]:

            icon = "🟢"

            if job["status"] != "SUCCESS":
                icon = "🔴"

            st.markdown(
                f"""
**{icon} {job['job']}**

Status: `{job['status']}`

Completed: `{job['completed']}`
"""
            )

            st.divider()

    st.markdown("### Engine Health")

    for engine in EngineRegistry.status():

        left, right = st.columns([5, 1])

        with left:
            st.write(engine["engine"])

        with right:
            st.success("ONLINE")
