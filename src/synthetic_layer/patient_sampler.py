"""
Synthetic Patient Sampler

Generates reproducible synthetic patient profiles for the digital twin.
This module creates patient baseline characteristics without using real data.
"""

import random


def sample_patient(seed=None):
    """
    Generate a synthetic patient profile with baseline cardiovascular parameters.
    
    This function creates a synthetic patient with realistic but generic ranges
    for cardiovascular parameters. It uses seeded randomness for reproducibility.
    
    Parameters
    ----------
    seed : int, optional
        Random seed for reproducibility. If None, uses current time.
    
    Returns
    -------
    dict
        Patient profile containing:
        - age : int (20-80 years)
        - baseline_sbp : int (100-160 mmHg)
        - baseline_dbp : int (60-100 mmHg)
        - heart_rate : int (50-100 bpm)
        - risk_group : str ('low', 'medium', 'high')
    
    Examples
    --------
    >>> patient = sample_patient(seed=42)
    >>> print(patient)
    {'age': 55, 'baseline_sbp': 130, 'baseline_dbp': 85, 
     'heart_rate': 72, 'risk_group': 'medium'}
    
    >>> # Deterministic - same seed gives same patient
    >>> p1 = sample_patient(seed=42)
    >>> p2 = sample_patient(seed=42)
    >>> assert p1 == p2
    """
    # Set random seed for reproducibility
    if seed is not None:
        random.seed(seed)
    
    # Sample age (20-80 years)
    age = random.randint(20, 80)
    
    # Sample baseline SBP (100-160 mmHg)
    # Older patients tend to have higher BP
    age_factor = (age - 20) / 60.0  # 0 to 1
    sbp_min = 100 + int(age_factor * 20)
    sbp_max = 140 + int(age_factor * 20)
    baseline_sbp = random.randint(sbp_min, sbp_max)
    
    # Sample baseline DBP (60-100 mmHg)
    # DBP should be roughly 60% of SBP
    dbp_target = int(baseline_sbp * 0.6)
    baseline_dbp = random.randint(max(60, dbp_target - 10), 
                                   min(100, dbp_target + 10))
    
    # Sample heart rate (50-100 bpm)
    # Younger patients tend to have higher HR
    hr_min = 50 + int((1 - age_factor) * 10)
    hr_max = 80 + int((1 - age_factor) * 20)
    heart_rate = random.randint(hr_min, hr_max)
    
    # Determine risk group based on BP
    if baseline_sbp < 120 and baseline_dbp < 80:
        risk_group = 'low'
    elif baseline_sbp < 140 and baseline_dbp < 90:
        risk_group = 'medium'
    else:
        risk_group = 'high'
    
    return {
        'age': age,
        'baseline_sbp': baseline_sbp,
        'baseline_dbp': baseline_dbp,
        'heart_rate': heart_rate,
        'risk_group': risk_group
    }


def sample_patients_batch(n_patients, seed=None):
    """
    Generate a batch of synthetic patients.
    
    Parameters
    ----------
    n_patients : int
        Number of patients to generate
    seed : int, optional
        Random seed for reproducibility
    
    Returns
    -------
    list of dict
        List of patient profiles
    
    Examples
    --------
    >>> patients = sample_patients_batch(100, seed=42)
    >>> len(patients)
    100
    """
    if seed is not None:
        random.seed(seed)
    
    patients = []
    for i in range(n_patients):
        # Use different seed for each patient
        patient_seed = seed + i if seed is not None else None
        patients.append(sample_patient(seed=patient_seed))
    
    return patients


if __name__ == "__main__":
    # Test patient sampler
    print("Testing Patient Sampler...")
    print("-" * 50)
    
    # Test 1: Single patient
    print("\nTest 1: Single Patient")
    patient = sample_patient(seed=42)
    for key, value in patient.items():
        print(f"  {key}: {value}")
    
    # Test 2: Determinism
    print("\nTest 2: Determinism Check")
    p1 = sample_patient(seed=42)
    p2 = sample_patient(seed=42)
    assert p1 == p2, "Same seed should produce same patient"
    print("  ✓ Determinism verified")
    
    # Test 3: Batch generation
    print("\nTest 3: Batch Generation")
    patients = sample_patients_batch(10, seed=100)
    print(f"  Generated {len(patients)} patients")
    
    # Show distribution
    risk_counts = {'low': 0, 'medium': 0, 'high': 0}
    for p in patients:
        risk_counts[p['risk_group']] += 1
    
    print(f"  Risk distribution: {risk_counts}")
    
    # Test 4: Value ranges
    print("\nTest 4: Value Range Checks")
    for p in patients:
        assert 20 <= p['age'] <= 80, "Age out of range"
        assert 100 <= p['baseline_sbp'] <= 160, "SBP out of range"
        assert 60 <= p['baseline_dbp'] <= 100, "DBP out of range"
        assert 50 <= p['heart_rate'] <= 100, "HR out of range"
        assert p['risk_group'] in ['low', 'medium', 'high'], "Invalid risk group"
    
    print("  ✓ All value ranges valid")
    
    print("\n" + "=" * 50)
    print("✓ All tests passed!")
