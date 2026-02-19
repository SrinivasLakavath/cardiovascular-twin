"""
Input Panel for Digital Twin UI

Collects synthetic patient profile parameters for simulation.
"""

import streamlit as st


def render_input_panel():
    """
    Render input panel for patient profile.
    Controls only - no documentation.
    
    Returns
    -------
    dict
        Patient profile parameters
    """
    st.sidebar.header("📋 Patient Profile")
    
    # Age
    age = st.sidebar.slider(
        "Age (years)",
        min_value=18,
        max_value=100,
        value=55
    )
    
    # Baseline SBP
    baseline_sbp = st.sidebar.slider(
        "Baseline SBP (mmHg)",
        min_value=80,
        max_value=200,
        value=130
    )
    
    # Baseline DBP
    baseline_dbp = st.sidebar.slider(
        "Baseline DBP (mmHg)",
        min_value=50,
        max_value=120,
        value=85
    )
    
    # Heart Rate
    heart_rate = st.sidebar.slider(
        "Heart Rate (bpm)",
        min_value=40,
        max_value=150,
        value=70
    )
    
    # Risk Group
    risk_group = st.sidebar.selectbox(
        "Risk Group",
        options=["low", "medium", "high"],
        index=1
    )
    
    # Drug Class
    drug_class = st.sidebar.selectbox(
        "Intervention Class",
        options=["beta_blocker", "vasodilator", "stimulant", "volume_expander"],
        index=0
    )
    
    # Dosage
    dosage = st.sidebar.slider(
        "Dosage (abstract units)",
        min_value=0.0,
        max_value=3.0,
        value=1.0,
        step=0.1
    )
    
    # Return as dictionary
    patient_profile = {
        'age': age,
        'baseline_sbp': baseline_sbp,
        'baseline_dbp': baseline_dbp,
        'heart_rate': heart_rate,
        'risk_group': risk_group,
        'drug_class': drug_class,
        'dosage': dosage
    }
    
    return patient_profile
