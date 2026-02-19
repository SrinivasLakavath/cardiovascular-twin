"""
ML Surrogate Digital Twin - Evaluation

Evaluates the trained surrogate twin model with comprehensive metrics
and physiological sanity checks.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib


def load_model_and_data():
    """
    Load trained model and test data.
    
    Returns
    -------
    model, X_test, y_test, df_test
    """
    print("Loading model and data...")
    
    # Load model
    from model import SurrogateTwin
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
    
    # Prepare test set (same split as training)
    from sklearn.model_selection import train_test_split
    feature_cols = [
        'age', 'baseline_sbp', 'baseline_dbp', 'heart_rate',
        'risk_group_encoded', 'drug_class_encoded', 'dosage'
    ]
    target_cols = ['delta_sbp', 'delta_dbp']
    
    X = df[feature_cols].values
    y = df[target_cols].values
    
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    _, df_test = train_test_split(df, test_size=0.2, random_state=42)
    
    return model, X_test, y_test, df_test


def evaluate_metrics(model, X_test, y_test):
    """
    Compute comprehensive evaluation metrics.
    
    Parameters
    ----------
    model : SurrogateTwin
        Trained model
    X_test : array-like
        Test features
    y_test : array-like
        Test targets
    
    Returns
    -------
    dict
        Evaluation metrics
    """
    print("\nComputing Evaluation Metrics...")
    print("-" * 50)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Metrics for delta_sbp
    mae_sbp = mean_absolute_error(y_test[:, 0], y_pred[:, 0])
    rmse_sbp = np.sqrt(mean_squared_error(y_test[:, 0], y_pred[:, 0]))
    r2_sbp = r2_score(y_test[:, 0], y_pred[:, 0])
    
    # Metrics for delta_dbp
    mae_dbp = mean_absolute_error(y_test[:, 1], y_pred[:, 1])
    rmse_dbp = np.sqrt(mean_squared_error(y_test[:, 1], y_pred[:, 1]))
    r2_dbp = r2_score(y_test[:, 1], y_pred[:, 1])
    
    print("Delta SBP Metrics:")
    print(f"  MAE:  {mae_sbp:.4f} mmHg")
    print(f"  RMSE: {rmse_sbp:.4f} mmHg")
    print(f"  R²:   {r2_sbp:.4f}")
    
    print("\nDelta DBP Metrics:")
    print(f"  MAE:  {mae_dbp:.4f} mmHg")
    print(f"  RMSE: {rmse_dbp:.4f} mmHg")
    print(f"  R²:   {r2_dbp:.4f}")
    
    return {
        'mae_sbp': mae_sbp,
        'rmse_sbp': rmse_sbp,
        'r2_sbp': r2_sbp,
        'mae_dbp': mae_dbp,
        'rmse_dbp': rmse_dbp,
        'r2_dbp': r2_dbp,
        'y_pred': y_pred
    }


def physiological_sanity_checks(df_test, y_pred):
    """
    Perform physiological sanity checks.
    
    Parameters
    ----------
    df_test : DataFrame
        Test dataset with intervention info
    y_pred : array-like
        Predicted responses
    
    Returns
    -------
    dict
        Sanity check results
    """
    print("\n" + "=" * 50)
    print("Physiological Sanity Checks:")
    print("=" * 50)
    
    df_test = df_test.copy()
    df_test['pred_delta_sbp'] = y_pred[:, 0]
    df_test['pred_delta_dbp'] = y_pred[:, 1]
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Beta blockers should decrease BP
    print("\nCheck 1: Beta blockers should decrease BP")
    beta_blocker_data = df_test[df_test['drug_class'] == 'beta_blocker']
    if len(beta_blocker_data) > 0:
        avg_delta_sbp = beta_blocker_data['pred_delta_sbp'].mean()
        print(f"  Average delta_sbp for beta_blocker: {avg_delta_sbp:.2f}")
        if avg_delta_sbp < 0:
            print("  ✓ PASS: Beta blockers decrease SBP")
            checks_passed += 1
        else:
            print("  ✗ FAIL: Beta blockers should decrease SBP")
        total_checks += 1
    
    # Check 2: Vasodilators should decrease BP
    print("\nCheck 2: Vasodilators should decrease BP")
    vasodilator_data = df_test[df_test['drug_class'] == 'vasodilator']
    if len(vasodilator_data) > 0:
        avg_delta_sbp = vasodilator_data['pred_delta_sbp'].mean()
        print(f"  Average delta_sbp for vasodilator: {avg_delta_sbp:.2f}")
        if avg_delta_sbp < 0:
            print("  ✓ PASS: Vasodilators decrease SBP")
            checks_passed += 1
        else:
            print("  ✗ FAIL: Vasodilators should decrease SBP")
        total_checks += 1
    
    # Check 3: Stimulants should increase BP
    print("\nCheck 3: Stimulants should increase BP")
    stimulant_data = df_test[df_test['drug_class'] == 'stimulant']
    if len(stimulant_data) > 0:
        avg_delta_sbp = stimulant_data['pred_delta_sbp'].mean()
        print(f"  Average delta_sbp for stimulant: {avg_delta_sbp:.2f}")
        if avg_delta_sbp > 0:
            print("  ✓ PASS: Stimulants increase SBP")
            checks_passed += 1
        else:
            print("  ✗ FAIL: Stimulants should increase SBP")
        total_checks += 1
    
    # Check 4: Higher dosage should increase magnitude
    print("\nCheck 4: Higher dosage should increase response magnitude")
    for drug in ['beta_blocker', 'vasodilator', 'stimulant']:
        drug_data = df_test[df_test['drug_class'] == drug]
        if len(drug_data) > 0:
            low_dose = drug_data[drug_data['dosage'] <= 0.5]['pred_delta_sbp'].abs().mean()
            high_dose = drug_data[drug_data['dosage'] >= 1.5]['pred_delta_sbp'].abs().mean()
            print(f"  {drug}: low dose |Δ|={low_dose:.2f}, high dose |Δ|={high_dose:.2f}")
            if high_dose > low_dose:
                print(f"    ✓ PASS")
                checks_passed += 1
            else:
                print(f"    ✗ FAIL")
            total_checks += 1
    
    print("\n" + "=" * 50)
    print(f"Sanity Checks: {checks_passed}/{total_checks} passed")
    print("=" * 50)
    
    return {
        'checks_passed': checks_passed,
        'total_checks': total_checks,
        'pass_rate': checks_passed / total_checks if total_checks > 0 else 0
    }


def main():
    """Main evaluation pipeline."""
    print("=" * 50)
    print("SURROGATE DIGITAL TWIN - EVALUATION")
    print("=" * 50)
    
    # Load model and data
    model, X_test, y_test, df_test = load_model_and_data()
    
    # Evaluate metrics
    metrics = evaluate_metrics(model, X_test, y_test)
    
    # Physiological sanity checks
    sanity_results = physiological_sanity_checks(df_test, metrics['y_pred'])
    
    print("\n" + "=" * 50)
    print("✓ Evaluation complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
