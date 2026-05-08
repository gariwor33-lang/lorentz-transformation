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
    st.markdown("### About")
    st.markdown(
        "This interactive diagram visualizes how two inertial "
        "reference frames, S and S', are related by the "
        "**Lorentz transformation** -- the fundamental symmetry "
        "of special relativity that preserves the spacetime interval."
    )

    with st.expander("Theory", expanded=False):
        st.markdown(
            "An event with coordinates $(x, ct)$ in frame S "
            "has coordinates in a frame S' moving with velocity "
            "$v = \\beta c$ given by the boost:"
        )
        st.latex(r"""
            \begin{pmatrix} x' \\ ct' \end{pmatrix}
            = \gamma
            \begin{pmatrix} 1 & -\beta \\ -\beta & 1 \end{pmatrix}
            \begin{pmatrix} x \\ ct \end{pmatrix},
            \quad
            \gamma = \frac{1}{\sqrt{1 - \beta^2}}
        """)
        st.markdown(
            "The quantity $s^2 = (ct)^2 - x^2$ is invariant under "
            "this transformation. Curves of constant $s^2$ form "
            "**hyperbolas** on the diagram. As $\\beta$ varies, the "
            "unit basis vectors of S' slide along the unit hyperbolas "
            "$x^2 - (ct)^2 = \\pm 1$, illustrating how the geometry "
            "of spacetime differs from Euclidean space."
        )
        st.markdown(
            "The dashed diagonal lines represent the **light cone** "
            "($x = \\pm ct$), which remains invariant under all "
            "Lorentz boosts."
        )

    st.markdown("---")
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
