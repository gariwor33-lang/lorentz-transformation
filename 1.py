import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Special Relativity Visualizer", layout="wide")

# 2. Main Title and Description
st.title("🛰️ Lorentz Transformations Visualization")
st.markdown("""
This application demonstrates the concept of **hyperbolic rotation** in Minkowski spacetime. 
As the relative velocity $v$ changes, the axes of the moving reference frame ($K'$) tilt asymptotically towards the light cone.
""")

# 3. Sidebar Configuration for Parameters
st.sidebar.header("System Parameters")
beta = st.sidebar.slider("Relative Velocity (v/c)", 0.0, 0.99, 0.60, step=0.01)

# 4. Relativistic Calculations
gamma = 1 / np.sqrt(1 - beta ** 2)
phi = np.arctanh(beta)  # Angle of hyperbolic rotation (rapidity)

# 5. Dynamic Metrics Display
col1, col2 = st.columns(2)
col1.metric("Lorentz Factor (γ)", f"{gamma:.4f}")
col2.metric("Rapidity / Rotation Angle (rad)", f"{phi:.4f}")

# 6. Figure Initialization
fig = go.Figure()
lim = 10  # Coordinate limit

# 7. Static Elements: The Light Cone
t_light = np.linspace(-lim, lim, 100)
fig.add_trace(go.Scatter(x=t_light, y=t_light, name="Light (x=ct)",
                         line=dict(color="orange", dash="dash", width=2), opacity=0.6))
fig.add_trace(go.Scatter(x=t_light, y=-t_light, name="Light (x=-ct)",
                         line=dict(color="orange", dash="dash", width=2), opacity=0.6))

# 8. Dynamic Elements: K' Axes (Moving Frame)
# x' axis: where ct' = 0 => ct = beta * x
x_vals = np.array([-lim, lim]) * gamma
ct_x = beta * x_vals
fig.add_trace(go.Scatter(x=x_vals, y=ct_x, name="x' Axis",
                         line=dict(color="#FF4B4B", width=4)))

# ct' axis: where x' = 0 => x = beta * ct
ct_vals = np.array([-lim, lim]) * gamma
x_ct = beta * ct_vals
fig.add_trace(go.Scatter(x=x_ct, y=ct_vals, name="ct' Axis",
                         line=dict(color="#1C83E1", width=4)))

# 9. Invariant Interval Hyperbolas (s^2 = x^2 - (ct)^2)
# Demonstrates the geometric locus of points with a constant spacetime interval
for s in [2, 4, 6, 8]:
    # Space-like intervals
    hyp_x = s * np.cosh(np.linspace(-2, 2, 100))
    hyp_ct = s * np.sinh(np.linspace(-2, 2, 100))
    fig.add_trace(go.Scatter(x=hyp_x, y=hyp_ct, mode='lines',
                             line=dict(color='rgba(255, 255, 255, 0.15)', width=1), showlegend=False))
    fig.add_trace(go.Scatter(x=-hyp_x, y=hyp_ct, mode='lines',
                             line=dict(color='rgba(255, 255, 255, 0.15)', width=1), showlegend=False))

    # Time-like intervals
    fig.add_trace(go.Scatter(x=hyp_ct, y=hyp_x, mode='lines',
                             line=dict(color='rgba(255, 255, 255, 0.15)', width=1), showlegend=False))
    fig.add_trace(go.Scatter(x=hyp_ct, y=-hyp_x, mode='lines',
                             line=dict(color='rgba(255, 255, 255, 0.15)', width=1), showlegend=False))

# 10. Layout Styling and Constraints
fig.update_layout(
    xaxis=dict(title="Space (x)", range=[-lim, lim], gridcolor="#333333", zeroline=True, zerolinecolor="white"),
    yaxis=dict(title="Time (ct)", range=[-lim, lim], gridcolor="#333333", zeroline=True, zerolinecolor="white",
               scaleanchor="x", scaleratio=1),
    height=800,
    template="plotly_dark",
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(0,0,0,0.5)")
)

# 11. Render the Plot
st.plotly_chart(fig, use_container_width=True)

# 12. Mathematical Background Section
with st.expander("Show Mathematical Background"):
    st.markdown("### The Lorentz Transformation Matrix")
    st.latex(r"""
    \begin{pmatrix} ct' \\ x' \end{pmatrix} = 
    \begin{pmatrix} \gamma & -\beta\gamma \\ -\beta\gamma & \gamma \end{pmatrix}
    \begin{pmatrix} ct \\ x \end{pmatrix}
    """)
    st.markdown("### Spacetime Interval Invariance")
    st.markdown("The invariance of the spacetime interval is expressed geometrically as hyperbolas:")
    st.latex(r"s^2 = (ct)^2 - x^2 = (ct')^2 - (x')^2")