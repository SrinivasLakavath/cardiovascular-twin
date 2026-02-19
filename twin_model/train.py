"""
ML Surrogate Digital Twin - Training Pipeline

Trains the surrogate digital twin model on synthetic cardiovascular data.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor


def prepare_data(csv_path='data/raw/synthetic_dataset.csv'):
    """
    Load and prepare data for training.
    
    Parameters
    ----------
    csv_path : str
        Path to the synthetic dataset CSV
    
    Returns
    -------
    X_train, X_test, y_train, y_test, feature_names, label_encoder
    """
    print("Loading dataset...")
    df = pd.read_csv(csv_path)
    print(f"  Dataset shape: {df.shape}")
    
    # Encode categorical variables
    print("\nEncoding categorical variables...")
    le_drug = LabelEncoder()
    le_risk = LabelEncoder()
    
    df['drug_class_encoded'] = le_drug.fit_transform(df['drug_class'])
    df['risk_group_encoded'] = le_risk.fit_transform(df['risk_group'])
    
    # Select features
    feature_cols = [
        'age',
        'baseline_sbp',
        'baseline_dbp',
        'heart_rate',
        'risk_group_encoded',
        'drug_class_encoded',
        'dosage'
    ]
    
    target_cols = ['delta_sbp', 'delta_dbp']
    
    X = df[feature_cols].values
    y = df[target_cols].values
    
    print(f"  Features: {feature_cols}")
    print(f"  Targets: {target_cols}")
    print(f"  X shape: {X.shape}")
    print(f"  y shape: {y.shape}")
    
    # Train-test split
    print("\nSplitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"  Train: {X_train.shape[0]} samples")
    print(f"  Test: {X_test.shape[0]} samples")
    
    return X_train, X_test, y_train, y_test, feature_cols, (le_drug, le_risk)


def train_model(X_train, y_train):
    """
    Train the surrogate twin model.
    
    Parameters
    ----------
    X_train : array-like
        Training features
    y_train : array-like
        Training targets
    
    Returns
    -------
    MultiOutputRegressor
        Trained model
    """
    print("\nTraining Surrogate Twin Model...")
    print("-" * 50)
    
    # Create model using sklearn directly (no custom class)
    base_estimator = GradientBoostingRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    
    model = MultiOutputRegressor(base_estimator)
    
    # Train
    print("Fitting model...")
    model.fit(X_train, y_train)
    
    print("✓ Training complete!")
    
    return model


def main():
    """Main training pipeline."""
    print("=" * 50)
    print("SURROGATE DIGITAL TWIN - TRAINING PIPELINE")
    print("=" * 50)
    
    # Prepare data
    X_train, X_test, y_train, y_test, feature_names, encoders = prepare_data()
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Save model
    print("\nSaving model...")
    import joblib
    os.makedirs('twin_model/weights', exist_ok=True)
    joblib.dump(model, 'twin_model/weights/surrogate_twin.pkl')
    print("Model saved to: twin_model/weights/surrogate_twin.pkl")
    
    # Save encoders
    joblib.dump(encoders, 'twin_model/weights/encoders.pkl')
    print("Encoders saved to: twin_model/weights/encoders.pkl")
    
    # Save feature names
    joblib.dump(feature_names, 'twin_model/weights/feature_names.pkl')
    print("Feature names saved to: twin_model/weights/feature_names.pkl")
    
    # Quick evaluation on test set
    print("\n" + "=" * 50)
    print("Quick Test Set Evaluation:")
    print("=" * 50)
    
    y_pred = model.predict(X_test)
    
    # Compute MAE for each output
    mae_sbp = np.mean(np.abs(y_test[:, 0] - y_pred[:, 0]))
    mae_dbp = np.mean(np.abs(y_test[:, 1] - y_pred[:, 1]))
    
    print(f"MAE (delta_sbp): {mae_sbp:.4f} mmHg")
    print(f"MAE (delta_dbp): {mae_dbp:.4f} mmHg")
    
    # Show sample predictions
    print("\nSample Predictions (first 5):")
    print("  Actual delta_sbp | Predicted delta_sbp | Actual delta_dbp | Predicted delta_dbp")
    print("-" * 80)
    for i in range(min(5, len(y_test))):
        print(f"  {y_test[i, 0]:15.2f} | {y_pred[i, 0]:19.2f} | {y_test[i, 1]:16.2f} | {y_pred[i, 1]:23.2f}")
    
    print("\n" + "=" * 50)
    print("✓ Training pipeline complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
