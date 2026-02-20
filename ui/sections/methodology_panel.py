"""
Methodology Panel for Digital Twin UI — Premium Version

Visual pipeline with SVG icons + interactive Windkessel waveform.
"""

import streamlit as st
import sys
import os
import numpy as np
import plotly.graph_objects as go

# Ensure project root on path for icon imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from assets.icons import icon


def render_methodology_panel():
    """Render methodology with visual pipeline and waveform."""
    
    st.header("Methodology")
    
    st.markdown("""
    This digital twin follows a **physiology-inspired, data-driven approach**.
    The pipeline below shows how raw physics becomes an interactive AI tool.
    """)
    
    # ========================================================================
    # VISUAL PIPELINE with SVG icons
    # ========================================================================
    steps = [
        ("dna", "Physiology Core", "Windkessel ODE Model", "#3182ce"),
        ("user", "Patient Generation", "Synthetic profiles (N=1000)", "#2b6cb0"),
        ("pill", "Intervention Mapping", "Drug \u2192 Parameter Changes", "#2c5282"),
        ("layers", "Dataset Creation", "Tabular: X \u2192 \u0394BP", "#2a4365"),
        ("brain", "ML Surrogate", "Gradient Boosting Twin", "#38a169"),
        ("search", "Explainability", "SHAP Feature Importance", "#2f855a"),
        ("activity", "Uncertainty (V2)", "Bootstrap Estimation", "#276749"),
        ("target", "What-If Analysis", "Interactive Scenarios", "#22543d"),
    ]
    
    # Render as styled step cards with SVG icons
    for i, (icon_name, title, desc, color) in enumerate(steps):
        step_icon = icon(icon_name, size=22, color=color)
        cols = st.columns([0.5, 5, 0.5])
        with cols[1]:
            st.markdown(f"""
            <div style="display:flex; align-items:center; padding:10px 16px; 
                        background:linear-gradient(90deg, {color}15, {color}05); 
                        border-left:4px solid {color}; border-radius:8px; margin:3px 0;">
                {step_icon}
                <div style="margin-left:6px;">
                    <span style="font-weight:700; color:{color}; font-size:0.95rem;">
                        Step {i+1}: {title}
                    </span><br>
                    <span style="color:#4a5568; font-size:0.85rem;">{desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        if i < len(steps) - 1:
            cols2 = st.columns([1, 5, 1])
            with cols2[1]:
                st.markdown("<div style='text-align:center; color:#a0aec0; font-size:1.2rem;'>\u2193</div>",
                            unsafe_allow_html=True)
    
    # ========================================================================
    # WINDKESSEL WAVEFORM
    # ========================================================================
    st.markdown("---")
    st.subheader("Windkessel Pressure Waveform")
    st.caption("Live output from the ODE solver \u2014 this is what the physics engine produces.")
    
    t, P = _generate_waveform()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=P,
        mode='lines',
        line=dict(color='#e53e3e', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(229, 62, 62, 0.08)',
        name='Arterial Pressure'
    ))
    
    sbp = max(P)
    dbp = min(P[len(P)//3:])
    
    fig.add_hline(y=sbp, line_dash="dash", line_color="#e53e3e", opacity=0.5,
                  annotation_text=f"SBP \u2248 {sbp:.0f}", annotation_position="top left")
    fig.add_hline(y=dbp, line_dash="dash", line_color="#3182ce", opacity=0.5,
                  annotation_text=f"DBP \u2248 {dbp:.0f}", annotation_position="bottom left")
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Time (s)', gridcolor='#edf2f7'),
        yaxis=dict(title='Pressure (mmHg)', gridcolor='#edf2f7'),
        showlegend=False,
        font=dict(family='Arial', size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True, key="waveform_chart")
    
    # ========================================================================
    # COMPONENT DETAILS
    # ========================================================================
    st.markdown("---")
    st.subheader("Component Details")
    
    with st.expander("Windkessel Model"):
        st.markdown("""
        **Governing ODE**: `dP/dt = (Q(t) - P/R) / C`
        
        | Parameter | Symbol | Calibrated Value | Meaning |
        |:---|:---|:---|:---|
        | Resistance | R | 18.0 | Peripheral vascular resistance |
        | Compliance | C | 1.0 | Arterial wall elasticity |
        | Cardiac Output | Q | 5.0 L/min | Blood flow from heart |
        
        **Note**: Simplified abstraction, not a clinical simulator.
        """)
    
    with st.expander("ML Surrogate (Gradient Boosting)"):
        st.markdown("""
        | Aspect | Detail |
        |:---|:---|
        | **Inputs** | Age, Baseline BP, HR, Risk Group, Drug Class, Dosage |
        | **Outputs** | \u0394 SBP, \u0394 DBP |
        | **Training** | 1000 synthetic samples |
        | **Purpose** | Fast approximation for interactive what-if analysis |
        """)
    
    with st.expander("Why ML instead of just the Simulator?"):
        st.markdown("""
        | Aspect | Simulator | ML Surrogate |
        |:---|:---|:---|
        | **Speed** | Slow (ODE solving) | Fast (ms) |
        | **Scalability** | One-at-a-time | Batch |
        | **Explainability** | Physics-based | SHAP |
        | **Uncertainty** | Not quantified | Quantified (V2) |
        """)
    
    # Limitations
    st.markdown("---")
    st.error("""
    **Limitations**: Cannot predict real patient outcomes \u2022 Cannot replace clinical judgment \u2022 
    Cannot model long-term effects \u2022 Cannot infer actual pharmacokinetics
    """)


def _generate_waveform():
    """Generate a sample Windkessel pressure waveform."""
    R, C, Q_mean = 18.0, 1.0, 5.0
    dt = 0.001
    T = 3.0
    t = np.arange(0, T, dt)
    P = np.zeros_like(t)
    P[0] = 80
    
    for i in range(1, len(t)):
        heart_rate = 72
        period = 60.0 / heart_rate
        phase = (t[i] % period) / period
        
        if phase < 0.35:
            Q = Q_mean * (1 + 2.0 * np.sin(np.pi * phase / 0.35))
        else:
            Q = Q_mean * 0.2
        
        dPdt = (Q - P[i-1] / R) / C
        P[i] = P[i-1] + dPdt * dt
    
    return t, P
