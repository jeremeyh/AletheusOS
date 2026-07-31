import streamlit as st

ENGINES = [
    ("🦅", "Hawk A•Eye™", "Online"),
    ("⚡", "THORᵡ™", "Online"),
    ("💰", "Marketplace", "Online"),
    ("🤝", "Negotiation AI™", "Online"),
    ("🧠", "Founder AI™", "Online"),
    ("🧬", "Digital Twin™", "Online"),
    ("📡", "Event Bus™", "Online"),
    ("📜", "Timeline™", "Online"),
]


def render_engine_health():
    """
    CardHawkOS Engine Health Panel.
    """

    st.subheader("⚙ Engine Health")

    for icon, name, status in ENGINES:
        left, right = st.columns([4, 1])

        with left:
            st.write(f"{icon} {name}")

        with right:
            st.success("●")
