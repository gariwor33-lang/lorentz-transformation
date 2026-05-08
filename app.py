import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(page_title="Lorentz Transformations", layout="wide")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Lorentz Transformation Visualization")
st.markdown("Interactive visualization of the geometry of Minkowski spacetime. The rest frame (S) is represented by orthogonal axes, while the moving frame (S') has skewed axes depending on its relative velocity. The dashed curves represent invariant spacetime intervals (hyperbolas).")

# Initialize session state for custom vectors
if 'custom_vectors' not in st.session_state:
    st.session_state.custom_vectors = []

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    beta = st.slider("Velocity (β = v/c)", min_value=-0.99, max_value=0.99, value=0.0, step=0.01)
    gamma = 1.0 / np.sqrt(1.0 - beta**2)
    
    st.markdown("---")
    st.header("Add Spacetime Vector")
    with st.form("vector_form"):
        col1, col2 = st.columns(2)
        with col1:
            vec_x = st.number_input("x coordinate", value=1.0)
        with col2:
            vec_ct = st.number_input("ct coordinate", value=0.5)
        
        submitted = st.form_submit_button("Add Vector")
        if submitted:
            st.session_state.custom_vectors.append({'x': vec_x, 'ct': vec_ct})
            
    if st.session_state.custom_vectors:
        if st.button("Clear Vectors"):
            st.session_state.custom_vectors = []
            st.rerun()

# Layout
col_plot, col_data = st.columns([2, 1])

with col_plot:
    fig = go.Figure()
    plot_range = 3
    
    # 1. Invariant Hyperbolas (x^2 - ct^2 = +/- 1)
    y_hyper = np.linspace(-plot_range, plot_range, 400)
    x_hyper_right = np.sqrt(1 + y_hyper**2)
    x_hyper_left = -np.sqrt(1 + y_hyper**2)
    
    x_hyper = np.linspace(-plot_range, plot_range, 400)
    y_hyper_top = np.sqrt(1 + x_hyper**2)
    y_hyper_bottom = -np.sqrt(1 + x_hyper**2)

    hyper_kwargs = dict(color="rgba(150, 150, 150, 0.4)", width=1, dash="dash")
    fig.add_trace(go.Scatter(x=x_hyper_right, y=y_hyper, mode="lines", line=hyper_kwargs, hoverinfo='skip', showlegend=False))
    fig.add_trace(go.Scatter(x=x_hyper_left, y=y_hyper, mode="lines", line=hyper_kwargs, hoverinfo='skip', showlegend=False))
    fig.add_trace(go.Scatter(x=x_hyper, y=y_hyper_top, mode="lines", line=hyper_kwargs, hoverinfo='skip', showlegend=False))
    fig.add_trace(go.Scatter(x=x_hyper, y=y_hyper_bottom, mode="lines", line=hyper_kwargs, hoverinfo='skip', showlegend=False))

    # 2. S Frame Axes (Orthogonal)
    axis_s_kwargs = dict(color="rgba(128, 128, 128, 0.8)", width=2)
    fig.add_trace(go.Scatter(x=[-plot_range, plot_range], y=[0, 0], mode="lines", line=axis_s_kwargs, name="x-axis (S)"))
    fig.add_trace(go.Scatter(x=[0, 0], y=[-plot_range, plot_range], mode="lines", line=axis_s_kwargs, name="ct-axis (S)"))
    
    # Unit vectors S
    unit_s_color = "rgba(128, 128, 128, 0.9)"
    fig.add_trace(go.Scatter(x=[1], y=[0], mode="markers+text", marker=dict(color=unit_s_color, size=8), text=[" x=1 "], textposition="bottom right", showlegend=False))
    fig.add_trace(go.Scatter(x=[0], y=[1], mode="markers+text", marker=dict(color=unit_s_color, size=8), text=[" ct=1 "], textposition="top left", showlegend=False))

    # 3. S' Frame Axes (Skewed)
    color_x_prime = "#FF4B4B" # Red
    color_ct_prime = "#0068C9" # Blue
    
    x_prime_axis_x = np.array([-plot_range, plot_range])
    x_prime_axis_y = beta * x_prime_axis_x
    fig.add_trace(go.Scatter(x=x_prime_axis_x, y=x_prime_axis_y, mode="lines", line=dict(color=color_x_prime, width=2), name="x'-axis (S')"))
    
    if abs(beta) > 0.01:
        ct_prime_axis_y = np.array([-plot_range, plot_range])
        ct_prime_axis_x = beta * ct_prime_axis_y
    else:
        ct_prime_axis_x = np.array([0, 0])
        ct_prime_axis_y = np.array([-plot_range, plot_range])
    fig.add_trace(go.Scatter(x=ct_prime_axis_x, y=ct_prime_axis_y, mode="lines", line=dict(color=color_ct_prime, width=2), name="ct'-axis (S')"))

    # Unit vectors S'
    # Unit vector on x': x = gamma, ct = gamma*beta
    fig.add_trace(go.Scatter(x=[gamma], y=[gamma*beta], mode="markers+text", marker=dict(color=color_x_prime, size=8), text=[" x'=1 "], textposition="bottom right", showlegend=False))
    # Unit vector on ct': x = gamma*beta, ct = gamma
    fig.add_trace(go.Scatter(x=[gamma*beta], y=[gamma], mode="markers+text", marker=dict(color=color_ct_prime, size=8), text=[" ct'=1 "], textposition="top left", showlegend=False))

    # Light cone (x = +/- ct)
    light_cone_kwargs = dict(color="rgba(255, 200, 0, 0.5)", width=1, dash="dot")
    fig.add_trace(go.Scatter(x=[-plot_range, plot_range], y=[-plot_range, plot_range], mode="lines", line=light_cone_kwargs, name="Light Cone"))
    fig.add_trace(go.Scatter(x=[-plot_range, plot_range], y=[plot_range, -plot_range], mode="lines", line=light_cone_kwargs, showlegend=False))

    # 4. Custom Vectors
    custom_colors = ["#00CC96", "#AB63FA", "#FFA15A", "#19D3F3", "#FF6692", "#B6E880"]
    for i, vec in enumerate(st.session_state.custom_vectors):
        cx, cct = vec['x'], vec['ct']
        color = custom_colors[i % len(custom_colors)]
        
        # Draw vector as arrow from origin
        fig.add_annotation(
            x=cx, y=cct,
            ax=0, ay=0,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor=color
        )
        
        # Calculate transformed coordinates for hover
        cx_prime = gamma * (cx - beta * cct)
        cct_prime = gamma * (cct - beta * cx)
        
        fig.add_trace(go.Scatter(
            x=[cx], y=[cct],
            mode="markers",
            marker=dict(color=color, size=8, symbol="diamond"),
            name=f"Vector {i+1}",
            hovertemplate=f"S: ({cx:.2f}, {cct:.2f})<br>S': ({{{{customdata[0]:.2f}}}}, {{{{customdata[1]:.2f}}}})<extra></extra>",
            customdata=[[cx_prime, cct_prime]]
        ))

    # Formatting
    fig.update_layout(
        xaxis=dict(range=[-plot_range, plot_range], zeroline=False, showgrid=False, title="Space (x)"),
        yaxis=dict(range=[-plot_range, plot_range], zeroline=False, showgrid=False, title="Time (ct)", scaleanchor="x", scaleratio=1),
        margin=dict(l=20, r=20, b=20, t=20),
        legend=dict(
            yanchor="top", y=0.99, 
            xanchor="left", x=0.01, 
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(128,128,128,0.2)",
            borderwidth=1
        ),
        dragmode="pan",
        hovermode="closest"
    )
    
    st.plotly_chart(fig, use_container_width=True, theme="streamlit", config={'scrollZoom': True})

with col_data:
    st.subheader("System Data")
    st.markdown(f"**Velocity (β):** `{beta:.3f}`")
    st.markdown(f"**Lorentz factor (γ):** `{gamma:.3f}`")
    
    if st.session_state.custom_vectors:
        st.markdown("---")
        st.subheader("Vectors")
        vector_data = []
        for i, vec in enumerate(st.session_state.custom_vectors):
            x, ct = vec['x'], vec['ct']
            x_prime = gamma * (x - beta * ct)
            ct_prime = gamma * (ct - beta * x)
            invariant = x**2 - ct**2
            vector_data.append({
                "Id": f"V{i+1}",
                "x": f"{x:.2f}",
                "ct": f"{ct:.2f}",
                "x'": f"{x_prime:.2f}",
                "ct'": f"{ct_prime:.2f}",
                "s²": f"{invariant:.2f}"
            })
        st.dataframe(pd.DataFrame(vector_data), hide_index=True, use_container_width=True)
