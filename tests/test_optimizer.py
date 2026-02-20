"""
Test Treatment Optimizer Logic
"""
import sys
import os
sys.path.append(os.getcwd())

from treatment_optimizer.optimizer import TreatmentOptimizer

def test_hypertensive_patient():
    """A hypertensive patient wanting 120/80 should get a BP-lowering drug."""
    print("Test 1: Hypertensive Patient (155/95 → 120/80)")
    
    optimizer = TreatmentOptimizer()
    
    profile = {
        'age': 60, 'baseline_sbp': 155, 'baseline_dbp': 95,
        'heart_rate': 80, 'risk_group': 'high',
        'drug_class': 'none', 'dosage': 0.0
    }
    
    result = optimizer.optimize(profile, target_sbp=120, target_dbp=80)
    best = result['best']
    
    print(f"  Recommended: {best['drug_name']} @ {best['dosage']:.1f}x")
    print(f"  Predicted BP: {best['predicted_sbp']:.0f}/{best['predicted_dbp']:.0f}")
    print(f"  Delta: {best['delta_sbp']:+.1f}/{best['delta_dbp']:+.1f}")
    
    # The optimizer should recommend a BP-lowering drug (beta_blocker or vasodilator)
    assert best['drug_class'] in ['beta_blocker', 'vasodilator'], \
        f"Expected BP-lowering drug, got {best['drug_class']}"
    assert best['delta_sbp'] < 0, "Expected negative SBP delta for hypertensive patient"
    print("  ✓ PASSED: Recommends BP-lowering drug\n")

def test_hypotensive_patient():
    """A hypotensive patient wanting 120/80 should get a BP-raising drug."""
    print("Test 2: Hypotensive Patient (90/55 → 120/80)")
    
    optimizer = TreatmentOptimizer()
    
    profile = {
        'age': 30, 'baseline_sbp': 90, 'baseline_dbp': 55,
        'heart_rate': 65, 'risk_group': 'low',
        'drug_class': 'none', 'dosage': 0.0
    }
    
    result = optimizer.optimize(profile, target_sbp=120, target_dbp=80)
    best = result['best']
    
    print(f"  Recommended: {best['drug_name']} @ {best['dosage']:.1f}x")
    print(f"  Predicted BP: {best['predicted_sbp']:.0f}/{best['predicted_dbp']:.0f}")
    print(f"  Delta: {best['delta_sbp']:+.1f}/{best['delta_dbp']:+.1f}")
    
    # Should recommend a BP-raising drug (stimulant or volume_expander)
    assert best['drug_class'] in ['stimulant', 'volume_expander'], \
        f"Expected BP-raising drug, got {best['drug_class']}"
    assert best['delta_sbp'] > 0, "Expected positive SBP delta for hypotensive patient"
    print("  ✓ PASSED: Recommends BP-raising drug\n")

def test_dose_monotonicity():
    """Higher target reduction should give higher doses."""
    print("Test 3: Dose Monotonicity")
    
    optimizer = TreatmentOptimizer()
    
    profile = {
        'age': 50, 'baseline_sbp': 160, 'baseline_dbp': 100,
        'heart_rate': 75, 'risk_group': 'high',
        'drug_class': 'none', 'dosage': 0.0
    }
    
    # Mild reduction target
    r1 = optimizer.optimize(profile, target_sbp=150, target_dbp=95)
    # Large reduction target
    r2 = optimizer.optimize(profile, target_sbp=120, target_dbp=80)
    
    print(f"  Mild target (150/95):  {r1['best']['drug_name']} @ {r1['best']['dosage']:.1f}x")
    print(f"  Large target (120/80): {r2['best']['drug_name']} @ {r2['best']['dosage']:.1f}x")
    
    # Larger target reduction should need higher dosage (or stronger drug)
    # We check that the absolute delta is larger for the more aggressive target
    assert abs(r2['best']['delta_sbp']) >= abs(r1['best']['delta_sbp']), \
        "Larger target should produce larger delta"
    print("  ✓ PASSED: More aggressive target gives stronger treatment\n")

def test_alternatives_exist():
    """Should provide at least 2 alternative drug classes."""
    print("Test 4: Alternatives Provided")
    
    optimizer = TreatmentOptimizer()
    
    profile = {
        'age': 55, 'baseline_sbp': 140, 'baseline_dbp': 90,
        'heart_rate': 72, 'risk_group': 'medium',
        'drug_class': 'none', 'dosage': 0.0
    }
    
    result = optimizer.optimize(profile, target_sbp=120, target_dbp=80)
    
    n_alts = len(result['alternatives'])
    print(f"  Best: {result['best']['drug_name']}")
    print(f"  Alternatives: {n_alts}")
    for alt in result['alternatives']:
        print(f"    - {alt['drug_name']} @ {alt['dosage']:.1f}x → {alt['predicted_sbp']:.0f}/{alt['predicted_dbp']:.0f}")
    
    assert n_alts >= 2, f"Expected at least 2 alternatives, got {n_alts}"
    print("  ✓ PASSED: Multiple alternatives provided\n")

if __name__ == "__main__":
    print("=" * 60)
    print("TREATMENT OPTIMIZER — VALIDATION TESTS")
    print("=" * 60 + "\n")
    
    test_hypertensive_patient()
    test_hypotensive_patient()
    test_dose_monotonicity()
    test_alternatives_exist()
    
    print("=" * 60)
    print("✓ ALL OPTIMIZER TESTS PASSED!")
    print("=" * 60)
