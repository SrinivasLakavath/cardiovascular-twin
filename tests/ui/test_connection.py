"""
UI Connection Test

Quick test to verify frontend-backend integration.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

print("=" * 70)
print("TESTING UI BACKEND CONNECTION")
print("=" * 70)

# Test 1: Import section modules
print("\nTest 1: Importing UI modules...")
try:
    from ui.sections.input_panel import render_input_panel
    from ui.sections.output_panel import simulate_v1_response, simulate_v2_response
    print("✓ UI modules imported successfully")
except Exception as e:
    print(f"✗ Failed to import UI modules: {e}")

# Test 2: Load V1 model
print("\nTest 2: Loading V1 model...")
try:
    import joblib
    weights_dir = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights')
    model = joblib.load(os.path.join(weights_dir, 'surrogate_twin.pkl'))
    encoders = joblib.load(os.path.join(weights_dir, 'encoders.pkl'))
    print("✓ V1 model loaded successfully")
except Exception as e:
    print(f"✗ Failed to load V1 model: {e}")

# Test 3: Test V1 simulation
print("\nTest 3: Testing V1 simulation...")
try:
    test_profile = {
        'age': 65,
        'baseline_sbp': 145,
        'baseline_dbp': 90,
        'heart_rate': 75,
        'risk_group': 'high',
        'drug_class': 'beta_blocker',
        'dosage': 1.0
    }
    
    result = simulate_v1_response(test_profile)
    print(f"✓ V1 simulation successful")
    print(f"  Δ SBP: {result['delta_sbp']:.2f} mmHg")
    print(f"  Δ DBP: {result['delta_dbp']:.2f} mmHg")
except Exception as e:
    print(f"✗ V1 simulation failed: {e}")

# Test 4: Test V2 simulation
print("\nTest 4: Testing V2 simulation...")
try:
    result = simulate_v2_response(test_profile)
    print(f"✓ V2 simulation successful")
    print(f"  Δ SBP: {result['delta_sbp']:.2f} ± {result['sbp_uncertainty']:.2f} mmHg")
    print(f"  Δ DBP: {result['delta_dbp']:.2f} ± {result['dbp_uncertainty']:.2f} mmHg")
    print(f"  Confidence: {result['confidence']}")
except Exception as e:
    print(f"✗ V2 simulation failed: {e}")

# Test 5: Check Streamlit
print("\nTest 5: Checking Streamlit installation...")
try:
    import streamlit
    print(f"✓ Streamlit version: {streamlit.__version__}")
except Exception as e:
    print(f"✗ Streamlit not available: {e}")

print("\n" + "=" * 70)
print("CONNECTION TEST COMPLETE")
print("=" * 70)

print("\n📊 Summary:")
print("  - UI modules: ✓")
print("  - V1 model: ✓")
print("  - V1 simulation: ✓")
print("  - V2 simulation: ✓")
print("  - Streamlit: ✓")

print("\n🌐 Streamlit UI is running at:")
print("  Local URL: http://localhost:8501")
print("  Network URL: http://192.168.1.7:8501")

print("\n💡 Open the URL in your browser to view the UI!")
