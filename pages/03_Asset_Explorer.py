import sqlite3

import pandas as pd
import streamlit as st

DB = "data/cardhawk.db"

st.set_page_config(
    page_title="Asset Explorer™",
    page_icon="🦅",
    layout="wide",
)

st.title("🦅 Asset Explorer™")

conn = sqlite3.connect(DB)

query = """
SELECT
    id,
    player,
    brand,
    set_name,
    parallel,
    grade,
    current_value,
    purchase_price,
    thorx_score,
    created_at
FROM assets
ORDER BY current_value DESC
"""

df = pd.read_sql_query(query, conn)

conn.close()

st.metric(
    "Assets",
    len(df)
)

search = st.text_input(
    "Search Player / Brand / Set"
)

if search:

    mask = (
        df["player"].fillna("").str.contains(search, case=False)
        |
        df["brand"].fillna("").str.contains(search, case=False)
        |
        df["set_name"].fillna("").str.contains(search, case=False)
    )

    df = df[mask]

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

st.subheader("Asset Details")

if len(df):

    asset = st.selectbox(
        "Select Asset",
        df["id"],
    )

    row = df[df["id"] == asset].iloc[0]

    left, right = st.columns(2)

    with left:

        st.write("### Card")

        st.write(row["player"])
        st.write(row["brand"])
        st.write(row["set_name"])
        st.write(row["parallel"])
        st.write(row["grade"])

    with right:

        st.write("### Intelligence")

        st.metric(
            "Current Value",
            f"${float(row['current_value'] or 0):,.2f}",
        )

        st.metric(
            "Purchase",
            f"${float(row['purchase_price'] or 0):,.2f}",
        )

        st.metric(
            "THORᵡ",
            round(float(row["thorx_score"] or 0), 2),
        )
