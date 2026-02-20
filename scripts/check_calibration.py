
import sys
import os
import numpy as np

# Add project root and src to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

from physio_engine.windkessel.core import simulate_bp

def test_calibration():
    print("Testing Windkessel Calibration")
    print("==============================")
    
    # Attempt to find parameters that give normal BP (120/80)
    # MAP ~ 93. R = MAP / Q. Q=5. => R ~ 18.6
    
    R_cal = 18.0
    C_cal = 1.0  # Compliance
    Q_cal = 5.0
    
    sbp, dbp = simulate_bp(R_cal, C_cal, Q_cal)
    print(f"Test Calibration (R={R_cal}, C={C_cal}, Q={Q_cal}):")
    print(f"  SBP: {sbp:.2f} mmHg")
    print(f"  DBP: {dbp:.2f} mmHg")
    print(f"  MAP: {(sbp + 2*dbp)/3:.2f} mmHg")

if __name__ == "__main__":
    test_calibration()
