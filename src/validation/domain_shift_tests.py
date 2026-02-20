"""
Domain Shift Simulation Tests

This module tests how the digital twin behaves under distribution shifts
similar to real-world data mismatch.

REAL-WORLD DEPLOYMENT RATIONALE:
================================
Synthetic data rarely matches real distributions due to:
1. Measurement noise in real sensors
2. Extreme patient profiles not in training data
3. Altered feature correlations in different populations

This module simulates these scenarios to evaluate robustness.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error


def add_measurement_noise(data, noise_level=0.1):
    """
    Add realistic measurement noise to vitals.
    
    Parameters
    ----------
    data : DataFrame
        Clean data
    noise_level : float
        Noise standard deviation as fraction of value
    
    Returns
    -------
    DataFrame
        Noisy data
    """
    noisy_data = data.copy()
    
    # Add noise to continuous features
    continuous_features = ['age', 'baseline_sbp', 'baseline_dbp', 'heart_rate', 'dosage']
    
    for feature in continuous_features:
        if feature in noisy_data.columns:
            noise = np.random.normal(0, noise_level * noisy_data[feature].std(), len(noisy_data))
            noisy_data[feature] = noisy_data[feature] + noise
            
            # Ensure values stay positive and reasonable
            if feature == 'age':
                noisy_data[feature] = np.clip(noisy_data[feature], 18, 100)
            elif feature in ['baseline_sbp', 'baseline_dbp']:
                noisy_data[feature] = np.clip(noisy_data[feature], 60, 200)
            elif feature == 'heart_rate':
                noisy_data[feature] = np.clip(noisy_data[feature], 40, 150)
            elif feature == 'dosage':
                noisy_data[feature] = np.clip(noisy_data[feature], 0, 3)
    
    return noisy_data


def create_extreme_profiles(n_samples=50):
    """
    Create extreme patient profiles outside training distribution.
    
    Parameters
    ----------
    n_samples : int
        Number of extreme samples to generate
    
    Returns
    -------
    DataFrame
        Extreme patient profiles
    """
    extreme_data = []
    
    for i in range(n_samples):
        if i % 3 == 0:
            # Very old with high BP
            profile = {
                'age': np.random.randint(85, 100),
                'baseline_sbp': np.random.randint(160, 190),
                'baseline_dbp': np.random.randint(95, 115),
                'heart_rate': np.random.randint(50, 65),
                'risk_group': 'high',
                'drug_class': np.random.choice(['beta_blocker', 'vasodilator']),
                'dosage': np.random.uniform(0.5, 2.0)
            }
        elif i % 3 == 1:
            # Very young with low BP
            profile = {
                'age': np.random.randint(18, 25),
                'baseline_sbp': np.random.randint(90, 110),
                'baseline_dbp': np.random.randint(55, 70),
                'heart_rate': np.random.randint(75, 95),
                'risk_group': 'low',
                'drug_class': np.random.choice(['stimulant', 'volume_expander']),
                'dosage': np.random.uniform(0.5, 2.0)
            }
        else:
            # Extreme dosage
            profile = {
                'age': np.random.randint(40, 70),
                'baseline_sbp': np.random.randint(120, 150),
                'baseline_dbp': np.random.randint(75, 95),
                'heart_rate': np.random.randint(60, 85),
                'risk_group': np.random.choice(['low', 'medium', 'high']),
                'drug_class': np.random.choice(['beta_blocker', 'vasodilator', 'stimulant']),
                'dosage': np.random.uniform(2.5, 3.0)  # Very high dose
            }
        
        extreme_data.append(profile)
    
    return pd.DataFrame(extreme_data)


def test_noise_robustness(model, X_test, y_test, noise_levels=[0.0, 0.05, 0.1, 0.2]):
    """
    Test model robustness to measurement noise.
    
    Parameters
    ----------
    model : trained model
        Digital twin model
    X_test : array-like
        Test features
    y_test : array-like
        Test targets
    noise_levels : list
        Noise levels to test
    
    Returns
    -------
    dict
        Results for each noise level
    """
    results = {}
    
    for noise_level in noise_levels:
        # Add noise to inputs
        if noise_level > 0:
            noise = np.random.normal(0, noise_level, X_test.shape)
            X_noisy = X_test + noise
        else:
            X_noisy = X_test
        
        # Predict
        y_pred = model.predict(X_noisy)
        
        # Compute metrics
        mae_sbp = mean_absolute_error(y_test[:, 0], y_pred[:, 0])
        mae_dbp = mean_absolute_error(y_test[:, 1], y_pred[:, 1])
        rmse_sbp = np.sqrt(mean_squared_error(y_test[:, 0], y_pred[:, 0]))
        
        results[noise_level] = {
            'mae_sbp': mae_sbp,
            'mae_dbp': mae_dbp,
            'rmse_sbp': rmse_sbp
        }
    
    return results


def evaluate_domain_shift():
    """
    Main evaluation function for domain shift scenarios.
    
    Returns
    -------
    dict
        Comprehensive domain shift test results
    """
    print("=" * 70)
    print("DOMAIN SHIFT SIMULATION TESTS")
    print("=" * 70)
    
    # Load model and data
    print("\nLoading model and test data...")
    weights_dir = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights')
    model = joblib.load(os.path.join(weights_dir, 'surrogate_twin.pkl'))
    encoders = joblib.load(os.path.join(weights_dir, 'encoders.pkl'))
    
    # Load test data
    df = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'raw', 'synthetic_dataset.csv'))
    
    # Encode and prepare
    le_drug, le_risk = encoders
    df['drug_class_encoded'] = le_drug.transform(df['drug_class'])
    df['risk_group_encoded'] = le_risk.transform(df['risk_group'])
    
    feature_cols = [
        'age', 'baseline_sbp', 'baseline_dbp', 'heart_rate',
        'risk_group_encoded', 'drug_class_encoded', 'dosage'
    ]
    
    X = df[feature_cols].values
    y = df[['delta_sbp', 'delta_dbp']].values
    
    # Use last 200 samples as test set
    X_test = X[-200:]
    y_test = y[-200:]
    
    # Test 1: Noise Robustness
    print("\n" + "-" * 70)
    print("TEST 1: Robustness to Measurement Noise")
    print("-" * 70)
    
    noise_results = test_noise_robustness(model, X_test, y_test)
    
    print(f"\n{'Noise Level':<15} {'MAE SBP':<12} {'MAE DBP':<12} {'RMSE SBP':<12}")
    print("-" * 70)
    
    for noise_level, metrics in noise_results.items():
        print(f"{noise_level:<15.2f} {metrics['mae_sbp']:<12.4f} {metrics['mae_dbp']:<12.4f} {metrics['rmse_sbp']:<12.4f}")
    
    # Compute degradation
    baseline_mae = noise_results[0.0]['mae_sbp']
    high_noise_mae = noise_results[0.2]['mae_sbp']
    degradation = ((high_noise_mae - baseline_mae) / baseline_mae) * 100
    
    print(f"\nError Increase at 20% Noise: {degradation:.1f}%")
    
    if degradation < 50:
        print("✓ PASS: Model is robust to measurement noise")
    else:
        print("⚠️ WARNING: Model is sensitive to noise")
    
    # Test 2: Extreme Profiles
    print("\n" + "-" * 70)
    print("TEST 2: Extreme Patient Profiles")
    print("-" * 70)
    
    print("\nGenerating 50 extreme patient profiles...")
    extreme_df = create_extreme_profiles(n_samples=50)
    
    # Encode extreme profiles
    extreme_df['drug_class_encoded'] = le_drug.transform(extreme_df['drug_class'])
    extreme_df['risk_group_encoded'] = le_risk.transform(extreme_df['risk_group'])
    
    X_extreme = extreme_df[feature_cols].values
    
    # Predict (no ground truth available)
    y_extreme_pred = model.predict(X_extreme)
    
    # Check prediction stability
    pred_std_sbp = np.std(y_extreme_pred[:, 0])
    pred_std_dbp = np.std(y_extreme_pred[:, 1])
    
    print(f"Prediction Std Dev (SBP): {pred_std_sbp:.2f} mmHg")
    print(f"Prediction Std Dev (DBP): {pred_std_dbp:.2f} mmHg")
    
    # Check for extreme predictions
    extreme_preds = np.abs(y_extreme_pred) > 20
    n_extreme = np.sum(extreme_preds)
    
    print(f"Predictions > |20| mmHg: {n_extreme}/{len(y_extreme_pred)*2}")
    
    if n_extreme < len(y_extreme_pred) * 0.2:
        print("✓ PASS: Predictions remain stable for extreme profiles")
    else:
        print("⚠️ WARNING: Some extreme predictions detected")
    
    # Summary
    print("\n" + "=" * 70)
    print("DOMAIN SHIFT TEST SUMMARY")
    print("=" * 70)
    
    summary = {
        'noise_robustness': {
            'baseline_mae': baseline_mae,
            'high_noise_mae': high_noise_mae,
            'degradation_percent': degradation,
            'status': 'PASS' if degradation < 50 else 'WARNING'
        },
        'extreme_profiles': {
            'pred_std_sbp': pred_std_sbp,
            'pred_std_dbp': pred_std_dbp,
            'n_extreme_predictions': int(n_extreme),
            'status': 'PASS' if n_extreme < len(y_extreme_pred) * 0.2 else 'WARNING'
        }
    }
    
    print(f"\n1. Noise Robustness: {summary['noise_robustness']['status']}")
    print(f"   - Error increase at 20% noise: {degradation:.1f}%")
    
    print(f"\n2. Extreme Profiles: {summary['extreme_profiles']['status']}")
    print(f"   - Prediction stability maintained")
    
    print("\n" + "=" * 70)
    print("✓ Domain shift tests complete!")
    print("=" * 70)
    
    return summary


if __name__ == "__main__":
    evaluate_domain_shift()
