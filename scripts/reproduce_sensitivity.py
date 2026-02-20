
import sys
import os
import numpy as np

# Add project root and src to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

from physio_engine.windkessel.core import simulate_bp

def test_sensitivity():
    print("Testing Windkessel Sensitivity to Extreme Values")
    print("================================================")
    
    # Baseline
    R_base, C_base, Q_base = 1.0, 1.5, 5.0
    sbp_base, dbp_base = simulate_bp(R_base, C_base, Q_base)
    print(f"Baseline (R={R_base}, C={C_base}, Q={Q_base}):")
    print(f"  SBP: {sbp_base:.2f}, DBP: {dbp_base:.2f}")
    
    # Extreme High Resistance (+200%)
    R_high = R_base * 3.0
    sbp_high_R, dbp_high_R = simulate_bp(R_high, C_base, Q_base)
    print(f"\nHigh Resistance (R={R_high}):")
    print(f"  SBP: {sbp_high_R:.2f}, DBP: {dbp_high_R:.2f}")
    print(f"  Change SBP: {sbp_high_R - sbp_base:.2f}")
    
    # Extreme Low Compliance (-80%)
    C_low = C_base * 0.2
    sbp_low_C, dbp_low_C = simulate_bp(R_base, C_low, Q_base)
    print(f"\nLow Compliance (C={C_low}):")
    print(f"  SBP: {sbp_low_C:.2f}, DBP: {dbp_low_C:.2f}")
    print(f"  Change SBP: {sbp_low_C - sbp_base:.2f}")
    
    # Extreme High Cardiac Output (+200%)
    Q_high = Q_base * 3.0
    sbp_high_Q, dbp_high_Q = simulate_bp(R_base, C_base, Q_high)
    print(f"\nHigh Cardiac Output (Q={Q_high}):")
    print(f"  SBP: {sbp_high_Q:.2f}, DBP: {dbp_high_Q:.2f}")
    print(f"  Change SBP: {sbp_high_Q - sbp_base:.2f}")

if __name__ == "__main__":
    test_sensitivity()
