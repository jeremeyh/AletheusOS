import streamlit as st


def render_timeline(events):
    """
    CardHawkOS Live Mission Timeline™
    """

    st.subheader("📜 Live Mission Timeline™")

    if not events:

        st.info("No activity recorded.")

        return

    for event in reversed(events):

        icon = event.get(
            "icon",
            "⚪",
        )

        title = event.get(
            "title",
            "Unknown",
        )

        description = event.get(
            "description",
            "",
        )

        timestamp = event.get(
            "timestamp",
            "",
        )

        with st.container(border=True):

            st.markdown(
                f"""
### {icon} {title}

{description}

<small>{timestamp}</small>
""",
                unsafe_allow_html=True,
            )
