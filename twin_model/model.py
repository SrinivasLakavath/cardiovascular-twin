"""
ML Surrogate Digital Twin - Model Architecture

This module defines the machine learning model that acts as the digital twin.
The model learns to predict cardiovascular responses from patient characteristics
and interventions.
"""

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
import joblib
import numpy as np


class SurrogateTwin:
    """
    Surrogate Digital Twin for cardiovascular response prediction.
    
    This model predicts changes in blood pressure (delta_sbp, delta_dbp)
    given patient characteristics and intervention details.
    
    The model uses Gradient Boosting for robustness and interpretability.
    """
    
    def __init__(self, n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42):
        """
        Initialize the Surrogate Twin model.
        
        Parameters
        ----------
        n_estimators : int, optional
            Number of boosting stages (default: 100)
        max_depth : int, optional
            Maximum depth of trees (default: 5)
        learning_rate : float, optional
            Learning rate for boosting (default: 0.1)
        random_state : int, optional
            Random seed for reproducibility (default: 42)
        """
        # Create base estimator
        base_estimator = GradientBoostingRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=random_state,
            verbose=0
        )
        
        # Wrap in MultiOutputRegressor for predicting both delta_sbp and delta_dbp
        self.model = MultiOutputRegressor(base_estimator)
        self.feature_names = None
        self.is_fitted = False
    
    def fit(self, X, y):
        """
        Train the surrogate twin model.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training features
        y : array-like, shape (n_samples, 2)
            Target values [delta_sbp, delta_dbp]
        
        Returns
        -------
        self
            Fitted model
        """
        self.model.fit(X, y)
        self.is_fitted = True
        return self
    
    def predict(self, X):
        """
        Predict cardiovascular responses.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input features
        
        Returns
        -------
        array-like, shape (n_samples, 2)
            Predicted [delta_sbp, delta_dbp]
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        return self.model.predict(X)
    
    def save(self, filepath):
        """
        Save the trained model to disk.
        
        Parameters
        ----------
        filepath : str
            Path to save the model
        """
        if not self.is_fitted:
            raise ValueError("Cannot save unfitted model")
        
        joblib.dump(self, filepath)
        print(f"Model saved to: {filepath}")
    
    @staticmethod
    def load(filepath):
        """
        Load a trained model from disk.
        
        Parameters
        ----------
        filepath : str
            Path to the saved model
        
        Returns
        -------
        SurrogateTwin
            Loaded model
        """
        model = joblib.load(filepath)
        print(f"Model loaded from: {filepath}")
        return model


if __name__ == "__main__":
    # Quick test of model architecture
    print("Testing Surrogate Twin Model Architecture...")
    print("-" * 50)
    
    # Create dummy data
    np.random.seed(42)
    X_train = np.random.randn(100, 7)  # 7 features
    y_train = np.random.randn(100, 2)  # 2 outputs
    
    # Create and train model
    print("\nCreating model...")
    model = SurrogateTwin(n_estimators=10, max_depth=3)
    
    print("Training model...")
    model.fit(X_train, y_train)
    
    print("Making predictions...")
    X_test = np.random.randn(10, 7)
    predictions = model.predict(X_test)
    
    print(f"\nPredictions shape: {predictions.shape}")
    print(f"Sample predictions:\n{predictions[:3]}")
    
    print("\n" + "=" * 50)
    print("✓ Model architecture test passed!")
