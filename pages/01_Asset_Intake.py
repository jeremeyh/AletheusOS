import streamlit as st
from pathlib import Path

st.title("📸 Asset Intake")

upload = st.file_uploader(
    "Upload Card Image",
    type=["jpg","jpeg","png","webp"]
)

if upload:

    save_path = Path("uploads/incoming") / upload.name

    with open(save_path,"wb") as fp:
        fp.write(upload.getbuffer())

    st.success(f"Saved: {save_path.name}")

    st.image(upload)
