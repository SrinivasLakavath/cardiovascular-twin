"""
Input Panel for Digital Twin UI

Collects synthetic patient profile parameters for simulation.
"""

import streamlit as st


def render_input_panel():
    """
    Render input panel for patient profile.
    
    Returns
    -------
    dict
        Patient profile parameters
    """
    st.sidebar.header("Patient Profile")
    
    # Age
    age = st.sidebar.slider(
        "Age (years)",
        min_value=18, max_value=100, value=55
    )
    
    # Baseline SBP
    baseline_sbp = st.sidebar.slider(
        "Baseline SBP (mmHg)",
        min_value=80, max_value=200, value=130
    )
    
    # Baseline DBP
    baseline_dbp = st.sidebar.slider(
        "Baseline DBP (mmHg)",
        min_value=50, max_value=120, value=85
    )
    
    # Heart Rate
    heart_rate = st.sidebar.slider(
        "Heart Rate (bpm)",
        min_value=40, max_value=150, value=70
    )
    
    # Risk Group
    risk_group = st.sidebar.selectbox(
        "Risk Group",
        options=["low", "medium", "high"],
        index=1
    )
    
    # Drug Selection
    drug_mode = st.sidebar.radio(
        "Intervention Mode",
        options=["Standard Drug", "Custom / Investigational"],
        index=0
    )
    
    if drug_mode == "Standard Drug":
        drug_name = st.sidebar.selectbox(
            "Drug Selection",
            options=[
                "Atenolol (Beta Blocker)",
                "Bisoprolol (Beta Blocker)", 
                "Lisinopril (Vasodilator)",
                "Amlodipine (Vasodilator)",
                "Adrenaline (Stimulant)",
                "Saline IV (Volume Expander)",
                "None (Baseline)"
            ],
            index=0
        )
        
        # Map Drug Name to Class
        if "Beta Blocker" in drug_name:
            drug_class = "beta_blocker"
        elif "Vasodilator" in drug_name:
            drug_class = "vasodilator"
        elif "Stimulant" in drug_name:
            drug_class = "stimulant"
        elif "Volume Expander" in drug_name:
            drug_class = "volume_expander"
        else:
            drug_class = "none"

        # Standard Dosage
        dosage = st.sidebar.slider(
            "Dosage Intensity (Multiplier)",
            min_value=0.0, max_value=3.0, value=1.0, step=0.1,
            help="1.0 = Standard Therapeutic Dose"
        )
        
        custom_params = None

    else:
        # Custom / Investigational Mode
        st.sidebar.markdown("---")
        st.sidebar.subheader("Custom Intervention")
        st.sidebar.info("Define direct physiological effects.")
        
        drug_class = "custom"
        dosage = 1.0
        
        r_change = st.sidebar.slider(
            "\u0394 Peripheral Resistance (%)",
            min_value=-50, max_value=50, value=0, step=5
        ) / 100.0
        
        c_change = st.sidebar.slider(
            "\u0394 Arterial Compliance (%)",
            min_value=-50, max_value=50, value=0, step=5
        ) / 100.0
        
        q_change = st.sidebar.slider(
            "\u0394 Cardiac Output (%)",
            min_value=-50, max_value=50, value=0, step=5
        ) / 100.0
        
        custom_params = {
            'r_change': r_change,
            'c_change': c_change,
            'q_change': q_change
        }
    
    patient_profile = {
        'age': age,
        'baseline_sbp': baseline_sbp,
        'baseline_dbp': baseline_dbp,
        'heart_rate': heart_rate,
        'risk_group': risk_group,
        'drug_class': drug_class,
        'dosage': dosage,
        'custom_params': custom_params
    }
    
    return patient_profile
