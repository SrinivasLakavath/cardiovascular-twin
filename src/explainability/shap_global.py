"""
Global SHAP Explainability

Computes global feature importance using SHAP values to understand
which features drive cardiovascular response predictions.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

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
    weights_dir = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights')
    model = SurrogateTwin.load(os.path.join(weights_dir, 'surrogate_twin.pkl'))
    
    # Load encoders and feature names
    encoders = joblib.load(os.path.join(weights_dir, 'encoders.pkl'))
    feature_names = joblib.load(os.path.join(weights_dir, 'feature_names.pkl'))
    
    # Load dataset
    df = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'raw', 'synthetic_dataset.csv'))
    
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
    
    return model, X_test, feature_names


def compute_global_shap(model, X_test, feature_names):
    """
    Compute global SHAP values.
    
    Parameters
    ----------
    model : SurrogateTwin
        Trained model
    X_test : array-like
        Test data
    feature_names : list
        Feature names
    
    Returns
    -------
    explainer, shap_values
    """
    print("\nComputing SHAP values...")
    print("(This may take a few moments...)")
    
    # Use a subset for faster computation
    X_sample = X_test[:100]
    
    # Create SHAP explainer
    explainer = shap.Explainer(model.predict, X_sample)
    
    # Compute SHAP values
    shap_values = explainer(X_sample)
    
    print("✓ SHAP values computed!")
    
    return explainer, shap_values


def plot_global_importance(shap_values, feature_names):
    """
    Plot global feature importance.
    
    Parameters
    ----------
    shap_values : shap.Explanation
        SHAP values
    feature_names : list
        Feature names
    """
    print("\nGenerating global importance plots...")
    
    os.makedirs('explainability/plots', exist_ok=True)
    
    # Plot for delta_sbp (output 0)
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values[:, :, 0], feature_names=feature_names, show=False)
    plt.title('Global Feature Importance for Delta SBP', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('explainability/plots/global_importance_sbp.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: explainability/plots/global_importance_sbp.png")
    
    # Plot for delta_dbp (output 1)
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values[:, :, 1], feature_names=feature_names, show=False)
    plt.title('Global Feature Importance for Delta DBP', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('explainability/plots/global_importance_dbp.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: explainability/plots/global_importance_dbp.png")
    
    # Bar plot for mean absolute SHAP values
    plt.figure(figsize=(10, 6))
    shap.plots.bar(shap_values[:, :, 0], show=False)
    plt.title('Mean |SHAP| for Delta SBP', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('explainability/plots/global_bar_sbp.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: explainability/plots/global_bar_sbp.png")


def main():
    """Main global SHAP analysis."""
    print("=" * 50)
    print("GLOBAL SHAP EXPLAINABILITY ANALYSIS")
    print("=" * 50)
    
    # Load model and data
    model, X_test, feature_names = load_model_and_data()
    
    # Compute SHAP values
    explainer, shap_values = compute_global_shap(model, X_test, feature_names)
    
    # Plot global importance
    plot_global_importance(shap_values, feature_names)
    
    print("\n" + "=" * 50)
    print("✓ Global SHAP analysis complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
