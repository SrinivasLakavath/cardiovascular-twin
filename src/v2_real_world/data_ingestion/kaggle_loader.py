"""
Kaggle Blood Pressure Dataset Loader

This module loads real-world blood pressure data from Kaggle
to ground Version 2 of the digital twin with realistic statistics.

DATASET: ahmedwadood/blood-pressure-dataset
SOURCE: Kaggle
PURPOSE: Extract real-world BP distributions for noise modeling

CRITICAL NOTES:
===============
1. This data is used for STATISTICS ONLY, not training
2. We do NOT infer drug effects from this data
3. We do NOT claim clinical accuracy
4. This grounds synthetic data in realistic variability
5. Version 1 remains unchanged and fully functional
"""

import pandas as pd
import numpy as np
import os


def load_kaggle_bp_data():
    """
    Load blood pressure dataset from Kaggle using kagglehub.
    
    Returns
    -------
    DataFrame
        Cleaned blood pressure data with relevant columns
    
    Notes
    -----
    This function uses kagglehub to automatically download and load
    the dataset. No manual download required.
    
    Dataset Limitations:
    - May not include intervention/drug information
    - May have measurement noise and outliers
    - Demographics may be limited
    - Not validated for clinical use
    """
    try:
        import kagglehub
        from kagglehub import KaggleDatasetAdapter
        
        print("Loading Kaggle blood pressure dataset...")
        print("Dataset: ahmedwadood/blood-pressure-dataset")
        
        # Load dataset using kagglehub
        df = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            'ahmedwadood/blood-pressure-dataset',
            file_path=''
        )
        
        print(f"✓ Dataset loaded: {len(df)} rows")
        
        # Display available columns
        print(f"Available columns: {list(df.columns)}")
        
        # Clean and prepare data
        df_cleaned = clean_bp_data(df)
        
        return df_cleaned
        
    except Exception as e:
        print(f"Error loading Kaggle dataset: {e}")
        print("Falling back to synthetic statistics...")
        return create_fallback_data()


def clean_bp_data(df):
    """
    Clean and prepare blood pressure data.
    
    Parameters
    ----------
    df : DataFrame
        Raw dataset
    
    Returns
    -------
    DataFrame
        Cleaned data with standardized columns
    """
    print("\nCleaning data...")
    
    # Try to identify SBP and DBP columns (case-insensitive)
    columns_lower = {col.lower(): col for col in df.columns}
    
    # Map common column names
    column_mapping = {}
    
    # Look for systolic BP
    for key in ['sbp', 'systolic', 'systolic_bp', 'sys_bp', 'systolic blood pressure']:
        if key in columns_lower:
            column_mapping['SBP'] = columns_lower[key]
            break
    
    # Look for diastolic BP
    for key in ['dbp', 'diastolic', 'diastolic_bp', 'dias_bp', 'diastolic blood pressure']:
        if key in columns_lower:
            column_mapping['DBP'] = columns_lower[key]
            break
    
    # Look for age
    for key in ['age', 'age_years', 'patient_age']:
        if key in columns_lower:
            column_mapping['Age'] = columns_lower[key]
            break
    
    if not column_mapping:
        print("⚠️ Could not identify BP columns automatically")
        print("Available columns:", list(df.columns))
        # Try to use first few numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            column_mapping = {
                'SBP': numeric_cols[0],
                'DBP': numeric_cols[1]
            }
            if len(numeric_cols) >= 3:
                column_mapping['Age'] = numeric_cols[2]
    
    # Rename columns
    df_clean = df.rename(columns={v: k for k, v in column_mapping.items()})
    
    # Select only relevant columns
    relevant_cols = [col for col in ['SBP', 'DBP', 'Age'] if col in df_clean.columns]
    df_clean = df_clean[relevant_cols].copy()
    
    # Remove missing values
    df_clean = df_clean.dropna()
    
    # Remove outliers (physiologically impossible values)
    if 'SBP' in df_clean.columns:
        df_clean = df_clean[(df_clean['SBP'] >= 70) & (df_clean['SBP'] <= 250)]
    if 'DBP' in df_clean.columns:
        df_clean = df_clean[(df_clean['DBP'] >= 40) & (df_clean['DBP'] <= 150)]
    if 'Age' in df_clean.columns:
        df_clean = df_clean[(df_clean['Age'] >= 0) & (df_clean['Age'] <= 120)]
    
    print(f"✓ Cleaned data: {len(df_clean)} rows, {len(df_clean.columns)} columns")
    print(f"  Columns: {list(df_clean.columns)}")
    
    return df_clean


def create_fallback_data():
    """
    Create fallback synthetic data if Kaggle load fails.
    
    Returns
    -------
    DataFrame
        Synthetic BP data with realistic distributions
    """
    print("Creating fallback synthetic data...")
    
    np.random.seed(42)
    n_samples = 1000
    
    # Generate realistic BP data
    age = np.random.randint(20, 80, n_samples)
    
    # Age-dependent BP
    sbp = 100 + 0.5 * age + np.random.normal(0, 15, n_samples)
    dbp = 60 + 0.3 * age + np.random.normal(0, 10, n_samples)
    
    df = pd.DataFrame({
        'SBP': sbp,
        'DBP': dbp,
        'Age': age
    })
    
    print(f"✓ Fallback data created: {len(df)} rows")
    
    return df


def save_data(df, filepath='v2_real_world/data/kaggle_bp_data.csv'):
    """
    Save cleaned data to CSV.
    
    Parameters
    ----------
    df : DataFrame
        Cleaned data
    filepath : str
        Output path
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"✓ Data saved to: {filepath}")


if __name__ == "__main__":
    print("=" * 70)
    print("VERSION 2: KAGGLE DATA INGESTION")
    print("=" * 70)
    
    # Load data
    df = load_kaggle_bp_data()
    
    # Display summary
    print("\n" + "=" * 70)
    print("DATA SUMMARY")
    print("=" * 70)
    print(df.describe())
    
    # Save data
    save_data(df)
    
    print("\n" + "=" * 70)
    print("✓ Kaggle data ingestion complete!")
    print("=" * 70)
    print("\nNOTE: This data is used for STATISTICS ONLY")
    print("      - NOT for training ML models")
    print("      - NOT for inferring drug effects")
    print("      - ONLY for grounding synthetic noise models")
