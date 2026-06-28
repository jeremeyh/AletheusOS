import streamlit as st

def render_listing_cards(listings):
    if not listings:
        st.info("No listings found.")
        return

    for item in listings:
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.markdown(f"### {getattr(item, 'title', '')}")
            c1.caption(f"{getattr(item, 'source', '')} • Seller: {getattr(item, 'seller', '')}")
            c2.metric("Ask", f"${float(getattr(item, 'price', 0) or 0):,.2f}")
            c3.write(getattr(item, "status", "active"))

def render_comp_summary(comp):
    estimate = comp.get("estimate", {})
    bands = comp.get("bands", {})

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Low", f"${estimate.get('low', 0):,.2f}")
    c2.metric("Average", f"${estimate.get('average', 0):,.2f}")
    c3.metric("High", f"${estimate.get('high', 0):,.2f}")
    c4.metric("Count", estimate.get("count", 0))

    st.subheader("CardHawk Value Bands™")
    st.json(bands)
