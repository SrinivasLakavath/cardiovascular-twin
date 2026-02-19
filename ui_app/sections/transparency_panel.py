"""
Transparency Panel for Digital Twin UI

Explains data usage and ethical considerations.
"""

import streamlit as st


def render_transparency_panel():
    """Render transparency and data usage panel."""
    
    st.header("🔍 Transparency & Data Usage")
    
    st.markdown("""
    This section provides complete transparency about data sources, usage, and limitations.
    """)
    
    # Data usage table
    st.subheader("Data Sources & Usage")
    
    data_table = {
        "Component": [
            "Physiology Model",
            "Training Labels",
            "Noise Statistics",
            "Validation",
            "Deployment Readiness"
        ],
        "Data Type": [
            "Synthetic (Windkessel equations)",
            "Synthetic (simulator outputs)",
            "Real (Kaggle BP dataset)",
            "Synthetic + noise-grounded",
            "Not claimed"
        ],
        "Purpose": [
            "Generate controlled responses",
            "Train ML surrogate",
            "Ground noise model in reality",
            "Test robustness",
            "N/A - research prototype"
        ]
    }
    
    st.table(data_table)
    
    # Kaggle data usage
    st.subheader("Kaggle Data Usage (Version 2)")
    
    st.info("""
    **Dataset**: `ahmedwadood/blood-pressure-dataset` (1000+ real BP measurements)
    
    **What we use it for**:
    - ✅ Extract realistic BP distributions (mean, std, percentiles)
    - ✅ Estimate measurement noise parameters (5.0/3.0 mmHg)
    - ✅ Ground synthetic noise model in real statistics
    - ✅ Validate distribution shift robustness
    
    **What we do NOT use it for**:
    - ❌ Training the ML model (model uses synthetic data only)
    - ❌ Inferring drug effects (dataset lacks intervention data)
    - ❌ Making clinical predictions
    - ❌ Claiming real-world accuracy
    """)
    
    # Ethical transparency
    st.subheader("Ethical Considerations")
    
    st.success("""
    **Honest Limitations**:
    
    1. **No Real Patient Data**: All training data is synthetic
    2. **No Clinical Validation**: Not tested with clinicians or in clinical trials
    3. **No Regulatory Approval**: Not FDA/CE certified
    4. **No Deployment Claims**: This is a research prototype
    5. **Abstract Interventions**: Not real drugs with pharmacokinetics
    
    **Why This Matters**: Transparency builds trust and prevents misuse.
    """)
    
    # Real-world readiness
    st.subheader("Real-World Readiness ≠ Deployment")
    
    st.warning("""
    **Important Distinction**:
    
    "Real-world readiness indicates *architectural adaptability*, not deployment suitability."
    
    **What this means**:
    - ✅ The architecture *could* be adapted with real data
    - ✅ The methodology is sound and defensible
    - ✅ Safety mechanisms (uncertainty, OOD detection) are in place
    - ❌ The system is NOT ready for clinical deployment
    - ❌ Significant validation work remains (12-24 months)
    """)
    
    # Path to deployment
    st.subheader("Path to Real-World Deployment")
    
    st.markdown("""
    **Required Steps** (not yet completed):
    
    1. **Data Collection**
       - Collect 500-1000 real patient observations
       - Include pre/post-intervention BP measurements
       - Obtain IRB approval
    
    2. **Model Adaptation**
       - Retrain or fine-tune on real data
       - Validate calibration accuracy
       - Test generalization
    
    3. **Clinical Validation**
       - Work with domain experts
       - Validate explanations
       - Establish clinical workflows
    
    4. **Prospective Trial**
       - Test predictions prospectively
       - Monitor adverse events
       - Continuous performance tracking
    
    5. **Regulatory Approval**
       - Pursue FDA/CE certification (if applicable)
       - Establish safety monitoring
       - Implement clinical review protocol
    
    **Timeline**: 12-24 months minimum
    """)
    
    # Current status
    st.info("""
    **Current Status**: Research prototype demonstrating methodology and architectural soundness.
    
    **Deployment Readiness Score**: 32/50 (64%) - Partial readiness
    
    See `real_world/readiness_scorecard.py` for detailed assessment.
    """)
