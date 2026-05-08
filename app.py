import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Lorentz Transformations", layout="wide")

st.markdown("""<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 0.5rem; padding-bottom: 0; max-width: 100%;}
    [data-testid="stSidebar"] {background-color: #f8f9fa;}
    iframe {border: none !important;}
</style>""", unsafe_allow_html=True)

if 'vectors' not in st.session_state:
    st.session_state.vectors = []

with st.sidebar:
    st.markdown("### Vector Input (S' frame)")
    st.caption("Coordinates are defined in the moving frame S' and will transform with it as you change the velocity.")
    with st.form("add_vec", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            vx = st.number_input("x'", value=1.0, step=0.1, format="%.2f")
        with c2:
            vct = st.number_input("ct'", value=0.5, step=0.1, format="%.2f")
        if st.form_submit_button("Add"):
            st.session_state.vectors.append({"xp": vx, "ctp": vct})
            st.rerun()
    if st.session_state.vectors:
        st.markdown("---")
        for i, v in enumerate(st.session_state.vectors):
            st.text(f"  V{i+1}: x' = {v['xp']:.2f},  ct' = {v['ctp']:.2f}")
        if st.button("Clear All"):
            st.session_state.vectors = []
            st.rerun()

vectors_json = json.dumps(st.session_state.vectors)

html = (Path(__file__).parent / "viz.html").read_text()
html = html.replace("__VECTORS__", vectors_json)

st.components.v1.html(html, height=860, scrolling=False)
