"""
Synthetic Data Generator

Orchestrates the generation of synthetic cardiovascular response data
by combining patient sampling, intervention mapping, and physiology simulation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from patient_sampler import sample_patient
from intervention_mapper import map_intervention
from physio_engine.windkessel.core import simulate_bp


def generate_single_sample(patient_seed, drug_class, dosage):
    """
    Generate a single data sample.
    
    Parameters
    ----------
    patient_seed : int
        Seed for patient generation
    drug_class : str
        Intervention class
    dosage : float
        Dosage level
    
    Returns
    -------
    dict
        Data row with patient info, intervention, and BP response
    """
    # 1. Sample patient
    patient = sample_patient(seed=patient_seed)
    
    # 2. Get baseline Windkessel parameters
    # CALIBRATED PARAMETERS (Target: 120/80 mmHg)
    baseline_params = {
        'R': 18.0,  # Peripheral Resistance (increased from 1.0)
        'C': 1.0,   # Arterial Compliance (decreased from 1.5)
        'Q': 5.0    # Cardiac Output (L/min)
    }
    
    # 3. Simulate baseline BP
    sbp_baseline, dbp_baseline = simulate_bp(
        R=baseline_params['R'],
        C=baseline_params['C'],
        Q=baseline_params['Q'],
        heart_rate=patient['heart_rate']
    )
    
    # 4. Apply intervention
    modified_params = map_intervention(drug_class, dosage, baseline_params)
    
    # 5. Simulate post-intervention BP
    sbp_post, dbp_post = simulate_bp(
        R=modified_params['R'],
        C=modified_params['C'],
        Q=modified_params['Q'],
        heart_rate=patient['heart_rate']
    )
    
    # 6. Compute deltas
    delta_sbp = sbp_post - sbp_baseline
    delta_dbp = dbp_post - dbp_baseline
    
    # 7. Create data row
    data_row = {
        'age': patient['age'],
        'baseline_sbp': patient['baseline_sbp'],
        'baseline_dbp': patient['baseline_dbp'],
        'heart_rate': patient['heart_rate'],
        'risk_group': patient['risk_group'],
        'drug_class': drug_class,
        'dosage': dosage,
        'delta_sbp': delta_sbp,
        'delta_dbp': delta_dbp,
        # Also store simulated values for validation
        'sim_sbp_baseline': sbp_baseline,
        'sim_dbp_baseline': dbp_baseline,
        'sim_sbp_post': sbp_post,
        'sim_dbp_post': dbp_post
    }
    
    return data_row


def generate_dataset(n_samples=1000, output_path='data/raw/synthetic_dataset.csv', seed=42):
    """
    Generate a complete synthetic dataset.
    
    This function creates a controlled experiment by:
    1. Sampling diverse patients
    2. Applying various interventions at different dosages
    3. Simulating cardiovascular responses
    4. Computing BP changes (deltas)
    
    Parameters
    ----------
    n_samples : int, optional
        Number of samples to generate (default: 1000)
    output_path : str, optional
        Path to save CSV file (default: 'data/raw/synthetic_dataset.csv')
    seed : int, optional
        Random seed for reproducibility (default: 42)
    
    Returns
    -------
    pd.DataFrame
        Generated dataset
    
    Examples
    --------
    >>> df = generate_dataset(n_samples=100, seed=42)
    >>> print(df.shape)
    (100, 13)
    >>> print(df.columns)
    ['age', 'baseline_sbp', 'baseline_dbp', 'heart_rate', 'risk_group',
     'drug_class', 'dosage', 'delta_sbp', 'delta_dbp', ...]
    """
    print(f"Generating {n_samples} synthetic samples...")
    print("-" * 50)
    
    # Define intervention scenarios
    drug_classes = ['none', 'beta_blocker', 'vasodilator', 'stimulant', 'volume_expander']
    dosages = [0.0, 0.5, 1.0, 1.5, 2.0]
    
    data_rows = []
    sample_count = 0
    
    # Generate samples
    for i in range(n_samples):
        # Cycle through interventions and dosages
        drug_idx = i % len(drug_classes)
        dose_idx = (i // len(drug_classes)) % len(dosages)
        
        drug_class = drug_classes[drug_idx]
        dosage = dosages[dose_idx]
        
        # Generate sample
        patient_seed = seed + i
        data_row = generate_single_sample(patient_seed, drug_class, dosage)
        data_rows.append(data_row)
        
        sample_count += 1
        if sample_count % 100 == 0:
            print(f"  Generated {sample_count}/{n_samples} samples...")
    
    # Create DataFrame
    df = pd.DataFrame(data_rows)
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"\n✓ Dataset saved to: {output_path}")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    
    # Show summary statistics
    print("\nDataset Summary:")
    print(f"  Age range: {df['age'].min()}-{df['age'].max()}")
    print(f"  SBP range: {df['baseline_sbp'].min()}-{df['baseline_sbp'].max()}")
    print(f"  Delta SBP range: {df['delta_sbp'].min():.2f} to {df['delta_sbp'].max():.2f}")
    print(f"  Delta DBP range: {df['delta_dbp'].min():.2f} to {df['delta_dbp'].max():.2f}")
    
    print("\nIntervention distribution:")
    print(df['drug_class'].value_counts())
    
    print("\nRisk group distribution:")
    print(df['risk_group'].value_counts())
    
    return df


if __name__ == "__main__":
    # Generate dataset
    print("=" * 50)
    print("SYNTHETIC CARDIOVASCULAR DATASET GENERATOR")
    print("=" * 50)
    
    # Generate 1000 samples
    df = generate_dataset(n_samples=1000, seed=42)
    
    print("\n" + "=" * 50)
    print("✓ Data generation complete!")
    print("=" * 50)
