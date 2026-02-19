"""
Uncertainty Estimation for Real-World Deployment

This module quantifies prediction confidence when the digital twin is applied
outside its synthetic training distribution.

REAL-WORLD DEPLOYMENT RATIONALE:
================================
Uncertainty estimation is CRITICAL for safe deployment because:
1. Real-world data differs from synthetic training data
2. Model confidence varies across input space
3. Out-of-distribution inputs require flagging
4. Clinical decisions need confidence bounds

This module provides:
- Prediction uncertainty estimation
- Out-of-distribution detection
- Confidence intervals for predictions
"""

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import joblib


def estimate_uncertainty_bootstrap(model, input_sample, n_bootstrap=100):
    """
    Estimate prediction uncertainty using bootstrap sampling.
    
    This method generates multiple predictions by perturbing the input
    and computes the variance as a measure of uncertainty.
    
    Parameters
    ----------
    model : trained model
        Digital twin model
    input_sample : array-like
        Input features (single sample)
    n_bootstrap : int, optional
        Number of bootstrap samples (default: 100)
    
    Returns
    -------
    dict
        Uncertainty estimates:
        - 'mean_pred': Mean prediction
        - 'std_pred': Standard deviation (uncertainty)
        - 'ci_lower': Lower 95% confidence interval
        - 'ci_upper': Upper 95% confidence interval
    
    Examples
    --------
    >>> uncertainty = estimate_uncertainty_bootstrap(model, patient_features)
    >>> print(f"Prediction: {uncertainty['mean_pred']} ± {uncertainty['std_pred']}")
    
    Notes
    -----
    Higher std_pred indicates higher uncertainty.
    Use this to flag predictions that need clinical review.
    """
    # Add small noise to input for bootstrap
    input_array = np.array(input_sample).reshape(1, -1)
    
    predictions = []
    for _ in range(n_bootstrap):
        # Add Gaussian noise (small perturbation)
        noise = np.random.normal(0, 0.01, input_array.shape)
        perturbed_input = input_array + noise
        
        # Predict
        pred = model.predict(perturbed_input)[0]
        predictions.append(pred)
    
    predictions = np.array(predictions)
    
    # Compute statistics
    mean_pred = np.mean(predictions, axis=0)
    std_pred = np.std(predictions, axis=0)
    
    # 95% confidence intervals
    ci_lower = np.percentile(predictions, 2.5, axis=0)
    ci_upper = np.percentile(predictions, 97.5, axis=0)
    
    uncertainty = {
        'mean_pred': mean_pred,
        'std_pred': std_pred,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'uncertainty_score': float(np.mean(std_pred))  # Overall uncertainty
    }
    
    return uncertainty


def flag_out_of_distribution(input_sample, training_stats, threshold=3.0):
    """
    Flag inputs that are out-of-distribution (OOD).
    
    This function detects when input features are significantly different
    from the training distribution, indicating the model may not be reliable.
    
    Parameters
    ----------
    input_sample : dict
        Input features
    training_stats : dict
        Training data statistics (mean, std for each feature)
    threshold : float, optional
        Z-score threshold for OOD detection (default: 3.0)
    
    Returns
    -------
    dict
        OOD detection results:
        - 'is_ood': bool (True if out-of-distribution)
        - 'ood_features': list of features that are OOD
        - 'z_scores': dict of z-scores for each feature
    
    Examples
    --------
    >>> stats = {'age': {'mean': 50, 'std': 15}, ...}
    >>> patient = {'age': 95, 'baseline_sbp': 140, ...}
    >>> ood_result = flag_out_of_distribution(patient, stats)
    >>> if ood_result['is_ood']:
    ...     print("WARNING: Patient is out-of-distribution!")
    
    Notes
    -----
    OOD inputs should trigger:
    1. Clinical review before using prediction
    2. Model recalibration consideration
    3. Uncertainty quantification
    """
    z_scores = {}
    ood_features = []
    
    for feature, value in input_sample.items():
        if feature in training_stats:
            mean = training_stats[feature]['mean']
            std = training_stats[feature]['std']
            
            # Compute z-score
            z_score = abs((value - mean) / std) if std > 0 else 0
            z_scores[feature] = z_score
            
            # Flag if beyond threshold
            if z_score > threshold:
                ood_features.append(feature)
    
    is_ood = len(ood_features) > 0
    
    ood_result = {
        'is_ood': is_ood,
        'ood_features': ood_features,
        'z_scores': z_scores,
        'max_z_score': max(z_scores.values()) if z_scores else 0
    }
    
    return ood_result


def get_prediction_confidence(uncertainty_score):
    """
    Convert uncertainty score to confidence level.
    
    Parameters
    ----------
    uncertainty_score : float
        Uncertainty score from estimate_uncertainty_bootstrap()
    
    Returns
    -------
    str
        Confidence level: 'high', 'medium', 'low'
    
    Examples
    --------
    >>> confidence = get_prediction_confidence(0.5)
    >>> print(confidence)  # 'high'
    """
    if uncertainty_score < 1.0:
        return 'high'
    elif uncertainty_score < 3.0:
        return 'medium'
    else:
        return 'low'


# ============================================================================
# REAL-WORLD DEPLOYMENT GUIDE
# ============================================================================
"""
HOW UNCERTAINTY GUIDES SAFE REAL-WORLD USAGE:
=============================================

CRITICAL PRINCIPLE:
------------------
NEVER deploy a predictive model without uncertainty quantification.

DEPLOYMENT WORKFLOW:
-------------------

STEP 1: Estimate Prediction Uncertainty
---------------------------------------
```python
from real_world.uncertainty import estimate_uncertainty_bootstrap

# Get prediction with uncertainty
uncertainty = estimate_uncertainty_bootstrap(model, patient_features)

print(f"Predicted Δ SBP: {uncertainty['mean_pred'][0]:.1f} mmHg")
print(f"Uncertainty: ± {uncertainty['std_pred'][0]:.1f} mmHg")
print(f"95% CI: [{uncertainty['ci_lower'][0]:.1f}, {uncertainty['ci_upper'][0]:.1f}]")
```

STEP 2: Check for Out-of-Distribution Inputs
--------------------------------------------
```python
from real_world.uncertainty import flag_out_of_distribution

# Load training statistics
training_stats = {
    'age': {'mean': 50, 'std': 15},
    'baseline_sbp': {'mean': 130, 'std': 18},
    # ... other features
}

# Check if patient is OOD
ood_result = flag_out_of_distribution(patient_features, training_stats)

if ood_result['is_ood']:
    print(f"⚠️ WARNING: Patient is out-of-distribution!")
    print(f"   OOD features: {ood_result['ood_features']}")
    print(f"   → Prediction may be unreliable")
    print(f"   → Recommend clinical review")
```

STEP 3: Make Decision Based on Confidence
-----------------------------------------
```python
from real_world.uncertainty import get_prediction_confidence

confidence = get_prediction_confidence(uncertainty['uncertainty_score'])

if confidence == 'high':
    print("✓ High confidence - prediction is reliable")
elif confidence == 'medium':
    print("⚠️ Medium confidence - use with caution")
else:
    print("❌ Low confidence - do NOT use without clinical review")
```

CLINICAL DECISION RULES:
-----------------------
1. High Confidence + In-Distribution → Use prediction
2. Medium Confidence → Flag for review
3. Low Confidence OR Out-of-Distribution → Require clinical validation
4. ALWAYS present uncertainty to clinicians

CRITICAL NOTES:
===============
1. Uncertainty is NOT optional - it's mandatory for safety
2. OOD detection prevents dangerous extrapolation
3. Confidence levels guide appropriate use
4. Always err on the side of caution
5. Document all uncertainty-based decisions
"""


if __name__ == "__main__":
    print("=" * 70)
    print("UNCERTAINTY ESTIMATION - DEMO")
    print("=" * 70)
    
    # Demo 1: Uncertainty estimation (simulated)
    print("\nDemo 1: Prediction Uncertainty Estimation")
    print("-" * 70)
    
    # Simulate a simple model for demo
    class DummyModel:
        def predict(self, X):
            # Simulate prediction with some noise
            return np.array([[-5.0 + np.random.normal(0, 0.5), 
                             -3.5 + np.random.normal(0, 0.3)]])
    
    model = DummyModel()
    patient_features = [65, 145, 90, 75, 1, 0, 1.0]  # Example features
    
    uncertainty = estimate_uncertainty_bootstrap(model, patient_features, n_bootstrap=50)
    
    print(f"Predicted Δ SBP: {uncertainty['mean_pred'][0]:.2f} mmHg")
    print(f"Uncertainty (std): ± {uncertainty['std_pred'][0]:.2f} mmHg")
    print(f"95% CI: [{uncertainty['ci_lower'][0]:.2f}, {uncertainty['ci_upper'][0]:.2f}]")
    print(f"Overall Uncertainty Score: {uncertainty['uncertainty_score']:.2f}")
    
    confidence = get_prediction_confidence(uncertainty['uncertainty_score'])
    print(f"Confidence Level: {confidence.upper()}")
    
    # Demo 2: Out-of-distribution detection
    print("\n\nDemo 2: Out-of-Distribution Detection")
    print("-" * 70)
    
    training_stats = {
        'age': {'mean': 50, 'std': 15},
        'baseline_sbp': {'mean': 130, 'std': 18},
        'baseline_dbp': {'mean': 82, 'std': 12},
        'heart_rate': {'mean': 72, 'std': 10}
    }
    
    # Test case 1: Normal patient (in-distribution)
    normal_patient = {
        'age': 55,
        'baseline_sbp': 135,
        'baseline_dbp': 85,
        'heart_rate': 70
    }
    
    ood_normal = flag_out_of_distribution(normal_patient, training_stats)
    print(f"Normal Patient:")
    print(f"  Is OOD: {ood_normal['is_ood']}")
    print(f"  Max Z-score: {ood_normal['max_z_score']:.2f}")
    print(f"  ✓ Safe to use prediction")
    
    # Test case 2: Extreme patient (out-of-distribution)
    extreme_patient = {
        'age': 95,  # Very old
        'baseline_sbp': 180,  # Very high
        'baseline_dbp': 110,  # Very high
        'heart_rate': 120  # Very high
    }
    
    ood_extreme = flag_out_of_distribution(extreme_patient, training_stats, threshold=3.0)
    print(f"\nExtreme Patient:")
    print(f"  Is OOD: {ood_extreme['is_ood']}")
    print(f"  OOD Features: {ood_extreme['ood_features']}")
    print(f"  Max Z-score: {ood_extreme['max_z_score']:.2f}")
    print(f"  ⚠️ WARNING: Out-of-distribution - prediction may be unreliable!")
    
    print("\n" + "=" * 70)
    print("✓ Uncertainty estimation enables safe real-world deployment!")
    print("=" * 70)
