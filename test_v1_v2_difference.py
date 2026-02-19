"""
Test to verify V1 and V2 produce DIFFERENT outputs.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# Import the simulation functions
from ui_app.sections.output_panel import simulate_v1_response, simulate_v2_response

print("=" * 70)
print("V1 vs V2 OUTPUT DIFFERENCE TEST")
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

print(f"\nTest Profile:")
print(f"  Drug: {test_profile['drug_class']}")
print(f"  Dosage: {test_profile['dosage']}")
print(f"  Age: {test_profile['age']}")
print(f"  Baseline BP: {test_profile['baseline_sbp']}/{test_profile['baseline_dbp']}")

print(f"\n" + "=" * 70)
print("RUNNING V1 SIMULATION")
print("=" * 70)
v1_result = simulate_v1_response(test_profile)

print(f"\n" + "=" * 70)
print("RUNNING V2 SIMULATION")
print("=" * 70)
v2_result = simulate_v2_response(test_profile)

print(f"\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)

print(f"\nV1 Output:")
print(f"  Δ SBP: {v1_result['delta_sbp']:.2f} mmHg")
print(f"  Δ DBP: {v1_result['delta_dbp']:.2f} mmHg")
print(f"  Uncertainty: Not applicable (V1)")

print(f"\nV2 Output:")
print(f"  Δ SBP: {v2_result['delta_sbp']:.2f} ± {v2_result.get('sbp_uncertainty', 0):.2f} mmHg")
print(f"  Δ DBP: {v2_result['delta_dbp']:.2f} ± {v2_result.get('dbp_uncertainty', 0):.2f} mmHg")
print(f"  Confidence: {v2_result.get('confidence', 'UNKNOWN')}")

print(f"\n" + "=" * 70)
print("VALIDATION CHECKS")
print("=" * 70)

# Check 1: Different predictions
sbp_diff = abs(v1_result['delta_sbp'] - v2_result['delta_sbp'])
dbp_diff = abs(v1_result['delta_dbp'] - v2_result['delta_dbp'])

print(f"\n1. Predictions are DIFFERENT:")
print(f"   SBP difference: {sbp_diff:.4f} mmHg")
print(f"   DBP difference: {dbp_diff:.4f} mmHg")

if sbp_diff > 0.01 or dbp_diff > 0.01:
    print(f"   ✓ PASS: V1 and V2 produce different outputs")
else:
    print(f"   ✗ FAIL: V1 and V2 produce identical outputs (BUG!)")

# Check 2: V2 has uncertainty
print(f"\n2. V2 has NON-ZERO uncertainty:")
sbp_unc = v2_result.get('sbp_uncertainty', 0)
dbp_unc = v2_result.get('dbp_uncertainty', 0)

print(f"   SBP uncertainty: {sbp_unc:.4f} mmHg")
print(f"   DBP uncertainty: {dbp_unc:.4f} mmHg")

if sbp_unc > 0 and dbp_unc > 0:
    print(f"   ✓ PASS: V2 has non-zero uncertainty")
else:
    print(f"   ✗ FAIL: V2 uncertainty is zero (BUG!)")

# Check 3: V1 has no uncertainty
print(f"\n3. V1 has NO uncertainty field:")
if 'sbp_uncertainty' not in v1_result and 'dbp_uncertainty' not in v1_result:
    print(f"   ✓ PASS: V1 correctly has no uncertainty")
else:
    print(f"   ✗ FAIL: V1 should not have uncertainty")

# Check 4: V2 has confidence level
print(f"\n4. V2 has confidence level:")
if 'confidence' in v2_result:
    print(f"   Confidence: {v2_result['confidence']}")
    print(f"   ✓ PASS: V2 has confidence level")
else:
    print(f"   ✗ FAIL: V2 missing confidence level")

print(f"\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

all_pass = (
    (sbp_diff > 0.01 or dbp_diff > 0.01) and
    sbp_unc > 0 and dbp_unc > 0 and
    'sbp_uncertainty' not in v1_result and
    'confidence' in v2_result
)

if all_pass:
    print("\n✓ ALL CHECKS PASSED")
    print("  V1 and V2 are properly separated")
    print("  V2 shows uncertainty, V1 does not")
    print("  Outputs are numerically different")
else:
    print("\n✗ SOME CHECKS FAILED")
    print("  Review the validation results above")

print(f"\n" + "=" * 70)
