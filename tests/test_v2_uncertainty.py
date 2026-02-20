"""
Test V2 uncertainty calculation to verify it returns non-zero values.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

from v2_real_world.uncertainty.uncertainty_wrapper import UncertaintyWrapper
import joblib
import numpy as np

print("=" * 70)
print("V2 UNCERTAINTY CALCULATION TEST")
print("=" * 70)

# Test profile
test_profile = {
    'age': 55,
    'baseline_sbp': 130,
    'baseline_dbp': 85,
    'heart_rate': 123,
    'risk_group': 'medium',
    'drug_class': 'beta_blocker',
    'dosage': 2.0
}

print(f"\nTest Profile: {test_profile['drug_class']}, dosage={test_profile['dosage']}")

# Load encoders
encoders_path = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights', 'encoders.pkl')
encoders = joblib.load(encoders_path)
le_drug, le_risk = encoders

# Encode inputs
drug_encoded = le_drug.transform([test_profile['drug_class']])[0]
risk_encoded = le_risk.transform([test_profile['risk_group']])[0]

# Prepare features
features = np.array([[
    test_profile['age'],
    test_profile['baseline_sbp'],
    test_profile['baseline_dbp'],
    test_profile['heart_rate'],
    risk_encoded,
    drug_encoded,
    test_profile['dosage']
]])

print(f"\nCalling UncertaintyWrapper.predict_with_uncertainty()...")

# Predict with uncertainty
wrapper = UncertaintyWrapper()
result = wrapper.predict_with_uncertainty(features, n_samples=30)

print(f"\n" + "=" * 70)
print("RESULT:")
print("=" * 70)
print(f"Prediction: {result['prediction']}")
print(f"Uncertainty: {result['uncertainty']}")
print(f"Confidence: {result['confidence_level']}")

print(f"\n" + "=" * 70)
print("FORMATTED OUTPUT (as UI should show):")
print("=" * 70)
print(f"Δ SBP: {result['prediction'][0]:.2f} mmHg")
print(f"Uncertainty: ± {result['uncertainty'][0]:.2f} mmHg")
print(f"")
print(f"Δ DBP: {result['prediction'][1]:.2f} mmHg")
print(f"Uncertainty: ± {result['uncertainty'][1]:.2f} mmHg")
print(f"")
print(f"Confidence: {result['confidence_level'].upper()}")

# Check if uncertainty is non-zero
if result['uncertainty'][0] > 0 and result['uncertainty'][1] > 0:
    print(f"\n✓ SUCCESS: Uncertainty values are NON-ZERO")
else:
    print(f"\n✗ FAILURE: Uncertainty values are ZERO (BUG!)")
    print(f"  SBP uncertainty: {result['uncertainty'][0]}")
    print(f"  DBP uncertainty: {result['uncertainty'][1]}")

print(f"\n" + "=" * 70)
