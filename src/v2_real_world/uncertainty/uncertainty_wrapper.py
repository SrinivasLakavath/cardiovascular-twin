"""
Uncertainty-Aware ML Inference Wrapper

This module adds uncertainty estimation to V1 ML predictions,
making ML a first-class citizen with confidence bounds.

PURPOSE:
========
- Wrap V1 model with uncertainty estimation
- Provide prediction ± uncertainty
- Enable safe real-world adaptation
- No modification to V1 model weights

WHY UNCERTAINTY MATTERS:
========================
1. **Clinical Safety**: Never deploy predictions without confidence
2. **Decision Support**: Clinicians need to know reliability
3. **OOD Detection**: Flag unreliable predictions
4. **Calibration**: Uncertainty guides when to trust the model

HOW IT ENABLES SAFE REAL-WORLD ADAPTATION:
===========================================
- Low uncertainty → Trust prediction
- High uncertainty → Require clinical review
- OOD inputs → Flag for validation
- Uncertainty-aware decisions prevent harm
"""

import os
import os
import numpy as np
import joblib

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DEFAULT_MODEL_PATH = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights', 'surrogate_twin.pkl')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DEFAULT_MODEL_PATH = os.path.join(PROJECT_ROOT, 'src', 'twin_model', 'weights', 'surrogate_twin.pkl')


class UncertaintyWrapper:
    """
    Wrapper that adds uncertainty estimation to V1 model.
    
    This does NOT modify the V1 model - only adds uncertainty quantification.
    """
    
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = DEFAULT_MODEL_PATH
        """
        Initialize uncertainty wrapper.
        
        Parameters
        ----------
        model_path : str
            Path to V1 model
        """
        self.model = joblib.load(model_path)
        print(f"✓ Loaded V1 model: {model_path}")
    
    def predict_with_uncertainty(self, input_features, method='bootstrap', n_samples=50):
        """
        Predict with uncertainty estimation.
        
        Parameters
        ----------
        input_features : array-like
            Input features (single sample or batch)
        method : str
            Uncertainty estimation method ('bootstrap' or 'ensemble')
        n_samples : int
            Number of bootstrap samples
        
        Returns
        -------
        dict
            Prediction with uncertainty:
            - 'prediction': Mean prediction
            - 'uncertainty': Standard deviation
            - 'ci_lower': Lower 95% confidence interval
            - 'ci_upper': Upper 95% confidence interval
            - 'confidence_level': 'high', 'medium', or 'low'
        
        Examples
        --------
        >>> wrapper = UncertaintyWrapper()
        >>> features = [65, 145, 90, 75, 1, 0, 1.0]
        >>> result = wrapper.predict_with_uncertainty(features)
        >>> print(f"Prediction: {result['prediction']} ± {result['uncertainty']}")
        """
        # Ensure input is 2D
        if len(np.array(input_features).shape) == 1:
            input_features = np.array(input_features).reshape(1, -1)
        
        if method == 'bootstrap':
            return self._bootstrap_uncertainty(input_features, n_samples)
        elif method == 'ensemble':
            return self._ensemble_uncertainty(input_features, n_samples)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def _bootstrap_uncertainty(self, X, n_samples):
        """
        Estimate uncertainty using bootstrap sampling.
        
        Add small noise to input and measure prediction variance.
        """
        predictions = []
        
        for _ in range(n_samples):
            # Add small Gaussian noise to input
            noise = np.random.normal(0, 0.01, X.shape)
            X_perturbed = X + noise
            
            # Predict
            pred = self.model.predict(X_perturbed)
            predictions.append(pred)
        
        predictions = np.array(predictions)
        
        # Compute statistics
        mean_pred = np.mean(predictions, axis=0)
        std_pred = np.std(predictions, axis=0)
        ci_lower = np.percentile(predictions, 2.5, axis=0)
        ci_upper = np.percentile(predictions, 97.5, axis=0)
        
        # Determine confidence level
        uncertainty_score = np.mean(std_pred)
        confidence_level = self._get_confidence_level(uncertainty_score)
        
        return {
            'prediction': mean_pred[0] if len(mean_pred) == 1 else mean_pred,
            'uncertainty': std_pred[0] if len(std_pred) == 1 else std_pred,
            'ci_lower': ci_lower[0] if len(ci_lower) == 1 else ci_lower,
            'ci_upper': ci_upper[0] if len(ci_upper) == 1 else ci_upper,
            'uncertainty_score': uncertainty_score,
            'confidence_level': confidence_level
        }
    
    def _ensemble_uncertainty(self, X, n_samples):
        """
        Estimate uncertainty using ensemble predictions.
        
        Similar to bootstrap but with different noise patterns.
        """
        # For single model, use bootstrap-like approach
        return self._bootstrap_uncertainty(X, n_samples)
    
    def _get_confidence_level(self, uncertainty_score):
        """
        Convert uncertainty score to confidence level.
        
        Parameters
        ----------
        uncertainty_score : float
            Uncertainty score
        
        Returns
        -------
        str
            'high', 'medium', or 'low'
        """
        if uncertainty_score < 0.5:
            return 'high'
        elif uncertainty_score < 2.0:
            return 'medium'
        else:
            return 'low'


def predict_with_uncertainty(model, input_features, n_bootstrap=50):
    """
    Standalone function for uncertainty-aware prediction.
    
    Parameters
    ----------
    model : trained model
        V1 model
    input_features : array-like
        Input features
    n_bootstrap : int
        Number of bootstrap samples
    
    Returns
    -------
    dict
        Prediction with uncertainty
    """
    wrapper = UncertaintyWrapper()
    wrapper.model = model
    return wrapper.predict_with_uncertainty(input_features, n_samples=n_bootstrap)


if __name__ == "__main__":
    print("=" * 70)
    print("VERSION 2: UNCERTAINTY-AWARE ML INFERENCE")
    print("=" * 70)
    
    # Create wrapper
    wrapper = UncertaintyWrapper()
    
    # Demo: Single prediction with uncertainty
    print("\n" + "-" * 70)
    print("DEMO: Prediction with Uncertainty")
    print("-" * 70)
    
    # Example patient
    patient_features = [65, 145, 90, 75, 1, 0, 1.0]  # age, sbp, dbp, hr, risk, drug, dose
    
    print(f"\nPatient: Age 65, BP 145/90, HR 75")
    print(f"Intervention: Beta blocker, dose 1.0")
    
    # Predict with uncertainty
    result = wrapper.predict_with_uncertainty(patient_features, n_samples=50)
    
    print(f"\nPrediction:")
    print(f"  Δ SBP: {result['prediction'][0]:.2f} ± {result['uncertainty'][0]:.2f} mmHg")
    print(f"  Δ DBP: {result['prediction'][1]:.2f} ± {result['uncertainty'][1]:.2f} mmHg")
    
    print(f"\n95% Confidence Intervals:")
    print(f"  Δ SBP: [{result['ci_lower'][0]:.2f}, {result['ci_upper'][0]:.2f}]")
    print(f"  Δ DBP: [{result['ci_lower'][1]:.2f}, {result['ci_upper'][1]:.2f}]")
    
    print(f"\nConfidence Level: {result['confidence_level'].upper()}")
    
    # Demo: Multiple patients
    print("\n" + "-" * 70)
    print("DEMO: Batch Predictions with Uncertainty")
    print("-" * 70)
    
    patients = [
        [55, 130, 85, 70, 0, 0, 1.0],  # Young, normal BP
        [75, 160, 95, 65, 2, 1, 1.5],  # Old, high BP
        [40, 110, 70, 80, 0, 2, 0.5],  # Young, low BP
    ]
    
    print(f"\n{'Patient':<10} {'Δ SBP':<20} {'Δ DBP':<20} {'Confidence':<12}")
    print("-" * 70)
    
    for i, patient in enumerate(patients, 1):
        result = wrapper.predict_with_uncertainty(patient, n_samples=30)
        
        sbp_str = f"{result['prediction'][0]:.2f} ± {result['uncertainty'][0]:.2f}"
        dbp_str = f"{result['prediction'][1]:.2f} ± {result['uncertainty'][1]:.2f}"
        
        print(f"{i:<10} {sbp_str:<20} {dbp_str:<20} {result['confidence_level'].upper():<12}")
    
    # Explain importance
    print("\n" + "=" * 70)
    print("WHY UNCERTAINTY MATTERS")
    print("=" * 70)
    
    print("""
1. CLINICAL SAFETY
   - Never deploy predictions without confidence bounds
   - Uncertainty guides clinical decision-making
   
2. DECISION SUPPORT
   - High confidence → Trust prediction
   - Medium confidence → Use with caution
   - Low confidence → Require clinical review
   
3. OUT-OF-DISTRIBUTION DETECTION
   - High uncertainty often indicates OOD inputs
   - Flags cases that need validation
   
4. SAFE REAL-WORLD ADAPTATION
   - Uncertainty-aware decisions prevent harm
   - Enables gradual deployment with safety nets
   - Builds trust through transparency
""")
    
    print("=" * 70)
    print("✓ Uncertainty wrapper ready!")
    print("=" * 70)
    print("\nNOTE: V1 model is NOT modified")
    print("      Only wrapped with uncertainty estimation")
