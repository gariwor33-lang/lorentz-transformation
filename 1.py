import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Special Relativity Visualizer", layout="wide")

# 2. Main Title and Description
st.title("Lorentz Transformations Visualization")
st.markdown("""
This application demonstrates the concept of **hyperbolic rotation** in Minkowski spacetime. 
As the relative velocity $v$ changes, the axes of the moving reference frame ($K'$) tilt asymptotically towards the light cone.
The points represent the unit vectors of the moving frame, illustrating the scale change (length contraction and time dilation).
""")

# 3. Sidebar Configuration for Parameters
st.sidebar.header("System Parameters")
beta = st.sidebar.slider("Relative Velocity (v/c)", 0.0, 0.99, 0.0, step=0.01)

# 4. Relativistic Calculations
gamma = 1 / np.sqrt(1 - beta**2)
phi = np.arctanh(beta) # Angle of hyperbolic rotation (rapidity)

# 5. Dynamic Metrics Display
col1, col2 = st.columns(2)
col1.metric("Lorentz Factor (γ)", f"{gamma:.4f}")
col2.metric("Rapidity / Rotation Angle (rad)", f"{phi:.4f}")

# 6. Figure Initialization
fig = go.Figure()
lim = 4  # Reduced coordinate limit for better visibility of unit vectors

# 7. Static Elements: The Light Cone
t_light = np.linspace(-lim, lim, 100)
fig.add_trace(go.Scatter(x=t_light, y=t_light, name="Light (x=ct)", 
                         line=dict(color="gray", dash="dash", width=1.5), opacity=0.6))
fig.add_trace(go.Scatter(x=t_light, y=-t_light, name="Light (x=-ct)", 
                         line=dict(color="gray", dash="dash", width=1.5), opacity=0.6))

# 8. Dynamic Elements: K' Axes (Moving Frame)
# x' axis: where ct' = 0 => ct = beta * x
x_vals = np.array([-lim, lim]) * gamma
ct_x = beta * x_vals
fig.add_trace(go.Scatter(x=x_vals, y=ct_x, name="x' Axis", 
                         line=dict(color="green", width=2)))

# ct' axis: where x' = 0 => x = beta * ct
ct_vals = np.array([-lim, lim]) * gamma
x_ct = beta * ct_vals
fig.add_trace(go.Scatter(x=x_ct, y=ct_vals, name="ct' Axis", 
                         line=dict(color="red", width=2)))

# 9. Unit Vectors (Points on the hyperbolas)
unit_t_x = gamma * beta
unit_t_ct = gamma

unit_x_x = gamma
unit_x_ct = gamma * beta

fig.add_trace(go.Scatter(x=[unit_t_x], y=[unit_t_ct], mode='markers+text',
                         marker=dict(color='blue', size=10),
                         text=[f"({unit_t_x:.2f}, {unit_t_ct:.2f})"],
                         textposition="top left",
                         name="Unit vector t' (s^2=1)"))

fig.add_trace(go.Scatter(x=[unit_x_x], y=[unit_x_ct], mode='markers+text',
                         marker=dict(color='green', size=10),
                         text=[f"({unit_x_x:.2f}, {unit_x_ct:.2f})"],
                         textposition="bottom right",
                         name="Unit vector x' (s^2=-1)"))

# 10. Invariant Interval Hyperbolas (s^2 = x^2 - (ct)^2)
# s^2 = 1 (Time-like interval hyperbola)
hyp_t_x = np.sinh(np.linspace(-2, 2, 100))
hyp_t_ct = np.cosh(np.linspace(-2, 2, 100))
fig.add_trace(go.Scatter(x=hyp_t_x, y=hyp_t_ct, mode='lines', 
                         line=dict(color='rgba(100, 150, 255, 0.4)', width=1), showlegend=False))

# s^2 = -1 (Space-like interval hyperbola)
hyp_x_x = np.cosh(np.linspace(-2, 2, 100))
hyp_x_ct = np.sinh(np.linspace(-2, 2, 100))
fig.add_trace(go.Scatter(x=hyp_x_x, y=hyp_x_ct, mode='lines', 
                         line=dict(color='rgba(100, 255, 100, 0.4)', width=1), showlegend=False))

# 11. Layout Styling and Constraints
fig.update_layout(
    xaxis=dict(title="Space (x)", range=[-lim, lim], gridcolor="#e0e0e0", zeroline=True, zerolinecolor="black"),
    yaxis=dict(title="Time (ct)", range=[-lim, lim], gridcolor="#e0e0e0", zeroline=True, zerolinecolor="black", scaleanchor="x", scaleratio=1),
    height=800,
    template="plotly_white",
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.8)"),
    margin=dict(l=20, r=20, t=40, b=20)
)

# 12. Render the Plot (config added for slight performance optimization)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# 13. Mathematical Background Section
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
    st.markdown("The unit vectors in the moving frame $K'$ have the following coordinates in the rest frame $K$:")
    st.latex(r"\hat{t}' = (\gamma\beta, \gamma) \quad \text{and} \quad \hat{x}' = (\gamma, \gamma\beta)")