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
    page_title="Aletheus Founder Workspace",
    page_icon="🧠",
    layout="wide",
)

overview_context = runtime_core.commands.dispatch("workspace.overview")
overview = overview_context.results.get("workspace", {})
runtime = overview.get("runtime", {})

st.title("Aletheus™ Founder Workspace")
st.caption("Aletheus v2.0A | Autonomous Kernel & Event Bus | 6th Dimension Multimedia")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Runtime", runtime.get("status", "unknown"))
col2.metric("Version", runtime.get("version", "unknown"))
col3.metric("Active Missions", runtime.get("active_missions", 0))
col4.metric("Kernel Events", runtime.get("kernel_events", 0))

col5, col6, col7, col8 = st.columns(4)
col5.metric("Memory Records", runtime.get("memory_records", 0))
col6.metric("Knowledge Entities", runtime.get("knowledge_entities", 0))
col7.metric("Notifications", overview.get("notifications", 0))
col8.metric("Journal Entries", overview.get("journal_entries", 0))

st.divider()

tabs = st.tabs(
    [
        "Overview",
        "Executive Intelligence",
        "Founder Copilot",
        "Universal Intelligence",
        "Prediction",
        "Learning",
        "Kernel",
        "Agents",
        "Planning",
        "Applications",
        "Semantic Intelligence",
        "Objectives",
        "Missions",
        "Journal",
        "Notifications",
        "Knowledge",
        "Memory",
        "Runtime",
    ]
)

with tabs[0]:
    st.subheader("Executive Overview")
    st.json(overview)

with tabs[1]:
    st.subheader("Executive Intelligence Layer")

    executive_status = runtime_core.commands.dispatch("executive.status", {}).results.get("executive_status", {})
    st.markdown("### Executive Status")
    st.json(executive_status)

    col_exec_1, col_exec_2, col_exec_3 = st.columns(3)

    with col_exec_1:
        if st.button("Generate Daily Brief"):
            result = runtime_core.commands.dispatch("executive.daily_brief", {})
            st.success("Daily brief generated.")
            st.json(result.results)

    with col_exec_2:
        if st.button("Generate Recommendations"):
            result = runtime_core.commands.dispatch("executive.recommendations", {})
            st.success("Recommendations generated.")
            st.json(result.results)

    with col_exec_3:
        if st.button("Analyze Risks"):
            result = runtime_core.commands.dispatch("executive.risks", {})
            st.warning("Risk analysis completed.")
            st.json(result.results)

    st.markdown("### Executive Summary")
    summary = runtime_core.commands.dispatch("executive.summary", {}).results.get("summary", {})
    st.json(summary)

    st.markdown("### System Report")
    report = runtime_core.commands.dispatch("executive.system_report", {}).results.get("system_report", {})
    st.json(report)

with tabs[2]:
    st.subheader("Founder Copilot")

    copilot_stats = runtime_core.commands.dispatch("copilot.stats", {}).results.get("copilot_stats", {})
    st.markdown("### Copilot Status")
    st.json(copilot_stats)

    prompt = st.text_area(
        "Ask Aletheus",
        value="What should I work on next for Card Hawk Foundation?",
    )

    if st.button("Ask Copilot"):
        result = runtime_core.commands.dispatch(
            "copilot.ask",
            {"prompt": prompt},
            application="founder_workspace",
        )
        st.success("Copilot response generated.")
        st.json(result.results)

    col_cp1, col_cp2, col_cp3 = st.columns(3)

    with col_cp1:
        if st.button("Founder Brief"):
            result = runtime_core.commands.dispatch("copilot.brief", {})
            st.json(result.results)

    with col_cp2:
        if st.button("Copilot Recommendations"):
            result = runtime_core.commands.dispatch("copilot.recommend", {})
            st.json(result.results)

    with col_cp3:
        if st.button("Copilot Timeline"):
            result = runtime_core.commands.dispatch("copilot.timeline", {})
            st.json(result.results)

    history = runtime_core.commands.dispatch("copilot.history", {}).results.get("history", [])
    if history:
        st.markdown("### Copilot History")
        st.dataframe(safe_dataframe(history), width="stretch")
    else:
        st.info("No copilot exchanges yet.")

with tabs[3]:
    st.subheader("Universal Intelligence Layer")

    uil_stats = runtime_core.commands.dispatch("uil.stats", {}).results.get("uil_stats", {})
    st.markdown("### Universal Intelligence Status")
    st.json(uil_stats)

    question = st.text_area(
        "Ask the Universal Intelligence Layer",
        value="What should Aletheus prioritize next for Card Hawk Foundation?",
    )

    col_uil_1, col_uil_2, col_uil_3 = st.columns(3)

    with col_uil_1:
        if st.button("Build Context"):
            result = runtime_core.commands.dispatch("uil.context", {"question": question})
            st.json(result.results)

    with col_uil_2:
        if st.button("Reason"):
            result = runtime_core.commands.dispatch("uil.reason", {"question": question})
            st.json(result.results)

    with col_uil_3:
        if st.button("Decide"):
            result = runtime_core.commands.dispatch("uil.decide", {"question": question})
            st.success("Decision generated.")
            st.json(result.results)

    col_uil_4, col_uil_5, col_uil_6 = st.columns(3)

    with col_uil_4:
        if st.button("Synthesize"):
            result = runtime_core.commands.dispatch("uil.synthesize", {"question": question})
            st.json(result.results)

    with col_uil_5:
        if st.button("Universal Brief"):
            result = runtime_core.commands.dispatch("uil.brief", {})
            st.json(result.results)

    with col_uil_6:
        if st.button("UIL Timeline"):
            result = runtime_core.commands.dispatch("uil.timeline", {})
            st.json(result.results)

    snapshot = runtime_core.commands.dispatch("uil.snapshot", {}).results.get("snapshot", {})
    st.markdown("### Intelligence Snapshot")
    st.json(snapshot)

with tabs[4]:
    st.subheader("Predictive Intelligence Layer")

    prediction_stats = runtime_core.commands.dispatch("predict.stats", {}).results.get("prediction_stats", {})
    st.markdown("### Prediction Stats")
    st.json(prediction_stats)

    col_pred_1, col_pred_2, col_pred_3 = st.columns(3)

    with col_pred_1:
        if st.button("Generate Forecast"):
            result = runtime_core.commands.dispatch("predict.forecast", {"horizon": "next sprint"})
            st.json(result.results)

    with col_pred_2:
        if st.button("Scan Risks"):
            result = runtime_core.commands.dispatch("predict.risks", {})
            st.warning("Predictive risks scanned.")
            st.json(result.results)

    with col_pred_3:
        if st.button("Find Opportunities"):
            result = runtime_core.commands.dispatch("predict.opportunities", {})
            st.success("Predictive opportunities generated.")
            st.json(result.results)

    st.markdown("### Scenario Simulator")
    scenario_title = st.text_input("Scenario Title", value="Card Hawk Marketplace Integration")
    scenario_premise = st.text_area(
        "Scenario Premise",
        value="What happens if Card Hawk Marketplace Intelligence becomes the next native service integration?",
    )

    if st.button("Run Scenario"):
        result = runtime_core.commands.dispatch(
            "predict.scenario",
            {
                "title": scenario_title,
                "premise": scenario_premise,
            },
        )
        st.json(result.results)

    if st.button("Generate Predictive Recommendations"):
        result = runtime_core.commands.dispatch("predict.recommend", {})
        st.success("Predictive recommendations generated.")
        st.json(result.results)

    timeline = runtime_core.commands.dispatch("predict.timeline", {}).results.get("timeline", {})
    st.markdown("### Prediction Timeline")
    st.json(timeline)

with tabs[5]:
    st.subheader("Adaptive Learning Engine")

    learning_stats = runtime_core.commands.dispatch("learn.stats", {}).results.get("learning_stats", {})
    st.markdown("### Learning Stats")
    st.json(learning_stats)

    st.markdown("### Record Experience")
    event_type = st.text_input("Event Type", value="prediction")
    description = st.text_area(
        "Experience Description",
        value="Aletheus generated a predictive recommendation for Card Hawk Foundation.",
    )
    outcome = st.selectbox("Outcome", ["unknown", "successful", "failed", "partial"], index=0)

    if st.button("Record Experience"):
        result = runtime_core.commands.dispatch(
            "learn.record",
            {
                "event_type": event_type,
                "description": description,
                "source": "founder_workspace",
                "outcome": outcome,
                "confidence": 0.82,
                "metadata": {"version": "1.8.0"},
            },
        )
        st.success("Learning experience recorded.")
        st.json(result.results)

    st.markdown("### Create Lesson")
    lesson_title = st.text_input("Lesson Title", value="Card Hawk integration improves Aletheus utility")
    lesson_body = st.text_area(
        "Lesson",
        value="Native Card Hawk integration creates richer feedback loops across prediction, planning, agents, and memory.",
    )

    if st.button("Create Lesson"):
        result = runtime_core.commands.dispatch(
            "learn.lesson",
            {
                "title": lesson_title,
                "lesson": lesson_body,
                "confidence": 0.88,
                "tags": ["cardhawk", "learning", "integration"],
            },
        )
        st.success("Lesson created.")
        st.json(result.results)

    col_l1, col_l2, col_l3 = st.columns(3)

    with col_l1:
        if st.button("Discover Patterns"):
            result = runtime_core.commands.dispatch("learn.patterns", {})
            st.json(result.results)

    with col_l2:
        if st.button("Suggest Improvements"):
            result = runtime_core.commands.dispatch("learn.improve", {})
            st.json(result.results)

    with col_l3:
        if st.button("Learning Snapshot"):
            result = runtime_core.commands.dispatch("learn.snapshot", {})
            st.json(result.results)

with tabs[6]:
    st.subheader("Aletheus v2 Autonomous Kernel")

    kernel_stats = runtime_core.commands.dispatch("kernel.stats", {}).results.get("kernel_stats", {})
    st.markdown("### Kernel Stats")
    st.json(kernel_stats)

    col_k1, col_k2, col_k3 = st.columns(3)

    with col_k1:
        if st.button("Boot Kernel"):
            result = runtime_core.commands.dispatch("kernel.boot", {})
            st.success("Kernel booted.")
            st.json(result.results)

    with col_k2:
        if st.button("Sync Runtime"):
            result = runtime_core.commands.dispatch("kernel.sync", {})
            st.success("Runtime synchronized into kernel.")
            st.json(result.results)

    with col_k3:
        if st.button("Kernel Snapshot"):
            result = runtime_core.commands.dispatch("kernel.snapshot", {})
            st.json(result.results)

    st.markdown("### Publish Kernel Event")
    event_type = st.text_input("Event Type", value="founder.kernel.test")
    event_source = st.text_input("Event Source", value="founder_workspace")
    event_message = st.text_area("Event Payload Message", value="Founder manually published a kernel event.")

    if st.button("Publish Event"):
        result = runtime_core.commands.dispatch(
            "kernel.publish",
            {
                "event_type": event_type,
                "source": event_source,
                "payload": {"message": event_message},
            },
        )
        st.success("Kernel event published.")
        st.json(result.results)

    status = runtime_core.commands.dispatch("kernel.status", {}).results.get("kernel", {})
    st.markdown("### Kernel Status")
    st.json(status)

with tabs[7]:
    st.subheader("Multi-Agent Orchestration")

    agent_stats = runtime_core.commands.dispatch("agent.stats", {}).results.get("agent_stats", {})
    st.markdown("### Agent Stats")
    st.json(agent_stats)

    if st.button("Bootstrap Default Agents"):
        result = runtime_core.commands.dispatch("agent.bootstrap", {})
        st.success("Default agents bootstrapped.")
        st.json(result.results)

    st.markdown("### Orchestrate Objective")
    objective = st.text_area(
        "Objective",
        value="Prepare Card Hawk Foundation for deeper native Aletheus integration.",
    )

    if st.button("Run Multi-Agent Orchestration"):
        result = runtime_core.commands.dispatch(
            "agent.orchestrate",
            {"objective": objective},
        )
        st.success("Orchestration completed.")
        st.json(result.results)

    st.markdown("### Assign Agent Task")
    agent_name = st.text_input("Agent Name", value="Executive Agent")
    task_title = st.text_input("Task Title", value="Summarize current system priorities")

    if st.button("Assign Task"):
        result = runtime_core.commands.dispatch(
            "agent.task.assign",
            {
                "agent_name": agent_name,
                "title": task_title,
                "payload": {"source": "founder_workspace"},
            },
        )
        st.success("Task assigned.")
        st.json(result.results)

    if st.button("Run Agent"):
        result = runtime_core.commands.dispatch(
            "agent.run",
            {"agent_name": agent_name},
        )
        st.success("Agent run completed.")
        st.json(result.results)

    agents = runtime_core.commands.dispatch("agent.list", {}).results.get("agents", [])
    if agents:
        st.markdown("### Agents")
        st.dataframe(safe_dataframe(agents), width="stretch")
    else:
        st.info("No agents registered.")

with tabs[8]:
    st.subheader("Autonomous Planning Engine")

    planning_stats = runtime_core.commands.dispatch("planning.stats", {}).results.get("planning_stats", {})
    st.markdown("### Planning Stats")
    st.json(planning_stats)

    st.markdown("### Create Autonomous Plan")
    objective = st.text_area(
        "Planning Objective",
        value="Prepare Card Hawk Foundation for full native Aletheus operation.",
    )

    if st.button("Create Autonomous Plan"):
        result = runtime_core.commands.dispatch(
            "planning.create",
            {
                "objective": objective,
                "priority": "critical",
            },
        )
        st.success("Autonomous plan created.")
        st.json(result.results)

    st.markdown("### Execute Plan")
    plan_id = st.text_input("Plan ID", value="")

    col_plan_1, col_plan_2 = st.columns(2)

    with col_plan_1:
        if st.button("Execute Next Step"):
            result = runtime_core.commands.dispatch(
                "planning.execute_next",
                {"plan_id": plan_id},
            )
            st.success("Next planning step executed.")
            st.json(result.results)

    with col_plan_2:
        if st.button("Execute Full Plan"):
            result = runtime_core.commands.dispatch(
                "planning.execute",
                {"plan_id": plan_id},
            )
            st.success("Full plan executed.")
            st.json(result.results)

    plans = runtime_core.commands.dispatch("planning.list", {}).results.get("plans", [])
    if plans:
        st.markdown("### Plans")
        st.dataframe(safe_dataframe(plans), width="stretch")
    else:
        st.info("No autonomous plans recorded.")

with tabs[9]:
    st.subheader("Native Applications")

    applications = runtime_core.commands.dispatch("application.list", {}).results.get("applications", [])
    if applications:
        st.dataframe(safe_dataframe(applications), width="stretch")
    else:
        st.info("No applications registered.")

    st.markdown("### Card Hawk Foundation™")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        if st.button("Bootstrap Card Hawk Foundation™"):
            result = runtime_core.commands.dispatch("cardhawk.foundation.bootstrap", {})
            st.success("Card Hawk Foundation bootstrapped.")
            st.json(result.results)

    with col_b:
        if st.button("Start Card Hawk Foundation™"):
            result = runtime_core.commands.dispatch("cardhawk.start", {})
            st.success("Card Hawk Foundation started.")
            st.json(result.results)

    with col_c:
        if st.button("Stop Card Hawk Foundation™"):
            result = runtime_core.commands.dispatch("cardhawk.stop", {})
            st.warning("Card Hawk Foundation stopped.")
            st.json(result.results)

    st.markdown("### Card Hawk Status")
    cardhawk = runtime_core.commands.dispatch("cardhawk.status", {}).results.get("cardhawk", {})
    st.json(cardhawk)

with tabs[10]:
    st.subheader("Semantic Intelligence Layer")

    semantic = runtime_core.commands.dispatch("semantic.stats", {}).results.get("semantic_stats", {})
    st.markdown("### Semantic Stats")
    st.json(semantic)

    if st.button("Bootstrap Card Hawk Semantics"):
        result = runtime_core.commands.dispatch("semantic.bootstrap.cardhawk", {})
        st.success("Card Hawk semantic layer bootstrapped.")
        st.json(result.results)

    st.markdown("### Create Concept")
    concept_name = st.text_input("Concept Name", value="Caleb Williams")
    concept_type = st.text_input("Concept Type", value="player")
    concept_description = st.text_area(
        "Concept Description",
        value="Chicago Bears quarterback and Card Hawk portfolio target.",
    )

    if st.button("Create Semantic Concept"):
        result = runtime_core.commands.dispatch(
            "semantic.concept.create",
            {
                "name": concept_name,
                "concept_type": concept_type,
                "description": concept_description,
                "aliases": [],
                "metadata": {"created_from": "founder_workspace"},
            },
        )
        st.success("Concept created.")
        st.json(result.results)

    st.markdown("### Assert Fact")
    subject = st.text_input("Subject", value="Caleb Williams")
    predicate = st.text_input("Predicate", value="plays_for")
    object_value = st.text_input("Object", value="Chicago Bears")

    if st.button("Assert Semantic Fact"):
        result = runtime_core.commands.dispatch(
            "semantic.assert",
            {
                "subject": subject,
                "predicate": predicate,
                "object_value": object_value,
                "confidence": 0.9,
                "source": "founder_workspace",
            },
        )
        st.success("Assertion recorded.")
        st.json(result.results)

    st.markdown("### Explain Concept")
    explain_name = st.text_input("Explain", value="Caleb Williams")

    if st.button("Explain"):
        result = runtime_core.commands.dispatch(
            "semantic.explain",
            {"name": explain_name},
        )
        st.json(result.results)

    concepts = runtime_core.commands.dispatch("semantic.concept.search", {}).results.get("concepts", [])
    if concepts:
        st.markdown("### Concepts")
        st.dataframe(safe_dataframe(concepts), width="stretch")

    assertions = runtime_core.commands.dispatch("semantic.query", {}).results.get("assertions", [])
    if assertions:
        st.markdown("### Assertions")
        st.dataframe(safe_dataframe(assertions), width="stretch")

with tabs[11]:
    st.subheader("Strategic Objectives")

    title = st.text_input("Objective Title", value="Prepare Card Hawk Foundation for native Aletheus integration")
    description = st.text_area(
        "Objective Description",
        value="Move Card Hawk Foundation into Aletheus as the first flagship reference application.",
    )
    priority = st.selectbox("Priority", ["low", "medium", "high", "critical"], index=3)

    if st.button("Create Objective"):
        result = runtime_core.commands.dispatch(
            "objective.create",
            {
                "title": title,
                "description": description,
                "priority": priority,
                "application": "founder_workspace",
            },
        )
        st.success("Objective created.")
        st.json(result.results)

    objectives = runtime_core.commands.dispatch("objective.list", {}).results.get("objectives", [])
    if objectives:
        st.dataframe(safe_dataframe(objectives), width="stretch")
    else:
        st.info("No objectives recorded.")

with tabs[12]:
    st.subheader("Mission Command")

    mission_title = st.text_input("Mission Title", value="Integrate Card Hawk Foundation")
    mission_objective = st.text_area(
        "Mission Objective",
        value="Register Card Hawk Foundation as the first native Aletheus application.",
    )

    if st.button("Create Integration Mission"):
        result = runtime_core.commands.dispatch(
            "mission.create",
            {
                "title": mission_title,
                "objective": mission_objective,
                "application": "founder_workspace",
                "priority": "critical",
                "tasks": [
                    {"title": "Register application", "description": "Create native application record."},
                    {"title": "Register Card Hawk services", "description": "Expose Asset Vault, Portfolio, Marketplace, and engines."},
                    {"title": "Connect knowledge graph", "description": "Create graph entities and relationships."},
                    {"title": "Record founder decision", "description": "Persist rationale and milestone."},
                ],
            },
        )
        st.success("Mission created.")
        st.json(result.results)

    missions = runtime_core.commands.dispatch("mission.list", {}).results.get("missions", [])
    if missions:
        st.dataframe(safe_dataframe(missions), width="stretch")
    else:
        st.info("No missions recorded.")

with tabs[13]:
    st.subheader("Founder Journal")

    journal_title = st.text_input("Journal Title", value="Genesis 0.8 Founder Workspace")
    journal_body = st.text_area(
        "Journal Body",
        value="Aletheus Founder Workspace is now the executive operating surface for the platform.",
    )
    category = st.text_input("Category", value="genesis")
    tags = st.text_input("Tags comma-separated", value="founder,workspace,genesis")

    if st.button("Create Journal Entry"):
        result = runtime_core.commands.dispatch(
            "founder.journal.create",
            {
                "title": journal_title,
                "body": journal_body,
                "category": category,
                "tags": [item.strip() for item in tags.split(",") if item.strip()],
            },
        )
        st.success("Journal entry created.")
        st.json(result.results)

    journal = runtime_core.commands.dispatch("founder.journal.list", {}).results.get("journal", [])
    if journal:
        st.dataframe(safe_dataframe(journal), width="stretch")
    else:
        st.info("No journal entries recorded.")

with tabs[14]:
    st.subheader("Notifications")

    if st.button("Create Genesis Notification"):
        result = runtime_core.commands.dispatch(
            "notification.create",
            {
                "title": "Genesis 0.8 Online",
                "message": "Founder Workspace has been activated.",
                "severity": "success",
                "source": "founder_workspace",
            },
        )
        st.success("Notification created.")
        st.json(result.results)

    notifications = runtime_core.commands.dispatch("notification.list", {}).results.get("notifications", [])
    if notifications:
        st.dataframe(safe_dataframe(notifications), width="stretch")
    else:
        st.info("No notifications recorded.")

with tabs[15]:
    st.subheader("Knowledge Graph Snapshot")
    graph = runtime_core.commands.dispatch("graph.export", {}).results.get("graph", {})
    st.json(graph)

with tabs[16]:
    st.subheader("Memory Snapshot")
    memory = runtime_core.commands.dispatch("memory.recall", {"limit": 50}).results.get("memory", [])
    if memory:
        st.dataframe(safe_dataframe(memory), width="stretch")
    else:
        st.info("No memory records found.")

with tabs[17]:
    st.subheader("Runtime Diagnostics")
    diagnostics = runtime_core.commands.dispatch("runtime.diagnostics").results
    st.json(diagnostics)
