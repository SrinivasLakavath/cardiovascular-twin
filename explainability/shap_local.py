"""
Local SHAP Explainability

Provides patient-specific explanations using SHAP values to understand
why the model made specific predictions for individual patients.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
import joblib
from sklearn.model_selection import train_test_split


def load_model_and_data():
    """Load trained model and data."""
    print("Loading model and data...")
    
    # Load model
    from twin_model.model import SurrogateTwin
    model = SurrogateTwin.load('twin_model/weights/surrogate_twin.pkl')
    
    # Load encoders and feature names
    encoders = joblib.load('twin_model/weights/encoders.pkl')
    feature_names = joblib.load('twin_model/weights/feature_names.pkl')
    
    # Load dataset
    df = pd.read_csv('data/raw/synthetic_dataset.csv')
    
    # Encode categorical variables
    le_drug, le_risk = encoders
    df['drug_class_encoded'] = le_drug.transform(df['drug_class'])
    df['risk_group_encoded'] = le_risk.transform(df['risk_group'])
    
    # Prepare data
    feature_cols = [
        'age', 'baseline_sbp', 'baseline_dbp', 'heart_rate',
        'risk_group_encoded', 'drug_class_encoded', 'dosage'
    ]
    
    X = df[feature_cols].values
    _, X_test = train_test_split(X, test_size=0.2, random_state=42)
    _, df_test = train_test_split(df, test_size=0.2, random_state=42)
    
    return model, X_test, df_test, feature_names


def explain_single_patient(model, X_sample, X_patient, feature_names, patient_idx):
    """
    Explain a single patient's prediction.
    
    Parameters
    ----------
    model : SurrogateTwin
        Trained model
    X_sample : array-like
        Background data for SHAP
    X_patient : array-like
        Patient data to explain
    feature_names : list
        Feature names
    patient_idx : int
        Patient index for naming
    """
    print(f"\nExplaining Patient #{patient_idx}...")
    
    # Create explainer
    explainer = shap.Explainer(model.predict, X_sample)
    
    # Compute SHAP values for this patient
    shap_values = explainer(X_patient.reshape(1, -1))
    
    # Make prediction
    prediction = model.predict(X_patient.reshape(1, -1))[0]
    
    print(f"  Predicted delta_sbp: {prediction[0]:.2f} mmHg")
    print(f"  Predicted delta_dbp: {prediction[1]:.2f} mmHg")
    
    # Plot waterfall for delta_sbp
    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_values[0, :, 0], show=False)
    plt.title(f'Patient #{patient_idx} - Delta SBP Explanation', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'explainability/plots/local_patient{patient_idx}_sbp.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: explainability/plots/local_patient{patient_idx}_sbp.png")
    
    # Plot waterfall for delta_dbp
    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_values[0, :, 1], show=False)
    plt.title(f'Patient #{patient_idx} - Delta DBP Explanation', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'explainability/plots/local_patient{patient_idx}_dbp.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: explainability/plots/local_patient{patient_idx}_dbp.png")


def compare_patients(model, X_sample, X_test, df_test, feature_names):
    """
    Compare explanations for different patients with same intervention.
    
    Parameters
    ----------
    model : SurrogateTwin
        Trained model
    X_sample : array-like
        Background data
    X_test : array-like
        Test data
    df_test : DataFrame
        Test dataframe
    feature_names : list
        Feature names
    """
    print("\nComparing Patients with Same Intervention...")
    print("-" * 50)
    
    # Find two patients with same drug and dosage but different responses
    beta_blocker_patients = df_test[
        (df_test['drug_class'] == 'beta_blocker') & 
        (df_test['dosage'] == 1.0)
    ]
    
    if len(beta_blocker_patients) >= 2:
        # Get indices
        idx1 = beta_blocker_patients.index[0] - df_test.index[0]
        idx2 = beta_blocker_patients.index[1] - df_test.index[0]
        
        # Explain both patients
        explain_single_patient(model, X_sample, X_test[idx1], feature_names, 1)
        explain_single_patient(model, X_sample, X_test[idx2], feature_names, 2)
        
        print("\n  → Both patients received beta_blocker at dosage 1.0")
        print("  → Differences in response are explained by patient characteristics")


def main():
    """Main local SHAP analysis."""
    print("=" * 50)
    print("LOCAL SHAP EXPLAINABILITY ANALYSIS")
    print("=" * 50)
    
    # Load model and data
    model, X_test, df_test, feature_names = load_model_and_data()
    
    # Use subset as background
    X_sample = X_test[:50]
    
    # Compare patients
    compare_patients(model, X_sample, X_test, df_test, feature_names)
    
    print("\n" + "=" * 50)
    print("✓ Local SHAP analysis complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
