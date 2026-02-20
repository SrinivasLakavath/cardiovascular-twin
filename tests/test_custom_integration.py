
import sys
import os
import numpy as np

# Add project root to path
sys.path.append(os.getcwd())

from ui_app.sections.output_panel import simulate_v1_response, simulate_v2_response

def test_custom_integration():
    print("Testing Custom Integration...")
    
    # Define a custom profile
    profile = {
        'age': 55,
        'baseline_sbp': 130,
        'baseline_dbp': 85,
        'heart_rate': 70,
        'risk_group': 'medium',
        'drug_class': 'custom',
        'dosage': 1.0,
        'custom_params': {
            'r_change': -0.2, # Decrease Resistance by 20%
            'c_change': 0.0,
            'q_change': 0.0
        }
    }
    
    # Test V1 (Deterministic)
    print("\nTesting V1 (Deterministic)...")
    result_v1 = simulate_v1_response(profile)
    print(f"V1 Result: {result_v1}")
    
    # Expectation: Decreasing R by 20% should drop BP significantly
    # Baseline ~120/80. R'=0.8*R. P'=0.8*P.
    # Delta should be approx -20% of 120 = -24 mmHg
    delta_sbp = result_v1['delta_sbp']
    assert -30 < delta_sbp < -15, f"V1 Delta SBP {delta_sbp} out of expected range (-30 to -15)"
    print("✓ V1 Check Passed")
    
    # Test V2 (Stochastic)
    print("\nTesting V2 (Stochastic + Uncertainty)...")
    result_v2 = simulate_v2_response(profile)
    print(f"V2 Result: {result_v2}")
    
    # Expectation: Similar mean, but with uncertainty
    assert 'sbp_uncertainty' in result_v2, "V2 should have uncertainty"
    assert result_v2['sbp_uncertainty'] > 0, "V2 uncertainty should be non-zero"
    print("✓ V2 Check Passed")
    
    print("\nALL CUSTOM SCENARIO TESTS PASSED")

if __name__ == "__main__":
    test_custom_integration()
