import pandas as pd
import streamlit as st
from services.runtime_v2 import runtime_v2

st.set_page_config(
    page_title="Founder Console | CardHawkOS",
    page_icon="🦅",
    layout="wide",
)

st.title("🦅 Founder Console")
st.caption("CardHawkOS Runtime v2 command center")

health_context = runtime_v2.command_bus.dispatch("runtime.health")
health = health_context.results.get("health", {})

col1, col2, col3, col4 = st.columns(4)

col1.metric("Runtime", health.get("status", "unknown"))
col2.metric("Engines", health.get("engines", 0))
col3.metric("Services", health.get("services", 0))
col4.metric("Plugins", health.get("plugins", 0))

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Runtime Health",
        "Registry",
        "Pipeline",
        "Scheduler",
        "Metrics",
    ]
)

with tab1:
    st.subheader("Runtime Health")

    st.json(health)

    if health_context.errors:
        st.error("Runtime health returned errors.")
        st.json(health_context.errors)

with tab2:
    st.subheader("Engine / Service / Plugin Registry")

    registry_context = runtime_v2.command_bus.dispatch("runtime.registry")
    registry = registry_context.results.get("registry", {})

    st.markdown("### Engines")
    engines = registry.get("engines", [])
    st.dataframe(pd.DataFrame({"Engine": engines}), use_container_width=True)

    st.markdown("### Services")
    services = registry.get("services", [])
    st.dataframe(pd.DataFrame({"Service": services}), use_container_width=True)

    st.markdown("### Plugins")
    plugins = registry.get("plugins", {})
    if plugins:
        plugin_rows = []
        for name, data in plugins.items():
            plugin_rows.append(
                {
                    "Plugin": name,
                    "Version": data.get("version"),
                    "Enabled": data.get("enabled"),
                    "Description": data.get("description"),
                    "Registered At": data.get("registered_at"),
                }
            )
        st.dataframe(pd.DataFrame(plugin_rows), use_container_width=True)
    else:
        st.info("No plugins registered.")

with tab3:
    st.subheader("Runtime Pipeline")

    st.write(
        "Run the integrated CardHawkOS Runtime v2 pipeline across Hawk A•Eye™, THORᵡ, DEF, NEST™, and FALCON™."
    )

    asset_name = st.text_input(
        "Asset / Opportunity Name", value="Sample CardHawk Opportunity"
    )
    player = st.text_input("Player", value="Caleb Williams")
    price = st.number_input("Price", min_value=0.0, value=150.0, step=5.0)

    if st.button("Run Runtime Pipeline", type="primary"):
        pipeline_context = runtime_v2.command_bus.dispatch(
            "runtime.pipeline",
            {
                "asset_name": asset_name,
                "player": player,
                "price": price,
            },
        )

        if pipeline_context.errors:
            st.error("Pipeline completed with errors.")
            st.json(pipeline_context.errors)
        else:
            st.success("Pipeline completed successfully.")

        st.json(pipeline_context.results)

with tab4:
    st.subheader("Scheduler")

    jobs = runtime_v2.scheduler.list_jobs()

    if jobs:
        job_rows = []
        for name, data in jobs.items():
            job_rows.append(
                {
                    "Job": name,
                    "Description": data.get("description"),
                    "Last Run": data.get("last_run"),
                    "Last Result": data.get("last_result"),
                }
            )

        st.dataframe(pd.DataFrame(job_rows), use_container_width=True)

        selected_job = st.selectbox("Select Job", list(jobs.keys()))

        if st.button("Run Selected Job"):
            result = runtime_v2.scheduler.run_job(selected_job)
            st.success(f"Job completed: {selected_job}")
            st.json(result)
    else:
        st.info("No scheduled jobs registered.")

with tab5:
    st.subheader("Runtime Metrics")

    metrics_context = runtime_v2.command_bus.dispatch("runtime.metrics")
    metrics = metrics_context.results.get("metrics", [])

    if metrics:
        st.dataframe(pd.DataFrame(metrics), use_container_width=True)
    else:
        st.info("No runtime metrics recorded yet.")

    st.markdown("### Event Log")
    if runtime_v2.event_log:
        st.dataframe(pd.DataFrame(runtime_v2.event_log), use_container_width=True)
    else:
        st.info("No runtime events recorded yet.")
