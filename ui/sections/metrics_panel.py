"""
Metrics Panel for Digital Twin UI — Premium Version

Displays model performance with real charts instead of text walls.
"""

import streamlit as st
import plotly.graph_objects as go


def render_metrics_panel(version="V1"):
    """Render performance metrics panel with charts."""
    st.header("Model Performance")
    
    if version == "V1":
        render_v1_metrics()
    else:
        render_v2_metrics()
    
    # Always show comparison chart
    st.markdown("---")
    render_comparison_chart()


def render_v1_metrics():
    """V1 metrics with compact layout."""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Training Data", value="Synthetic",
                  help="Generated from Windkessel simulator")
    with col2:
        st.metric(label="Model Fidelity", value="MAE < 0.01",
                  help="Error relative to simulator output (mmHg)")
    with col3:
        st.metric(label="Purpose", value="Validation",
                  help="Proves algorithmic correctness")
    
    col_good, col_bad = st.columns(2)
    
    with col_good:
        st.success(
            "**V1 Demonstrates:**\n"
            "- ML surrogate learns simulator\n"
            "- Algorithm correctness\n"
            "- XAI framework works\n"
            "- Sound methodology"
        )
    with col_bad:
        st.warning(
            "**V1 Does NOT Prove:**\n"
            "- Real-world accuracy\n"
            "- Clinical validity\n"
            "- Patient generalization\n"
            "- Deployment readiness"
        )


def render_v2_metrics():
    """V2 metrics with compact layout."""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Training Data", value="Synthetic",
                  help="Same as V1 (not retrained)")
    with col2:
        st.metric(label="Noise Source", value="Kaggle BP",
                  help="Real BP statistics for noise modeling")
    with col3:
        st.metric(label="Robustness", value="MAE ~0.5",
                  help="Performance under realistic noise (mmHg)")
    
    st.info(
        "**Performance Degradation** in V2 is *expected and desirable* — it reflects "
        "exposure to realistic noise and distribution shift. This demonstrates robustness, not weakness."
    )
    
    col_good, col_bad = st.columns(2)
    
    with col_good:
        st.success(
            "**V2 Adds:**\n"
            "- Real-world noise grounding\n"
            "- Uncertainty quantification\n"
            "- Domain shift evaluation\n"
            "- Realistic expectations"
        )
    with col_bad:
        st.warning(
            "**Critical Note:** Both V1 and V2 use "
            "synthetic training data. Real deployment needs "
            "real patient data + regulatory approval."
        )


def render_comparison_chart():
    """Interactive V1 vs V2 comparison chart."""
    
    st.subheader("V1 vs V2 Performance Comparison")
    
    categories = ['Fidelity<br>(MAE)', 'Noise<br>Robustness', 'Uncertainty<br>Quantification', 
                  'Speed', 'Explainability']
    
    # Scores out of 5 (conceptual comparison)
    v1_scores = [5, 1, 0.5, 5, 4.5]
    v2_scores = [4, 4, 4.5, 4.5, 4.5]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=v1_scores,
        theta=categories,
        fill='toself',
        name='V1 (Synthetic)',
        line_color='#3182ce',
        fillcolor='rgba(49, 130, 206, 0.15)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=v2_scores,
        theta=categories,
        fill='toself',
        name='V2 (Real-World Grounded)',
        line_color='#38a169',
        fillcolor='rgba(56, 161, 105, 0.15)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5], gridcolor='#edf2f7'),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        height=400,
        margin=dict(l=60, r=60, t=40, b=60),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True, key="v1_v2_radar")
    
    # Compact comparison table
    with st.expander("Detailed Comparison Table"):
        st.table({
            "Metric": ["Data Source", "Noise Model", "MAE (mmHg)", "Uncertainty", "Purpose"],
            "V1": ["Synthetic", "None (clean)", "< 0.01", "Not quantified", "Method validation"],
            "V2": ["Synthetic + Kaggle", "Realistic (5/3 mmHg)", "~0.5", "\u00b1 0.3-0.5", "Robustness + realism"]
        })
