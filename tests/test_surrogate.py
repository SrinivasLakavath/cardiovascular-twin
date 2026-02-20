
import sys
import os
import joblib
import numpy as np

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

def test_surrogate_model():
    print("Testing Surrogate Model Sensitivity")
    print("===================================")
    
    model_path = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights', 'surrogate_twin.pkl')
    encoders_path = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights', 'encoders.pkl')
    
    try:
        model = joblib.load(model_path)
        encoders = joblib.load(encoders_path)
        le_drug, le_risk = encoders
        print("Model and encoders loaded successfully.")
    except Exception as e:
        print(f"FAILED to load model: {e}")
        return

    # Baseline Profile
    # age, baseline_sbp, baseline_dbp, heart_rate, risk_group, drug_class, dosage
    # Using 'medium' risk and 'beta_blocker'
    risk_encoded = le_risk.transform(['medium'])[0]
    drug_encoded = le_drug.transform(['beta_blocker'])[0]
    
    baseline_features = np.array([[
        55,     # age
        130,    # sbp
        85,     # dbp
        70,     # hr
        risk_encoded,
        drug_encoded,
        1.0     # dosage
    ]])
    
    pred_base = model.predict(baseline_features)[0]
    print(f"\nBaseline Prediction (Dosage 1.0):")
    print(f"  Delta SBP: {pred_base[0]:.2f}")
    print(f"  Delta DBP: {pred_base[1]:.2f}")
    
    # Extreme Dosage
    extreme_features = baseline_features.copy()
    extreme_features[0, 6] = 3.0  # Max dosage
    
    pred_extreme = model.predict(extreme_features)[0]
    print(f"\nExtreme Prediction (Dosage 3.0):")
    print(f"  Delta SBP: {pred_extreme[0]:.2f}")
    print(f"  Delta DBP: {pred_extreme[1]:.2f}")
    
    print(f"\nChange: {pred_extreme[0] - pred_base[0]:.2f}")

if __name__ == "__main__":
    test_surrogate_model()
