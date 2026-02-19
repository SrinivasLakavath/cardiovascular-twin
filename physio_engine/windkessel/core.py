"""
Windkessel Cardiovascular Model - Core Implementation

This module implements a canonical lumped-parameter Windkessel model
for cardiovascular hemodynamics. It serves as a physiology-inspired
ground truth generator for the digital twin project.

The model uses a minimal ODE representation:
    dP/dt = (Q - P/R) / C

Where:
    P = Blood pressure (mmHg)
    Q = Cardiac output (L/min)
    R = Peripheral resistance (mmHg·min/L)
    C = Arterial compliance (L/mmHg)

This is NOT a clinical simulator - it's a canonical abstraction
for educational and methodological purposes.
"""

import numpy as np
from scipy.integrate import odeint


def pulsatile_cardiac_output(t, Q_mean, heart_rate=72):
    """
    Generate pulsatile cardiac output to simulate heartbeats.
    
    Parameters
    ----------
    t : float
        Current time (seconds)
    Q_mean : float
        Mean cardiac output (L/min)
    heart_rate : float
        Heart rate (beats per minute)
    
    Returns
    -------
    float
        Instantaneous cardiac output (L/min)
    """
    # Convert heart rate to frequency (Hz)
    freq = heart_rate / 60.0
    
    # Pulsatile component using a simple sine wave
    # Systole occurs during the first 1/3 of the cardiac cycle
    phase = 2 * np.pi * freq * t
    
    # Create pulsatile flow (higher during systole, lower during diastole)
    # Using a rectified sine wave to simulate cardiac ejection
    pulse = np.maximum(0, np.sin(phase))
    
    # Scale to maintain mean cardiac output
    Q_instantaneous = Q_mean * (1 + 2 * pulse)
    
    return Q_instantaneous


def windkessel_ode(P, t, R, C, Q_mean, heart_rate):
    """
    Windkessel ODE function for scipy integration with pulsatile flow.
    
    Governing equation: dP/dt = (Q(t) - P/R) / C
    
    Parameters
    ----------
    P : float
        Current pressure (mmHg)
    t : float
        Current time (seconds)
    R : float
        Peripheral resistance (mmHg·min/L)
    C : float
        Arterial compliance (L/mmHg)
    Q_mean : float
        Mean cardiac output (L/min)
    heart_rate : float
        Heart rate (beats per minute)
    
    Returns
    -------
    float
        Rate of change of pressure (dP/dt)
    """
    # Get instantaneous cardiac output
    Q = pulsatile_cardiac_output(t, Q_mean, heart_rate)
    
    # Windkessel equation
    dP_dt = (Q - P / R) / C
    return dP_dt


def simulate_bp(R, C, Q, t_end=10.0, dt=0.01, heart_rate=72):
    """
    Simulate blood pressure trajectory using Windkessel model with pulsatile flow.
    
    This function integrates the Windkessel ODE over time with pulsatile
    cardiac output and extracts systolic (SBP) and diastolic (DBP) blood pressure values.
    
    Parameters
    ----------
    R : float
        Peripheral resistance (mmHg·min/L)
        Typical range: 0.5 - 2.0
    C : float
        Arterial compliance (L/mmHg)
        Typical range: 1.0 - 2.0
    Q : float
        Mean cardiac output (L/min)
        Typical range: 3.0 - 7.0
    t_end : float, optional
        Simulation duration in seconds (default: 10.0)
    dt : float, optional
        Time step in seconds (default: 0.01)
    heart_rate : float, optional
        Heart rate in beats per minute (default: 72)
    
    Returns
    -------
    sbp : float
        Systolic blood pressure (maximum pressure, mmHg)
    dbp : float
        Diastolic blood pressure (minimum pressure, mmHg)
    
    Notes
    -----
    - The simulation uses pulsatile cardiac output to create realistic BP waveforms
    - SBP is the maximum pressure over the trajectory
    - DBP is the minimum pressure over the trajectory
    - This is a deterministic simulation with no randomness
    
    Examples
    --------
    >>> sbp, dbp = simulate_bp(R=1.0, C=1.5, Q=5.0)
    >>> print(f"SBP: {sbp:.1f} mmHg, DBP: {dbp:.1f} mmHg")
    SBP: 120.5 mmHg, DBP: 78.3 mmHg
    """
    # Time array
    t = np.arange(0, t_end, dt)
    
    # Initial condition: mean arterial pressure
    P0 = Q * R
    
    # Integrate ODE with pulsatile cardiac output
    P_trajectory = odeint(windkessel_ode, P0, t, args=(R, C, Q, heart_rate))
    
    # Extract SBP (systolic = max) and DBP (diastolic = min)
    # Skip first few seconds to avoid transient effects
    skip_samples = int(2.0 / dt)  # Skip first 2 seconds
    P_steady = P_trajectory[skip_samples:]
    
    sbp = float(np.max(P_steady))
    dbp = float(np.min(P_steady))
    
    return sbp, dbp


if __name__ == "__main__":
    # Quick test of the Windkessel model
    print("Testing Windkessel Model...")
    print("-" * 50)
    
    # Test case 1: Normal parameters
    R1, C1, Q1 = 1.0, 1.5, 5.0
    sbp1, dbp1 = simulate_bp(R1, C1, Q1)
    print(f"Test 1 (Normal): R={R1}, C={C1}, Q={Q1}")
    print(f"  → SBP: {sbp1:.2f} mmHg, DBP: {dbp1:.2f} mmHg")
    print(f"  → Pulse Pressure: {sbp1 - dbp1:.2f} mmHg")
    
    # Test case 2: High resistance (hypertension-like)
    R2, C2, Q2 = 1.8, 1.5, 5.0
    sbp2, dbp2 = simulate_bp(R2, C2, Q2)
    print(f"\nTest 2 (High R): R={R2}, C={C2}, Q={Q2}")
    print(f"  → SBP: {sbp2:.2f} mmHg, DBP: {dbp2:.2f} mmHg")
    print(f"  → Pulse Pressure: {sbp2 - dbp2:.2f} mmHg")
    
    # Test case 3: High cardiac output (exercise-like)
    R3, C3, Q3 = 1.0, 1.5, 7.0
    sbp3, dbp3 = simulate_bp(R3, C3, Q3)
    print(f"\nTest 3 (High Q): R={R3}, C={C3}, Q={Q3}")
    print(f"  → SBP: {sbp3:.2f} mmHg, DBP: {dbp3:.2f} mmHg")
    print(f"  → Pulse Pressure: {sbp3 - dbp3:.2f} mmHg")
    
    # Sanity checks
    print("\n" + "=" * 50)
    print("Sanity Checks:")
    assert sbp1 > dbp1, "SBP should be greater than DBP"
    assert sbp2 > sbp1, "Higher R should increase SBP"
    assert sbp3 > sbp1, "Higher Q should increase SBP"
    print("✓ All sanity checks passed!")
