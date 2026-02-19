"""
Real-World Blood Pressure Statistics Extraction

This module extracts realistic BP distributions and variability
from Kaggle data to ground synthetic data generation.

PURPOSE:
========
- Compute mean, std, percentiles for SBP and DBP
- Stratify by age bins if available
- Provide realistic noise parameters
- Enable distribution shift analysis

USAGE:
======
These statistics are used to:
1. Normalize inputs (scale adapter)
2. Estimate realistic measurement noise
3. Analyze domain shift between synthetic and real
4. Calibrate synthetic data generation

NOT USED FOR:
=============
- Training ML models
- Inferring drug effects
- Making clinical predictions
"""

import pandas as pd
import numpy as np
import json
import os


def compute_bp_statistics(df):
    """
    Compute comprehensive BP statistics.
    
    Parameters
    ----------
    df : DataFrame
        Blood pressure data with SBP, DBP columns
    
    Returns
    -------
    dict
        Statistics dictionary
    """
    stats = {}
    
    # Overall statistics
    if 'SBP' in df.columns:
        stats['sbp'] = {
            'mean': float(df['SBP'].mean()),
            'std': float(df['SBP'].std()),
            'median': float(df['SBP'].median()),
            'min': float(df['SBP'].min()),
            'max': float(df['SBP'].max()),
            'q25': float(df['SBP'].quantile(0.25)),
            'q75': float(df['SBP'].quantile(0.75)),
            'iqr': float(df['SBP'].quantile(0.75) - df['SBP'].quantile(0.25))
        }
    
    if 'DBP' in df.columns:
        stats['dbp'] = {
            'mean': float(df['DBP'].mean()),
            'std': float(df['DBP'].std()),
            'median': float(df['DBP'].median()),
            'min': float(df['DBP'].min()),
            'max': float(df['DBP'].max()),
            'q25': float(df['DBP'].quantile(0.25)),
            'q75': float(df['DBP'].quantile(0.75)),
            'iqr': float(df['DBP'].quantile(0.75) - df['DBP'].quantile(0.25))
        }
    
    # Pulse pressure
    if 'SBP' in df.columns and 'DBP' in df.columns:
        pulse_pressure = df['SBP'] - df['DBP']
        stats['pulse_pressure'] = {
            'mean': float(pulse_pressure.mean()),
            'std': float(pulse_pressure.std())
        }
    
    # Age statistics if available
    if 'Age' in df.columns:
        stats['age'] = {
            'mean': float(df['Age'].mean()),
            'std': float(df['Age'].std()),
            'min': float(df['Age'].min()),
            'max': float(df['Age'].max())
        }
    
    # Sample size
    stats['n_samples'] = len(df)
    
    return stats


def compute_age_stratified_stats(df, age_bins=[0, 40, 60, 120]):
    """
    Compute BP statistics stratified by age groups.
    
    Parameters
    ----------
    df : DataFrame
        Blood pressure data
    age_bins : list
        Age bin edges
    
    Returns
    -------
    dict
        Age-stratified statistics
    """
    if 'Age' not in df.columns:
        return {}
    
    age_stats = {}
    
    # Create age groups
    df['age_group'] = pd.cut(df['Age'], bins=age_bins, 
                             labels=[f'{age_bins[i]}-{age_bins[i+1]}' 
                                    for i in range(len(age_bins)-1)])
    
    for age_group in df['age_group'].unique():
        if pd.isna(age_group):
            continue
            
        group_data = df[df['age_group'] == age_group]
        
        age_stats[str(age_group)] = {
            'n': len(group_data),
            'sbp_mean': float(group_data['SBP'].mean()) if 'SBP' in group_data.columns else None,
            'sbp_std': float(group_data['SBP'].std()) if 'SBP' in group_data.columns else None,
            'dbp_mean': float(group_data['DBP'].mean()) if 'DBP' in group_data.columns else None,
            'dbp_std': float(group_data['DBP'].std()) if 'DBP' in group_data.columns else None
        }
    
    return age_stats


def estimate_measurement_noise(df):
    """
    Estimate realistic measurement noise parameters.
    
    Parameters
    ----------
    df : DataFrame
        Blood pressure data
    
    Returns
    -------
    dict
        Noise parameters
    """
    noise_params = {}
    
    # Estimate noise as a fraction of IQR (robust to outliers)
    if 'SBP' in df.columns:
        sbp_iqr = df['SBP'].quantile(0.75) - df['SBP'].quantile(0.25)
        # Typical BP measurement noise is ~5 mmHg
        # Express as fraction of IQR for scaling
        noise_params['sbp_noise_std'] = 5.0  # mmHg
        noise_params['sbp_noise_fraction'] = 5.0 / sbp_iqr if sbp_iqr > 0 else 0.1
    
    if 'DBP' in df.columns:
        dbp_iqr = df['DBP'].quantile(0.75) - df['DBP'].quantile(0.25)
        noise_params['dbp_noise_std'] = 3.0  # mmHg
        noise_params['dbp_noise_fraction'] = 3.0 / dbp_iqr if dbp_iqr > 0 else 0.1
    
    return noise_params


def save_statistics(stats, filepath='v2_real_world/data/bp_statistics.json'):
    """
    Save statistics to JSON file.
    
    Parameters
    ----------
    stats : dict
        Statistics dictionary
    filepath : str
        Output path
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"✓ Statistics saved to: {filepath}")


def load_statistics(filepath='v2_real_world/data/bp_statistics.json'):
    """
    Load statistics from JSON file.
    
    Parameters
    ----------
    filepath : str
        Input path
    
    Returns
    -------
    dict
        Statistics dictionary
    """
    with open(filepath, 'r') as f:
        stats = json.load(f)
    return stats


if __name__ == "__main__":
    print("=" * 70)
    print("VERSION 2: REAL-WORLD STATISTICS EXTRACTION")
    print("=" * 70)
    
    # Load data
    try:
        df = pd.read_csv('v2_real_world/data/kaggle_bp_data.csv')
        print(f"✓ Loaded data: {len(df)} rows")
    except:
        print("⚠️ Could not load Kaggle data, run kaggle_loader.py first")
        print("Creating demo statistics...")
        # Create demo data
        np.random.seed(42)
        df = pd.DataFrame({
            'SBP': np.random.normal(130, 18, 1000),
            'DBP': np.random.normal(82, 12, 1000),
            'Age': np.random.randint(20, 80, 1000)
        })
    
    # Compute statistics
    print("\nComputing overall statistics...")
    overall_stats = compute_bp_statistics(df)
    
    print("\nComputing age-stratified statistics...")
    age_stats = compute_age_stratified_stats(df)
    
    print("\nEstimating measurement noise...")
    noise_params = estimate_measurement_noise(df)
    
    # Combine all statistics
    all_stats = {
        'overall': overall_stats,
        'age_stratified': age_stats,
        'noise_parameters': noise_params
    }
    
    # Display summary
    print("\n" + "=" * 70)
    print("STATISTICS SUMMARY")
    print("=" * 70)
    
    if 'sbp' in overall_stats:
        print(f"\nSBP: {overall_stats['sbp']['mean']:.1f} ± {overall_stats['sbp']['std']:.1f} mmHg")
        print(f"     Range: [{overall_stats['sbp']['min']:.1f}, {overall_stats['sbp']['max']:.1f}]")
    
    if 'dbp' in overall_stats:
        print(f"\nDBP: {overall_stats['dbp']['mean']:.1f} ± {overall_stats['dbp']['std']:.1f} mmHg")
        print(f"     Range: [{overall_stats['dbp']['min']:.1f}, {overall_stats['dbp']['max']:.1f}]")
    
    print(f"\nMeasurement Noise:")
    print(f"  SBP: {noise_params.get('sbp_noise_std', 0):.1f} mmHg")
    print(f"  DBP: {noise_params.get('dbp_noise_std', 0):.1f} mmHg")
    
    # Save statistics
    save_statistics(all_stats)
    
    print("\n" + "=" * 70)
    print("✓ Statistics extraction complete!")
    print("=" * 70)
    print("\nThese statistics will be used for:")
    print("  - Input normalization")
    print("  - Realistic noise injection")
    print("  - Domain shift analysis")
