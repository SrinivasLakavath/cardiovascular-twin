"""
Physiological Validation Checks

Validates that the digital twin respects known cardiovascular trends
and physiological principles.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split


def load_model_and_data():
    """Load trained model and test data."""
    print("Loading model and data...")
    
    # Load model using joblib directly
    import joblib as jl
    weights_dir = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights')
    model = jl.load(os.path.join(weights_dir, 'surrogate_twin.pkl'))
    
    # Load encoders
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
    _, df_test = train_test_split(df, test_size=0.2, random_state=42)
    
    # Get predictions
    y_pred = model.predict(X_test)
    df_test = df_test.copy()
    df_test['pred_delta_sbp'] = y_pred[:, 0]
    df_test['pred_delta_dbp'] = y_pred[:, 1]
    
    return model, df_test


def check_directional_correctness(df_test):
    """
    Check that interventions have correct directional effects.
    
    Parameters
    ----------
    df_test : DataFrame
        Test data with predictions
    
    Returns
    -------
    bool
        True if all checks pass
    """
    print("\n" + "=" * 50)
    print("CHECK 1: Directional Correctness")
    print("=" * 50)
    
    all_passed = True
    
    # Beta blockers should decrease BP
    beta_data = df_test[df_test['drug_class'] == 'beta_blocker']
    avg_delta = beta_data['pred_delta_sbp'].mean()
    print(f"\nBeta Blocker: avg delta_sbp = {avg_delta:.2f} mmHg")
    assert avg_delta < 0, "Beta blockers should decrease SBP"
    print("  ✓ PASS: Beta blockers decrease BP")
    
    # Vasodilators should decrease BP
    vaso_data = df_test[df_test['drug_class'] == 'vasodilator']
    avg_delta = vaso_data['pred_delta_sbp'].mean()
    print(f"\nVasodilator: avg delta_sbp = {avg_delta:.2f} mmHg")
    assert avg_delta < 0, "Vasodilators should decrease SBP"
    print("  ✓ PASS: Vasodilators decrease BP")
    
    # Stimulants should increase BP
    stim_data = df_test[df_test['drug_class'] == 'stimulant']
    avg_delta = stim_data['pred_delta_sbp'].mean()
    print(f"\nStimulant: avg delta_sbp = {avg_delta:.2f} mmHg")
    assert avg_delta > 0, "Stimulants should increase SBP"
    print("  ✓ PASS: Stimulants increase BP")
    
    return all_passed


def check_dose_response(df_test):
    """
    Check that higher doses produce larger magnitude responses.
    
    Parameters
    ----------
    df_test : DataFrame
        Test data with predictions
    
    Returns
    -------
    bool
        True if all checks pass
    """
    print("\n" + "=" * 50)
    print("CHECK 2: Dose-Response Relationship")
    print("=" * 50)
    
    all_passed = True
    
    for drug in ['beta_blocker', 'vasodilator', 'stimulant']:
        drug_data = df_test[df_test['drug_class'] == drug]
        
        low_dose = drug_data[drug_data['dosage'] <= 0.5]['pred_delta_sbp'].abs().mean()
        high_dose = drug_data[drug_data['dosage'] >= 1.5]['pred_delta_sbp'].abs().mean()
        
        print(f"\n{drug}:")
        print(f"  Low dose (≤0.5): |Δ| = {low_dose:.2f} mmHg")
        print(f"  High dose (≥1.5): |Δ| = {high_dose:.2f} mmHg")
        
        assert high_dose > low_dose, f"{drug}: Higher dose should have larger effect"
        print(f"  ✓ PASS: Dose-response is monotonic")
    
    return all_passed


def check_physiological_bounds(df_test):
    """
    Check that predictions stay within physiological bounds.
    
    Parameters
    ----------
    df_test : DataFrame
        Test data with predictions
    
    Returns
    -------
    bool
        True if all checks pass
    """
    print("\n" + "=" * 50)
    print("CHECK 3: Physiological Bounds")
    print("=" * 50)
    
    # Check that delta values are reasonable (not extreme)
    max_delta_sbp = df_test['pred_delta_sbp'].abs().max()
    max_delta_dbp = df_test['pred_delta_dbp'].abs().max()
    
    print(f"\nMax |delta_sbp|: {max_delta_sbp:.2f} mmHg")
    print(f"Max |delta_dbp|: {max_delta_dbp:.2f} mmHg")
    
    # Reasonable bounds: delta should not exceed ±50 mmHg
    assert max_delta_sbp < 50, "Delta SBP should be within ±50 mmHg"
    assert max_delta_dbp < 50, "Delta DBP should be within ±50 mmHg"
    print("  ✓ PASS: All predictions within physiological bounds")
    
    return True


def check_sbp_dbp_relationship(df_test):
    """
    Check that SBP and DBP changes are correlated.
    
    Parameters
    ----------
    df_test : DataFrame
        Test data with predictions
    
    Returns
    -------
    bool
        True if all checks pass
    """
    print("\n" + "=" * 50)
    print("CHECK 4: SBP-DBP Relationship")
    print("=" * 50)
    
    # Compute correlation
    correlation = df_test['pred_delta_sbp'].corr(df_test['pred_delta_dbp'])
    
    print(f"\nCorrelation between delta_sbp and delta_dbp: {correlation:.3f}")
    
    # SBP and DBP changes should be positively correlated
    assert correlation > 0.5, "SBP and DBP changes should be correlated"
    print("  ✓ PASS: SBP and DBP changes are correlated")
    
    return True


def main():
    """Main physiological validation."""
    print("=" * 50)
    print("PHYSIOLOGICAL VALIDATION CHECKS")
    print("=" * 50)
    
    # Load model and data
    model, df_test = load_model_and_data()
    
    # Run all checks
    try:
        check_directional_correctness(df_test)
        check_dose_response(df_test)
        check_physiological_bounds(df_test)
        check_sbp_dbp_relationship(df_test)
        
        print("\n" + "=" * 50)
        print("✓ ALL PHYSIOLOGICAL CHECKS PASSED!")
        print("=" * 50)
        print("\nConclusion: The digital twin respects known cardiovascular trends.")
        
    except AssertionError as e:
        print(f"\n✗ VALIDATION FAILED: {e}")
        raise


if __name__ == "__main__":
    main()
