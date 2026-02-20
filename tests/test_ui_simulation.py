"""
Quick test to verify UI simulation functions work correctly.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

# Test V1 simulation
print("=" * 70)
print("TESTING V1 SIMULATION FUNCTION")
print("=" * 70)

test_profile = {
    'age': 65,
    'baseline_sbp': 145,
    'baseline_dbp': 90,
    'heart_rate': 75,
    'risk_group': 'high',
    'drug_class': 'beta_blocker',
    'dosage': 1.0
}

try:
    import joblib
    import numpy as np
    
    # Load model
    model_path = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights', 'surrogate_twin.pkl')
    encoders_path = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights', 'encoders.pkl')
    
    print(f"\nChecking model files...")
    print(f"Model exists: {os.path.exists(model_path)}")
    print(f"Encoders exist: {os.path.exists(encoders_path)}")
    
    if os.path.exists(model_path) and os.path.exists(encoders_path):
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
        
        # Predict
        prediction = model.predict(features)[0]
        
        print(f"\n✓ V1 Simulation SUCCESS!")
        print(f"  Input: Age={test_profile['age']}, SBP={test_profile['baseline_sbp']}, Drug={test_profile['drug_class']}, Dose={test_profile['dosage']}")
        print(f"  Output: Δ SBP = {prediction[0]:.2f} mmHg, Δ DBP = {prediction[1]:.2f} mmHg")
        
        # Test with different dosage
        test_profile2 = test_profile.copy()
        test_profile2['dosage'] = 2.0
        
        drug_encoded2 = le_drug.transform([test_profile2['drug_class']])[0]
        risk_encoded2 = le_risk.transform([test_profile2['risk_group']])[0]
        
        features2 = np.array([[
            test_profile2['age'],
            test_profile2['baseline_sbp'],
            test_profile2['baseline_dbp'],
            test_profile2['heart_rate'],
            risk_encoded2,
            drug_encoded2,
            test_profile2['dosage']
        ]])
        
        prediction2 = model.predict(features2)[0]
        
        print(f"\n✓ Testing with different dosage (2.0):")
        print(f"  Output: Δ SBP = {prediction2[0]:.2f} mmHg, Δ DBP = {prediction2[1]:.2f} mmHg")
        
        if abs(prediction[0] - prediction2[0]) > 0.01:
            print(f"\n✓ Model is DYNAMIC (predictions change with inputs)")
        else:
            print(f"\n✗ Model appears STATIC (predictions don't change)")
    else:
        print("\n✗ Model files not found!")
        print("  Run: python twin_model/train.py")
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
