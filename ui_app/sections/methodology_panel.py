"""
Methodology Panel for Digital Twin UI

Explains the workflow and ML role clearly.
"""

import streamlit as st


def render_methodology_panel():
    """Render methodology explanation panel."""
    
    st.header("🔬 Methodology")
    
    st.markdown("""
    ### System Architecture
    
    This digital twin follows a **physiology-inspired, data-driven approach**:
    """)
    
    # Pipeline diagram (text-based)
    st.code("""
    1. Physiology-Inspired Simulator (Windkessel)
       ↓
    2. Synthetic Patient Generation
       ↓
    3. Controlled Intervention Mapping
       ↓
    4. Synthetic Dataset Creation (1000 samples)
       ↓
    5. ML Surrogate Digital Twin (Gradient Boosting)
       ↓
    6. Explainability Layer (SHAP)
       ↓
    7. Uncertainty Quantification (V2)
       ↓
    8. What-If Scenario Exploration
    """, language="text")
    
    # Key insight
    st.info(
        "**Key Insight**: The ML model learns a surrogate mapping that approximates "
        "simulator behavior under partial observability and noise. "
        "The simulator is a *teacher*, not the final model."
    )
    
    # Detailed explanation
    st.subheader("Component Roles")
    
    with st.expander("🧬 Physiology-Inspired Simulator"):
        st.markdown("""
        **Windkessel Model**: Canonical lumped-parameter cardiovascular model
        
        - Equation: `dP/dt = (Q(t) - P/R) / C`
        - Parameters: Resistance (R), Compliance (C), Cardiac Output (Q)
        - Purpose: Generate controlled, physiologically-plausible responses
        
        **Note**: This is a simplified abstraction, not a clinical simulator.
        """)
    
    with st.expander("🤖 ML Surrogate Digital Twin"):
        st.markdown("""
        **Gradient Boosting Regressor** (Multi-output)
        
        - **Inputs**: Age, baseline BP, heart rate, risk group, intervention class, dosage
        - **Outputs**: Δ SBP, Δ DBP
        - **Training**: 1000 synthetic samples from Windkessel simulator
        - **Purpose**: Learn fast approximation of simulator behavior
        
        **What the ML learns**: A surrogate mapping that approximates simulator behavior 
        under partial observability and noise, not real patient outcomes.
        """)
    
    with st.expander("🔍 Explainability (SHAP)"):
        st.markdown("""
        **SHAP (SHapley Additive exPlanations)**
        
        - Global feature importance
        - Patient-specific local explanations
        - Dose-response analysis
        
        **Purpose**: Understand which features drive simulated responses.
        """)
    
    with st.expander("🎲 Uncertainty Quantification (V2)"):
        st.markdown("""
        **Bootstrap-Based Uncertainty Estimation**
        
        - Method: Perturb inputs with small noise, measure prediction variance
        - Output: Mean ± uncertainty with 95% confidence intervals
        - Confidence levels: High / Medium / Low
        
        **Purpose**: Quantify prediction reliability for safe decision support.
        
        **Why this matters**: Uncertainty reflects expected variability under noisy conditions.
        """)
    
    # What this is NOT
    st.subheader("What This Model CANNOT Do")
    
    st.error("""
    This model **cannot**:
    
    - ❌ Predict real patient outcomes
    - ❌ Replace clinical judgment
    - ❌ Guarantee accuracy under unseen conditions
    - ❌ Model long-term temporal effects
    - ❌ Infer actual drug pharmacokinetics
    """)
    
    # ML vs Simulator comparison
    st.subheader("ML vs Simulator Comparison")
    
    st.markdown("""
    **Why use ML instead of just the simulator?**
    
    | Aspect | Simulator | ML Surrogate |
    |--------|-----------|--------------|
    | **Speed** | Slow (ODE solving) | Fast (milliseconds) |
    | **Scalability** | Poor (one-at-a-time) | Excellent (batch) |
    | **Explainability** | Physics-based | Data-driven (SHAP) |
    | **Uncertainty** | Not quantified | Quantified (V2) |
    | **Use Case** | Teaching | What-if exploration |
    
    **Conclusion**: ML provides a fast, scalable, explainable approximation suitable for 
    interactive what-if analysis, not a replacement for the physics.
    """)
