"""
Intervention Mapper

Maps abstract intervention classes to Windkessel model parameter changes.
This module defines how different drug classes affect cardiovascular parameters.
"""


def map_intervention(drug_class, dosage, baseline_params=None):
    """
    Map an intervention (drug class + dosage) to Windkessel parameter changes.
    
    This function abstracts interventions as parameter modifications rather than
    simulating real drugs. Each drug class has explicit, interpretable effects
    on the Windkessel model parameters (R, C, Q).
    
    Parameters
    ----------
    drug_class : str
        Type of intervention. Supported values:
        - 'beta_blocker': Decreases cardiac output (Q)
        - 'vasodilator': Decreases peripheral resistance (R)
        - 'stimulant': Increases cardiac output (Q)
        - 'volume_expander': Increases arterial compliance (C)
        - 'none': No intervention (baseline)
    dosage : float
        Dosage level (0.0 to 2.0)
        - 0.0: No effect
        - 1.0: Standard dose
        - 2.0: High dose
    baseline_params : dict, optional
        Baseline parameters {'R': float, 'C': float, 'Q': float}
        If None, uses default values
    
    Returns
    -------
    dict
        Modified parameters {'R': float, 'C': float, 'Q': float}
    
    Notes
    -----
    Intervention Effects:
    - beta_blocker: Q' = Q * (1 - 0.3 * dosage)
    - vasodilator: R' = R * (1 - 0.25 * dosage)
    - stimulant: Q' = Q * (1 + 0.4 * dosage)
    - volume_expander: C' = C * (1 + 0.2 * dosage)
    
    These are simplified, explicit assumptions for educational purposes.
    NOT based on real pharmacokinetics.
    
    Examples
    --------
    >>> params = map_intervention('beta_blocker', 1.0)
    >>> print(params)
    {'R': 1.0, 'C': 1.5, 'Q': 3.5}  # Q reduced from 5.0
    
    >>> params = map_intervention('vasodilator', 1.5)
    >>> print(params)
    {'R': 0.625, 'C': 1.5, 'Q': 5.0}  # R reduced
    """
    # Default baseline parameters (normal physiology)
    if baseline_params is None:
        baseline_params = {
            'R': 1.0,   # Peripheral resistance (mmHg·min/L)
            'C': 1.5,   # Arterial compliance (L/mmHg)
            'Q': 5.0    # Cardiac output (L/min)
        }
    
    # Copy baseline parameters
    R = baseline_params['R']
    C = baseline_params['C']
    Q = baseline_params['Q']
    
    # Apply intervention-specific parameter changes
    if drug_class == 'beta_blocker':
        # Beta blockers reduce heart rate and contractility → decrease Q
        # Effect: Q' = Q * (1 - 0.3 * dosage)
        Q = Q * (1 - 0.3 * dosage)
    
    elif drug_class == 'vasodilator':
        # Vasodilators relax blood vessels → decrease R
        # Effect: R' = R * (1 - 0.25 * dosage)
        R = R * (1 - 0.25 * dosage)
    
    elif drug_class == 'stimulant':
        # Stimulants increase heart rate and contractility → increase Q
        # Effect: Q' = Q * (1 + 0.4 * dosage)
        Q = Q * (1 + 0.4 * dosage)
    
    elif drug_class == 'volume_expander':
        # Volume expanders increase blood volume → increase C
        # Effect: C' = C * (1 + 0.2 * dosage)
        C = C * (1 + 0.2 * dosage)
    
    elif drug_class == 'none':
        # No intervention - return baseline
        pass
    
    else:
        raise ValueError(f"Unknown drug class: {drug_class}. "
                        f"Supported: beta_blocker, vasodilator, stimulant, "
                        f"volume_expander, none")
    
    # Ensure parameters stay within physiological bounds
    R = max(0.3, min(3.0, R))  # Resistance: 0.3 - 3.0
    C = max(0.5, min(3.0, C))  # Compliance: 0.5 - 3.0
    Q = max(2.0, min(10.0, Q)) # Cardiac output: 2.0 - 10.0
    
    return {
        'R': R,
        'C': C,
        'Q': Q
    }


def get_intervention_description(drug_class):
    """
    Get a human-readable description of an intervention's mechanism.
    
    Parameters
    ----------
    drug_class : str
        Intervention class
    
    Returns
    -------
    str
        Description of the intervention's effect
    """
    descriptions = {
        'beta_blocker': 'Decreases cardiac output by reducing heart rate and contractility',
        'vasodilator': 'Decreases peripheral resistance by relaxing blood vessels',
        'stimulant': 'Increases cardiac output by increasing heart rate and contractility',
        'volume_expander': 'Increases arterial compliance by expanding blood volume',
        'none': 'No intervention (baseline)'
    }
    
    return descriptions.get(drug_class, 'Unknown intervention')


if __name__ == "__main__":
    # Test intervention mapper
    print("Testing Intervention Mapper...")
    print("-" * 50)
    
    # Test 1: Beta blocker
    print("\nTest 1: Beta Blocker (dosage=1.0)")
    params = map_intervention('beta_blocker', 1.0)
    print(f"  R={params['R']:.2f}, C={params['C']:.2f}, Q={params['Q']:.2f}")
    print(f"  Effect: {get_intervention_description('beta_blocker')}")
    assert params['Q'] < 5.0, "Beta blocker should decrease Q"
    
    # Test 2: Vasodilator
    print("\nTest 2: Vasodilator (dosage=1.0)")
    params = map_intervention('vasodilator', 1.0)
    print(f"  R={params['R']:.2f}, C={params['C']:.2f}, Q={params['Q']:.2f}")
    print(f"  Effect: {get_intervention_description('vasodilator')}")
    assert params['R'] < 1.0, "Vasodilator should decrease R"
    
    # Test 3: Stimulant
    print("\nTest 3: Stimulant (dosage=1.0)")
    params = map_intervention('stimulant', 1.0)
    print(f"  R={params['R']:.2f}, C={params['C']:.2f}, Q={params['Q']:.2f}")
    print(f"  Effect: {get_intervention_description('stimulant')}")
    assert params['Q'] > 5.0, "Stimulant should increase Q"
    
    # Test 4: Volume expander
    print("\nTest 4: Volume Expander (dosage=1.0)")
    params = map_intervention('volume_expander', 1.0)
    print(f"  R={params['R']:.2f}, C={params['C']:.2f}, Q={params['Q']:.2f}")
    print(f"  Effect: {get_intervention_description('volume_expander')}")
    assert params['C'] > 1.5, "Volume expander should increase C"
    
    # Test 5: Dose-response
    print("\nTest 5: Dose-Response (Beta Blocker)")
    for dose in [0.0, 0.5, 1.0, 1.5, 2.0]:
        params = map_intervention('beta_blocker', dose)
        print(f"  Dose={dose:.1f}: Q={params['Q']:.2f}")
    
    # Test 6: No intervention
    print("\nTest 6: No Intervention")
    params = map_intervention('none', 0.0)
    print(f"  R={params['R']:.2f}, C={params['C']:.2f}, Q={params['Q']:.2f}")
    assert params == {'R': 1.0, 'C': 1.5, 'Q': 5.0}, "No intervention should return baseline"
    
    # Test 7: Custom baseline
    print("\nTest 7: Custom Baseline")
    custom_baseline = {'R': 1.5, 'C': 1.2, 'Q': 6.0}
    params = map_intervention('beta_blocker', 1.0, baseline_params=custom_baseline)
    print(f"  Custom baseline Q={custom_baseline['Q']:.2f}")
    print(f"  After beta blocker Q={params['Q']:.2f}")
    assert params['Q'] < custom_baseline['Q'], "Should decrease from custom baseline"
    
    print("\n" + "=" * 50)
    print("✓ All tests passed!")
