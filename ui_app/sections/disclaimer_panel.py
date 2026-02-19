"""
Disclaimer Panel for Digital Twin UI

Provides prominent disclaimers and accuracy framing.
CRITICAL: This is the most important safety component.
"""

import streamlit as st


def render_disclaimer_panel():
    """Render disclaimer and accuracy framing panel."""
    
    st.header("⚠️ Important Disclaimers")
    
    # Primary disclaimer (prominent)
    st.error("""
    ### 🚨 RESEARCH SIMULATION ONLY
    
    **This system is a research simulation and demonstration prototype.**
    
    - ❌ **NOT** for clinical use
    - ❌ **NOT** clinically accurate
    - ❌ **NOT** validated on real patients
    - ❌ **NOT** regulatory-compliant
    - ❌ **NO** medical decisions should be made based on these outputs
    
    **All outputs are simulated responses under controlled assumptions, not real patient predictions.**
    """)
    
    # Scope boundary (repeated for emphasis)
    st.warning("""
    ### 📏 Scope Boundary
    
    This system models *relative cardiovascular response trends* under controlled assumptions.
    
    It does **not** estimate absolute blood pressure values for real patients.
    """)
    
    # Why no accuracy percentages
    st.subheader("Why We Don't Show Accuracy Percentages")
    
    st.info("""
    **Reason**: "Accuracy" implies comparison to ground truth. We don't have real patient outcomes.
    
    **What we show instead**:
    
    1. **Model Fidelity** (V1): How well ML approximates the simulator
       - MAE < 0.01 mmHg relative to simulator
       - This is NOT real-world accuracy
    
    2. **Robustness** (V2): How well the model handles realistic noise
       - MAE ~0.5 mmHg under noise-grounded conditions
       - This demonstrates resilience, not clinical accuracy
    
    3. **Uncertainty** (V2): Quantified prediction variability
       - ±0.3-0.5 mmHg typical uncertainty
       - Reflects expected variability, not error bounds
    
    **Why this is more honest**: We measure what we can validate (simulator fidelity, robustness), 
    not what we cannot (real-world accuracy).
    """)
    
    # Why uncertainty is more meaningful
    st.subheader("Why Uncertainty is More Meaningful Than Accuracy")
    
    st.success("""
    **Uncertainty quantification is the responsible approach**:
    
    1. **Honest About Limits**: Shows what the model doesn't know
    2. **Enables Safe Decisions**: High uncertainty → require review
    3. **Prevents Overconfidence**: No false precision
    4. **Clinically Relevant**: Matches how clinicians think
    
    **Example**:
    - ❌ "95% accurate" → Misleading (accurate at what?)
    - ✅ "Δ SBP = -2.6 ± 0.4 mmHg, confidence: HIGH" → Informative
    
    **Conclusion**: Uncertainty is a feature, not a weakness.
    """)
    
    # With real data, what would change
    st.subheader("With High-Quality Real-World Data...")
    
    st.markdown("""
    **The architecture could be calibrated to improve relevance**:
    
    ### Current State (Synthetic)
    - Training: 1000 synthetic samples from Windkessel
    - Validation: Physiological sanity checks + noise robustness
    - Performance: Excellent fidelity to simulator, unknown real-world performance
    
    ### With Real Data (Future)
    - Training: 500-1000 real patient observations with interventions
    - Validation: Prospective clinical trial
    - Performance: Measured against real outcomes
    - Expected MAE: 3-7 mmHg (comparable to clinical variability)
    
    ### What Would Improve
    - ✅ Real-world generalization
    - ✅ Clinical relevance
    - ✅ Deployment readiness
    - ✅ Regulatory pathway
    
    ### What Would NOT Change
    - Architecture (already designed for real-world adaptation)
    - Methodology (physiology-inspired + ML + XAI)
    - Safety mechanisms (uncertainty, OOD detection)
    
    **Timeline**: 12-24 months for full validation
    """)
    
    # Final statement
    st.info("""
    ### 🎯 What This Project Demonstrates
    
    **This is a methodological demonstration**, not a clinical tool.
    
    **It proves**:
    - ✅ Physiology-inspired modeling can guide ML
    - ✅ Explainability can be integrated from the start
    - ✅ Uncertainty quantification enables safe adaptation
    - ✅ The architecture is sound and defensible
    
    **It does NOT prove**:
    - ❌ Clinical accuracy
    - ❌ Real-world generalization
    - ❌ Deployment readiness
    
    **Use case**: Research, education, and methodology validation.
    """)
    
    # Contact/feedback
    st.caption("""
    ---
    **Questions or concerns?** This is an academic research project. 
    All limitations are documented transparently.
    """)
