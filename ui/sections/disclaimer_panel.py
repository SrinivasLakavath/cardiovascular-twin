"""
Disclaimer Panel — Compact, clean, no emojis.
"""

import streamlit as st


def render_disclaimer_panel():
    """Render compact disclaimers."""
    
    st.header("Important Disclaimers")
    
    # Primary Warning
    st.error("""
    ### Research Simulation Only
    
    This is a **research prototype** \u2014 NOT a clinical tool.
    
    Not for clinical use  \u2022  Not validated on patients  \u2022  Not regulatory-compliant
    
    All outputs are simulated responses under controlled assumptions.
    """)
    
    # What we measure
    st.subheader("Why We Don't Show \"Accuracy %\"")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(
            "**What we CAN measure:**\n"
            "- Model Fidelity (V1): MAE < 0.01\n"
            "- Robustness (V2): MAE ~0.5\n"
            "- Uncertainty: \u00b1 0.3\u20130.5 mmHg"
        )
    with col2:
        st.warning(
            "**What we CANNOT claim:**\n"
            "- Real-world accuracy\n"
            "- Clinical validity\n"
            "- Deployment readiness"
        )
    
    st.caption(
        "\"Accuracy\" implies comparison to ground truth. We measure *simulator fidelity* "
        "and *noise robustness*, not clinical accuracy."
    )
    
    # What this proves
    st.markdown("---")
    
    col_yes, col_no = st.columns(2)
    
    with col_yes:
        st.success(
            "**This project demonstrates:**\n"
            "- Physiology-inspired modeling\n"
            "- Integrated explainability\n"
            "- Uncertainty quantification\n"
            "- Sound architecture"
        )
    
    with col_no:
        st.error(
            "**This project does NOT prove:**\n"
            "- Clinical accuracy\n"
            "- Real-world generalization\n"
            "- Deployment readiness\n"
            "- Regulatory compliance"
        )
    
    st.caption("**Use case**: Research, education, and methodology validation.")
