"""
XAI Engine — Real-Time Explainability for the Digital Twin UI

Provides per-patient SHAP explanations using TreeExplainer.
Designed to be called from the Streamlit UI for live explanations.

Key features:
- Uses shap.TreeExplainer (fast, exact for tree-based models)
- Returns structured results suitable for Plotly visualization
- Generates natural language interpretation from top SHAP drivers
- Caches model and background data for fast repeated calls
"""

import os
import sys
import numpy as np
import joblib

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


# Human-readable feature names
FEATURE_DISPLAY_NAMES = {
    'age': 'Age',
    'baseline_sbp': 'Baseline SBP',
    'baseline_dbp': 'Baseline DBP',
    'heart_rate': 'Heart Rate',
    'risk_group_encoded': 'Risk Group',
    'drug_class_encoded': 'Drug Class',
    'dosage': 'Dosage'
}

# Feature interpretation templates (what does high/low mean?)
FEATURE_INTERPRETATIONS = {
    'age': {
        'high': 'older patients tend to show altered cardiovascular sensitivity',
        'low': 'younger patients typically show more predictable responses'
    },
    'baseline_sbp': {
        'high': 'higher starting blood pressure amplifies the modeled drug effect',
        'low': 'lower starting blood pressure reduces the modeled magnitude of change'
    },
    'baseline_dbp': {
        'high': 'elevated diastolic pressure indicates increased vascular resistance in the model',
        'low': 'lower diastolic pressure suggests reduced vascular load'
    },
    'heart_rate': {
        'high': 'elevated heart rate increases cardiac output in the model',
        'low': 'lower heart rate suggests a calmer cardiovascular baseline'
    },
    'risk_group_encoded': {
        'high': 'higher risk profile amplifies modeled sensitivity to interventions',
        'low': 'lower risk profile suggests more stable response characteristics'
    },
    'drug_class_encoded': {
        'high': 'the selected drug class has a strong modeled effect on blood pressure',
        'low': 'the drug mechanism has a modest modeled impact on blood pressure'
    },
    'dosage': {
        'high': 'higher dosage directly increases the modeled intervention strength',
        'low': 'lower dosage produces a milder modeled effect'
    }
}

# Drug class readable names
DRUG_CLASS_NAMES = {
    'beta_blocker': 'Beta Blocker',
    'vasodilator': 'Vasodilator',
    'stimulant': 'Stimulant',
    'volume_expander': 'Volume Expander',
    'none': 'No Intervention',
    'custom': 'Custom Intervention'
}


def load_xai_resources():
    """
    Load model, encoders, and background data for SHAP.
    
    Returns
    -------
    dict with keys: model, le_drug, le_risk, feature_names, background_data
    """
    model_path = os.path.join(SRC_DIR, 'twin_model', 'weights', 'surrogate_twin.pkl')
    encoders_path = os.path.join(SRC_DIR, 'twin_model', 'weights', 'encoders.pkl')
    feature_names_path = os.path.join(SRC_DIR, 'twin_model', 'weights', 'feature_names.pkl')
    dataset_path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'synthetic_dataset.csv')
    
    model = joblib.load(model_path)
    encoders = joblib.load(encoders_path)
    le_drug, le_risk = encoders
    feature_names = joblib.load(feature_names_path)
    
    # Load background data for SHAP (small subset)
    import pandas as pd
    df = pd.read_csv(dataset_path)
    df['drug_class_encoded'] = le_drug.transform(df['drug_class'])
    df['risk_group_encoded'] = le_risk.transform(df['risk_group'])
    
    feature_cols = [
        'age', 'baseline_sbp', 'baseline_dbp', 'heart_rate',
        'risk_group_encoded', 'drug_class_encoded', 'dosage'
    ]
    
    # Use 100 random samples as background
    bg = df[feature_cols].sample(n=min(100, len(df)), random_state=42).values
    
    return {
        'model': model,
        'le_drug': le_drug,
        'le_risk': le_risk,
        'feature_names': feature_names,
        'background_data': bg
    }


def explain_prediction(patient_profile, resources):
    """
    Compute per-patient SHAP explanation for a simulation result.
    
    Parameters
    ----------
    patient_profile : dict
        Patient profile from the UI (age, baseline_sbp, drug_class, etc.)
    resources : dict
        Loaded XAI resources from load_xai_resources()
    
    Returns
    -------
    dict with:
        - shap_values_sbp : array of SHAP values for delta SBP
        - shap_values_dbp : array of SHAP values for delta DBP
        - feature_names : list of display-friendly feature names
        - feature_values : dict mapping feature name to actual value
        - top_drivers : list of (feature_name, shap_value, direction) sorted by |SHAP|
        - interpretation : str — natural language explanation
        - base_value_sbp : float — model's average SBP prediction
        - base_value_dbp : float — model's average DBP prediction
    """
    import shap
    
    model = resources['model']
    le_drug = resources['le_drug']
    le_risk = resources['le_risk']
    background = resources['background_data']
    
    # Skip custom interventions (physics-only, no ML model to explain)
    if patient_profile.get('drug_class') == 'custom':
        return None
    
    # Encode the patient
    drug_encoded = le_drug.transform([patient_profile['drug_class']])[0]
    risk_encoded = le_risk.transform([patient_profile['risk_group']])[0]
    
    patient_features = np.array([[
        patient_profile['age'],
        patient_profile['baseline_sbp'],
        patient_profile['baseline_dbp'],
        patient_profile['heart_rate'],
        risk_encoded,
        drug_encoded,
        patient_profile['dosage']
    ]])
    
    # TreeExplainer — fast and exact for GBM
    # The model is MultiOutputRegressor, so we explain each sub-estimator
    feature_names_internal = [
        'age', 'baseline_sbp', 'baseline_dbp', 'heart_rate',
        'risk_group_encoded', 'drug_class_encoded', 'dosage'
    ]
    display_names = [FEATURE_DISPLAY_NAMES.get(f, f) for f in feature_names_internal]
    
    # Handle both SurrogateTwin wrapper and raw MultiOutputRegressor
    inner_model = model
    if hasattr(model, 'model'):
        inner_model = model.model  # SurrogateTwin wrapper
    
    shap_sbp = _explain_single_output(inner_model.estimators_[0], background, patient_features)
    shap_dbp = _explain_single_output(inner_model.estimators_[1], background, patient_features)
    
    # Build feature values dict for display
    drug_name = DRUG_CLASS_NAMES.get(patient_profile['drug_class'], patient_profile['drug_class'])
    feature_values = {
        'Age': f"{patient_profile['age']} years",
        'Baseline SBP': f"{patient_profile['baseline_sbp']} mmHg",
        'Baseline DBP': f"{patient_profile['baseline_dbp']} mmHg",
        'Heart Rate': f"{patient_profile['heart_rate']} bpm",
        'Risk Group': patient_profile['risk_group'].title(),
        'Drug Class': drug_name,
        'Dosage': f"{patient_profile['dosage']:.1f}x"
    }
    
    # Top drivers (sorted by absolute SHAP for SBP)
    top_drivers = []
    for i, fname in enumerate(feature_names_internal):
        dname = display_names[i]
        sv = shap_sbp[i]
        direction = 'increases' if sv > 0 else 'decreases'
        top_drivers.append((dname, sv, direction, fname))
    
    top_drivers.sort(key=lambda x: abs(x[1]), reverse=True)
    
    # Generate interpretation
    interpretation = _generate_interpretation(
        top_drivers, patient_profile, shap_sbp, feature_names_internal
    )
    
    return {
        'shap_values_sbp': shap_sbp,
        'shap_values_dbp': shap_dbp,
        'feature_names': display_names,
        'feature_values': feature_values,
        'top_drivers': top_drivers,
        'interpretation': interpretation,
        'base_value_sbp': float(np.mean(model.predict(background)[:, 0])),
        'base_value_dbp': float(np.mean(model.predict(background)[:, 1])),
    }


def _explain_single_output(estimator, background, patient_features):
    """Compute SHAP values for a single GBM estimator."""
    import shap
    explainer = shap.TreeExplainer(estimator, data=background)
    shap_values = explainer.shap_values(patient_features)
    return shap_values[0]  # Single patient


def _generate_interpretation(top_drivers, profile, shap_sbp, feature_names):
    """
    Generate natural-language interpretation from SHAP values.
    
    Returns a structured markdown string.
    """
    drug_name = DRUG_CLASS_NAMES.get(profile.get('drug_class', ''), 'Selected Drug')
    total_shap = sum(sv for _, sv, _, _ in top_drivers)
    
    lines = []
    
    # Opening sentence
    if total_shap < 0:
        lines.append(
            f"The model predicts a **blood pressure reduction** "
            f"(net SHAP contribution: {total_shap:+.1f} mmHg)."
        )
    elif total_shap > 0:
        lines.append(
            f"The model predicts a **blood pressure increase** "
            f"(net SHAP contribution: {total_shap:+.1f} mmHg)."
        )
    else:
        lines.append("The model predicts **minimal change** in blood pressure.")
    
    lines.append("")
    lines.append("**Key drivers of this result:**")
    lines.append("")
    
    # Top 3 drivers
    for rank, (dname, sv, direction, fname) in enumerate(top_drivers[:3], 1):
        abs_sv = abs(sv)
        
        # Context-specific explanation
        interp_key = 'high' if sv > 0 else 'low'
        context = FEATURE_INTERPRETATIONS.get(fname, {}).get(interp_key, '')
        
        # Value display
        if fname == 'drug_class_encoded':
            val_str = drug_name
        elif fname == 'risk_group_encoded':
            val_str = profile.get('risk_group', 'unknown').title()
        elif fname == 'dosage':
            val_str = f"{profile.get('dosage', 1.0):.1f}x"
        elif fname == 'age':
            val_str = f"{profile.get('age', 55)} years"
        elif fname == 'baseline_sbp':
            val_str = f"{profile.get('baseline_sbp', 130)} mmHg"
        elif fname == 'baseline_dbp':
            val_str = f"{profile.get('baseline_dbp', 85)} mmHg"
        elif fname == 'heart_rate':
            val_str = f"{profile.get('heart_rate', 70)} bpm"
        else:
            val_str = str(profile.get(fname, ''))
        
        arrow = "\u2193" if sv < 0 else "\u2191"
        lines.append(
            f"{rank}. **{dname}** ({val_str}) {arrow} "
            f"contributes **{sv:+.2f} mmHg** \u2014 {context}"
        )
    
    # Closing note
    lines.append("")
    lines.append(
        "*These SHAP values show how each feature pushes the prediction "
        "above or below the model's average. This is a model-internal "
        "explanation, not a clinical interpretation.*"
    )
    
    return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 60)
    print("XAI ENGINE — SELF TEST")
    print("=" * 60)
    
    resources = load_xai_resources()
    print(f"Model loaded, background shape: {resources['background_data'].shape}")
    
    test_profile = {
        'age': 60,
        'baseline_sbp': 155,
        'baseline_dbp': 95,
        'heart_rate': 80,
        'risk_group': 'high',
        'drug_class': 'beta_blocker',
        'dosage': 1.0
    }
    
    result = explain_prediction(test_profile, resources)
    
    if result:
        print(f"\nSHAP values (SBP): {result['shap_values_sbp']}")
        print(f"SHAP values (DBP): {result['shap_values_dbp']}")
        print(f"\nTop drivers:")
        for name, sv, direction, _ in result['top_drivers']:
            print(f"  {name}: {sv:+.3f} ({direction})")
        print(f"\nInterpretation:\n{result['interpretation']}")
    
    print("\nSelf-test complete.")
