"""
Transparency Panel — Compact Version with visual scorecard.
"""

import streamlit as st


def render_transparency_panel():
    """Render transparency with visual scorecard."""
    
    st.header("Transparency & Data Usage")
    
    # ========================================================================
    # DATA SOURCES TABLE
    # ========================================================================
    st.subheader("Data Sources")
    
    st.table({
        "Component": ["Physiology Model", "Training Labels", "Noise Stats (V2)", "Validation"],
        "Type": ["Synthetic (Windkessel)", "Synthetic (simulator)", "Real (Kaggle BP)", "Synthetic + noise"],
        "Purpose": ["Generate responses", "Train ML surrogate", "Ground noise model", "Test robustness"]
    })
    
    # ========================================================================
    # KAGGLE USAGE
    # ========================================================================
    with st.expander("Kaggle Data Usage Details"):
        col1, col2 = st.columns(2)
        with col1:
            st.success(
                "**What we USE:**\n"
                "- BP distributions (mean, std)\n"
                "- Noise parameters (5/3 mmHg)\n"
                "- Distribution shift validation"
            )
        with col2:
            st.warning(
                "**What we DON'T use:**\n"
                "- NOT for model training\n"
                "- NOT for drug effects\n"
                "- NOT for clinical claims"
            )
    
    # ========================================================================
    # READINESS SCORECARD
    # ========================================================================
    st.markdown("---")
    st.subheader("Readiness Scorecard")
    
    dimensions = [
        ("Architecture", 0.9, "Sound, modular, extensible"),
        ("Methodology", 0.85, "Physiology-inspired + ML + XAI"),
        ("Safety Mechanisms", 0.7, "Uncertainty + OOD detection"),
        ("Data Quality", 0.4, "Synthetic only (no real patients)"),
        ("Clinical Validation", 0.05, "Not validated with clinicians"),
        ("Regulatory", 0.0, "No FDA/CE certification"),
    ]
    
    for name, score, desc in dimensions:
        col_name, col_bar, col_pct = st.columns([2, 4, 1])
        with col_name:
            st.markdown(f"**{name}**")
        with col_bar:
            st.progress(score)
        with col_pct:
            st.markdown(f"**{score*100:.0f}%**")
        st.caption(f"  {desc}")
    
    overall = sum(s for _, s, _ in dimensions) / len(dimensions)
    st.metric("Overall Readiness", f"{overall*100:.0f}%", 
              delta="Research prototype" if overall < 0.6 else "Partial readiness")
    
    # ========================================================================
    # PATH TO DEPLOYMENT
    # ========================================================================
    st.markdown("---")
    with st.expander("Path to Real-World Deployment"):
        steps_data = [
            ("1. Data Collection", "500-1000 real patient observations + IRB approval"),
            ("2. Model Adaptation", "Retrain/fine-tune on real data + calibration"),
            ("3. Clinical Validation", "Domain expert review + workflow testing"),
            ("4. Prospective Trial", "Test predictions + monitor adverse events"),
            ("5. Regulatory", "FDA/CE certification (if applicable)"),
        ]
        for step, desc in steps_data:
            st.markdown(f"**{step}**: {desc}")
        st.caption("**Timeline**: 12-24 months minimum")
