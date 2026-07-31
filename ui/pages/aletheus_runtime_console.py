import json

import pandas as pd
import streamlit as st

from aletheus.runtime import runtime_core


def safe_dataframe(rows):
    if not rows:
        return pd.DataFrame()

    normalized = []

    for row in rows:
        clean = {}
        for key, value in row.items():
            if isinstance(value, (dict, list)):
                clean[key] = json.dumps(value, ensure_ascii=False)
            elif value is None:
                clean[key] = ""
            else:
                clean[key] = str(value)
        normalized.append(clean)

    return pd.DataFrame(normalized)


st.set_page_config(
    page_title="Aletheus Runtime Console",
    page_icon="🧠",
    layout="wide",
)

health_context = runtime_core.commands.dispatch("runtime.health")
health = health_context.results.get("health", {})

diagnostics_context = runtime_core.commands.dispatch("runtime.diagnostics")
diagnostics = diagnostics_context.results.get("diagnostics", {})
memory_diagnostics = diagnostics_context.results.get("memory", {})

st.title("Aletheus™ Runtime Console")
st.caption("Genesis 0.7 | Autonomous Mission Engine | 6th Dimension Multimedia")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Runtime", health.get("status", "unknown"))
col2.metric("Version", health.get("version", "unknown"))
col3.metric("Services", health.get("services", 0))
col4.metric("Active Missions", health.get("active_missions", 0))

st.divider()

tabs = st.tabs(
    [
        "Health",
        "Memory",
        "Cognition",
        "Knowledge Graph",
        "Missions",
        "Diagnostics",
        "Commands",
        "Events",
        "Metrics",
        "Queue",
        "Scheduler",
        "Pipelines",
        "Workflows",
        "Plugins",
    ]
)

with tabs[0]:
    st.subheader("Runtime Health")
    st.json(health)

with tabs[1]:
    st.subheader("Aletheus Memory Core")

    st.markdown("### Memory Stats")
    st.json(memory_diagnostics)

    st.markdown("### Add Memory Record")

    key = st.text_input("Key", value="founder_note")
    namespace = st.text_input("Namespace", value="founder_workspace")
    memory_type = st.selectbox(
        "Memory Type",
        ["working", "session", "episodic", "semantic", "decision", "persistent"],
    )
    value = st.text_area("Value", value="Aletheus Genesis 0.4 Memory Core is online.")
    tags = st.text_input("Tags comma-separated", value="genesis,memory,founder")

    if st.button("Remember"):
        payload = {
            "key": key,
            "value": value,
            "namespace": namespace,
            "memory_type": memory_type,
            "tags": [item.strip() for item in tags.split(",") if item.strip()],
        }
        result = runtime_core.commands.dispatch(
            "memory.remember",
            payload,
            application="founder_console",
        )
        st.success("Memory record stored.")
        st.json(result.results)

    st.markdown("### Recall Memory")

    recall_type = st.selectbox(
        "Recall by Memory Type",
        ["", "working", "session", "episodic", "semantic", "decision", "persistent"],
    )

    recall_payload = {}
    if recall_type:
        recall_payload["memory_type"] = recall_type

    recall_result = runtime_core.commands.dispatch("memory.recall", recall_payload)
    memory_rows = recall_result.results.get("memory", [])

    if memory_rows:
        st.dataframe(safe_dataframe(memory_rows), width="stretch")
    else:
        st.info("No memory records found.")

with tabs[2]:
    st.subheader("Aletheus Cognition Core")

    cognition_stats = diagnostics_context.results.get("cognition", {})
    st.markdown("### Cognition Stats")
    st.json(cognition_stats)

    st.markdown("### Create Goal")
    goal_title = st.text_input("Goal Title", value="Increase Card Hawk portfolio value")
    goal_description = st.text_area(
        "Goal Description",
        value="Use Aletheus cognition to plan, reason, and record decisions for portfolio growth.",
    )
    goal_priority = st.selectbox(
        "Priority", ["low", "medium", "high", "critical"], index=2
    )

    if st.button("Create Goal"):
        result = runtime_core.commands.dispatch(
            "goal.create",
            {
                "title": goal_title,
                "description": goal_description,
                "priority": goal_priority,
                "application": "founder_console",
            },
        )
        st.success("Goal created.")
        st.json(result.results)

    st.markdown("### Generate Plan")
    plan_goal_title = st.text_input(
        "Plan Goal Title", value="Increase Card Hawk portfolio value"
    )

    if st.button("Generate Plan"):
        result = runtime_core.commands.dispatch(
            "plan.generate",
            {
                "goal_id": "console",
                "goal_title": plan_goal_title,
            },
        )
        st.success("Plan generated.")
        st.json(result.results)

    st.markdown("### Reason")
    prompt = st.text_area(
        "Reasoning Prompt",
        value="Should Aletheus prioritize marketplace intelligence before acquisition execution?",
    )
    evidence = st.text_input(
        "Evidence comma-separated",
        value="Marketplace data improves price discipline,THORᵡ requires current comps,DEF benefits from structured input",
    )

    if st.button("Evaluate Reasoning"):
        result = runtime_core.commands.dispatch(
            "reason.evaluate",
            {
                "prompt": prompt,
                "evidence": [
                    item.strip() for item in evidence.split(",") if item.strip()
                ],
                "assumptions": ["Current marketplace data may be incomplete"],
            },
        )
        st.success("Reasoning session completed.")
        st.json(result.results)

    st.markdown("### Record Decision")
    decision_title = st.text_input(
        "Decision Title", value="Prioritize Marketplace Intelligence"
    )
    decision_value = st.text_input("Decision", value="Proceed")
    rationale = st.text_area(
        "Rationale",
        value="Marketplace intelligence improves downstream scoring, planning, and acquisition timing.",
    )

    if st.button("Record Decision"):
        result = runtime_core.commands.dispatch(
            "decision.record",
            {
                "title": decision_title,
                "decision": decision_value,
                "rationale": rationale,
                "confidence": 0.88,
                "evidence": ["Runtime Memory Core online", "Cognition Core online"],
            },
        )
        st.success("Decision recorded.")
        st.json(result.results)

    st.markdown("### Active Goals")
    goals = runtime_core.commands.dispatch("goal.list", {}).results.get("goals", [])
    if goals:
        st.dataframe(safe_dataframe(goals), width="stretch")
    else:
        st.info("No goals recorded.")

    st.markdown("### Plans")
    plans = runtime_core.commands.dispatch("plan.list", {}).results.get("plans", [])
    if plans:
        st.dataframe(safe_dataframe(plans), width="stretch")
    else:
        st.info("No plans recorded.")

    st.markdown("### Decisions")
    decisions = runtime_core.commands.dispatch("decision.history", {}).results.get(
        "decisions", []
    )
    if decisions:
        st.dataframe(safe_dataframe(decisions), width="stretch")
    else:
        st.info("No decisions recorded.")

with tabs[3]:
    st.subheader("Aletheus Knowledge Graph Engine")

    knowledge_stats = diagnostics_context.results.get("knowledge", {})
    st.markdown("### Graph Stats")
    st.json(knowledge_stats)

    st.markdown("### Create Entity")
    entity_label = st.text_input("Entity Label", value="Caleb Williams")
    entity_type = st.text_input("Entity Type", value="player")
    entity_properties = st.text_area(
        "Entity Properties JSON-like note",
        value="Chicago Bears quarterback and Card Hawk portfolio target.",
    )

    if st.button("Create Entity"):
        result = runtime_core.commands.dispatch(
            "entity.create",
            {
                "label": entity_label,
                "entity_type": entity_type,
                "properties": {"note": entity_properties},
            },
        )
        st.success("Entity created.")
        st.json(result.results)

    st.markdown("### Search Entities")
    search_label = st.text_input("Search Label", value="")
    search_type = st.text_input("Search Type", value="")

    search_payload = {}
    if search_label:
        search_payload["label"] = search_label
    if search_type:
        search_payload["entity_type"] = search_type

    entities = runtime_core.commands.dispatch(
        "entity.search", search_payload
    ).results.get("entities", [])
    if entities:
        st.dataframe(safe_dataframe(entities), width="stretch")
    else:
        st.info("No entities found.")

    st.markdown("### Create Relationship")
    source_id = st.text_input("Source Entity ID", value="")
    target_id = st.text_input("Target Entity ID", value="")
    relationship_type = st.text_input("Relationship Type", value="related_to")

    if st.button("Create Relationship"):
        result = runtime_core.commands.dispatch(
            "relationship.create",
            {
                "source_id": source_id,
                "target_id": target_id,
                "relationship_type": relationship_type,
                "properties": {"created_from": "runtime_console"},
            },
        )
        st.success("Relationship created.")
        st.json(result.results)

    st.markdown("### Graph Export")
    graph = runtime_core.commands.dispatch("graph.export", {}).results.get("graph", {})
    st.json(graph)

with tabs[4]:
    st.subheader("Aletheus Autonomous Mission Engine")

    mission_stats = diagnostics_context.results.get("mission", {})
    st.markdown("### Mission Stats")
    st.json(mission_stats)

    st.markdown("### Create Mission")
    mission_title = st.text_input(
        "Mission Title", value="Increase Card Hawk portfolio value"
    )
    mission_objective = st.text_area(
        "Mission Objective",
        value="Use Aletheus to observe, reason, evaluate, and recommend portfolio actions.",
    )
    mission_priority = st.selectbox(
        "Mission Priority", ["low", "medium", "high", "critical"], index=2
    )

    if st.button("Create Mission"):
        result = runtime_core.commands.dispatch(
            "mission.create",
            {
                "title": mission_title,
                "objective": mission_objective,
                "application": "founder_console",
                "priority": mission_priority,
                "tasks": [
                    {
                        "title": "Refresh marketplace intelligence",
                        "description": "Collect current market signal.",
                    },
                    {
                        "title": "Run cognitive evaluation",
                        "description": "Generate plan and reasoning.",
                    },
                    {
                        "title": "Record decision",
                        "description": "Persist mission rationale.",
                    },
                ],
            },
        )
        st.success("Mission created.")
        st.json(result.results)

    st.markdown("### Generate Mission From Goal")
    goal_title = st.text_input(
        "Goal → Mission Title", value="Increase Card Hawk portfolio value"
    )

    if st.button("Generate Mission From Goal"):
        result = runtime_core.commands.dispatch(
            "mission.from_goal",
            {
                "goal_title": goal_title,
                "goal_description": "Autonomously generate an execution mission from this founder goal.",
                "application": "founder_console",
                "priority": "high",
            },
        )
        st.success("Mission generated.")
        st.json(result.results)

    st.markdown("### Active Missions")
    missions = runtime_core.commands.dispatch("mission.list", {}).results.get(
        "missions", []
    )
    if missions:
        st.dataframe(safe_dataframe(missions), width="stretch")
    else:
        st.info("No missions recorded.")

    st.markdown("### Run Mission")
    mission_id = st.text_input("Mission ID to Run", value="")

    if st.button("Run Mission"):
        result = runtime_core.commands.dispatch(
            "mission.run",
            {"mission_id": mission_id},
            application="founder_console",
        )
        st.success("Mission run executed.")
        st.json(result.results)

    st.markdown("### Mission History")
    history = runtime_core.commands.dispatch("mission.history", {}).results.get(
        "mission_history", []
    )
    if history:
        st.dataframe(safe_dataframe(history), width="stretch")
    else:
        st.info("No mission runs recorded.")

with tabs[5]:
    st.subheader("Runtime Diagnostics")
    st.json(diagnostics)

with tabs[6]:
    st.subheader("Registered Commands")
    st.dataframe(
        pd.DataFrame({"Command": diagnostics.get("commands", [])}),
        width="stretch",
    )

with tabs[7]:
    st.subheader("Runtime Events")
    events = runtime_core.commands.dispatch("runtime.events").results.get("events", [])
    if events:
        st.dataframe(safe_dataframe(events), width="stretch")
    else:
        st.info("No events recorded.")

with tabs[8]:
    st.subheader("Runtime Metrics")
    metrics = runtime_core.commands.dispatch("runtime.metrics").results.get(
        "metrics", []
    )
    if metrics:
        st.dataframe(safe_dataframe(metrics), width="stretch")
    else:
        st.info("No metrics recorded.")

with tabs[9]:
    st.subheader("Runtime Job Queue")

    command = st.text_input("Command", value="runtime.health")
    application = st.text_input("Application", value="system")

    if st.button("Enqueue Job"):
        job = runtime_core.queue.enqueue(command, {}, application=application)
        st.success(f"Queued job: {job.job_id}")

    if st.button("Run Next Job"):
        job = runtime_core.queue.run_next()
        if job:
            st.success(f"Job completed: {job.job_id} | {job.status}")
            st.json(job.to_dict())
        else:
            st.info("No queued jobs.")

    queue = runtime_core.queue.list()
    if queue:
        st.dataframe(safe_dataframe(queue), width="stretch")
    else:
        st.info("Queue empty.")

with tabs[10]:
    st.subheader("Scheduler")
    jobs = runtime_core.scheduler.list()
    if jobs:
        rows = []
        for name, job in jobs.items():
            rows.append(
                {
                    "Job": name,
                    "Description": job.get("description"),
                    "Last Run": job.get("last_run"),
                    "Last Result": job.get("last_result"),
                }
            )
        st.dataframe(safe_dataframe(rows), width="stretch")
    else:
        st.info("No scheduled jobs.")

with tabs[11]:
    st.subheader("Pipelines")
    st.json(runtime_core.pipelines.list())

with tabs[12]:
    st.subheader("Workflows")
    st.json(runtime_core.workflows.list())

with tabs[13]:
    st.subheader("Plugins")
    st.json(runtime_core.plugins.list())
