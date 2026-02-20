"""
Cross-check backend results with UI display.
Verify that the values shown in UI match actual model predictions.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

import joblib
import numpy as np

print("=" * 70)
print("BACKEND vs UI CROSS-CHECK")
print("=" * 70)

# Test profile matching the screenshot
test_profile = {
    'age': 55,  # Default from screenshot
    'baseline_sbp': 130,
    'baseline_dbp': 85,
    'heart_rate': 123,  # From screenshot
    'risk_group': 'medium',
    'drug_class': 'beta_blocker',
    'dosage': 2.0  # From screenshot
}

print(f"\nTest Profile:")
print(f"  Age: {test_profile['age']}")
print(f"  Baseline SBP: {test_profile['baseline_sbp']} mmHg")
print(f"  Baseline DBP: {test_profile['baseline_dbp']} mmHg")
print(f"  Heart Rate: {test_profile['heart_rate']} bpm")
print(f"  Risk Group: {test_profile['risk_group']}")
print(f"  Drug Class: {test_profile['drug_class']}")
print(f"  Dosage: {test_profile['dosage']}")

# Load model and encoders
model_path = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights', 'surrogate_twin.pkl')
encoders_path = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights', 'encoders.pkl')

model = joblib.load(model_path)
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

# Predict (V1 - clean)
prediction = model.predict(features)[0]

print(f"\n" + "=" * 70)
print("BACKEND PREDICTION (V1)")
print("=" * 70)
print(f"Δ SBP: {prediction[0]:.2f} mmHg")
print(f"Δ DBP: {prediction[1]:.2f} mmHg")

print(f"\n" + "=" * 70)
print("EXPECTED UI DISPLAY")
print("=" * 70)
print(f"Card 1 (Δ SBP): {prediction[0]:.2f}")
print(f"Card 2 (Δ DBP): {prediction[1]:.2f}")
print(f"Color: {'Blue (#3182CE)' if prediction[0] < 0 else 'Red (#C53030)'} (negative = blue)")

print(f"\n" + "=" * 70)
print("SCREENSHOT VALUES (from user)")
print("=" * 70)
print(f"Δ SBP shown: -5.12")
print(f"Δ DBP shown: -4.37")

print(f"\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)
print(f"Backend Δ SBP: {prediction[0]:.2f}")
print(f"UI shows Δ SBP: -5.12")
print(f"Match: {'✓' if abs(prediction[0] - (-5.12)) < 0.01 else '✗ MISMATCH'}")
print()
print(f"Backend Δ DBP: {prediction[1]:.2f}")
print(f"UI shows Δ DBP: -4.37")
print(f"Match: {'✓' if abs(prediction[1] - (-4.37)) < 0.01 else '✗ MISMATCH'}")

print(f"\n" + "=" * 70)
