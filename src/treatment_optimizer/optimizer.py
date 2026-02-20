"""
Treatment Optimizer — Prescriptive Analytics Engine

Given a patient profile and a target blood pressure, this module finds
the optimal drug + dosage combination by searching the surrogate model's
prediction space.

This is the "inverse prediction" layer:
    Forward:  (Patient, Drug, Dose) → ΔBP
    Inverse:  (Patient, Target BP)  → Best (Drug, Dose)
"""

import sys
import os
import numpy as np

# Ensure project root is on path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# Drug catalog with human-readable names
DRUG_CATALOG = {
    'beta_blocker': {
        'names': ['Atenolol', 'Bisoprolol', 'Metoprolol'],
        'mechanism': 'Reduces cardiac output → lowers BP',
        'typical_effect': 'Decreases SBP by 10-15 mmHg at standard dose'
    },
    'vasodilator': {
        'names': ['Lisinopril', 'Amlodipine', 'Losartan'],
        'mechanism': 'Reduces peripheral resistance → lowers BP',
        'typical_effect': 'Decreases SBP by 12-20 mmHg at standard dose'
    },
    'stimulant': {
        'names': ['Adrenaline', 'Dobutamine'],
        'mechanism': 'Increases cardiac output → raises BP',
        'typical_effect': 'Increases SBP by 10-25 mmHg at standard dose'
    },
    'volume_expander': {
        'names': ['Saline IV', 'Dextran'],
        'mechanism': 'Increases arterial compliance → modulates BP',
        'typical_effect': 'Variable effect on BP depending on baseline'
    },
    'none': {
        'names': ['No Intervention'],
        'mechanism': 'Baseline (no treatment)',
        'typical_effect': 'No change'
    }
}


class TreatmentOptimizer:
    """
    Prescriptive analytics engine for cardiovascular digital twin.
    
    Uses the trained ML surrogate to perform fast grid search over
    all drug × dosage combinations and finds the optimal treatment
    to achieve a user-specified target blood pressure.
    """
    
    def __init__(self):
        """Load the trained surrogate model and encoders."""
        import joblib
        
        model_path = os.path.join(PROJECT_ROOT, 'twin_model', 'weights', 'surrogate_twin.pkl')
        encoders_path = os.path.join(PROJECT_ROOT, 'twin_model', 'weights', 'encoders.pkl')
        
        self.model = joblib.load(model_path)
        self.encoders = joblib.load(encoders_path)
        self.le_drug, self.le_risk = self.encoders
        
        # Dosage search grid (0.1 to 3.0 in steps of 0.1)
        self.dosage_grid = np.arange(0.1, 3.1, 0.1)
        
        # Drug classes to search (exclude 'none' from optimization)
        self.drug_classes = ['beta_blocker', 'vasodilator', 'stimulant', 'volume_expander']
    
    def _predict(self, profile, drug_class, dosage):
        """
        Make a single prediction using the surrogate model.
        
        Returns (delta_sbp, delta_dbp).
        """
        drug_encoded = self.le_drug.transform([drug_class])[0]
        risk_encoded = self.le_risk.transform([profile['risk_group']])[0]
        
        features = np.array([[
            profile['age'],
            profile['baseline_sbp'],
            profile['baseline_dbp'],
            profile['heart_rate'],
            risk_encoded,
            drug_encoded,
            dosage
        ]])
        
        prediction = self.model.predict(features)[0]
        return float(prediction[0]), float(prediction[1])
    
    def rank_treatments(self, patient_profile, target_sbp, target_dbp):
        """
        Evaluate ALL drug × dosage combinations and rank them by
        how close they get to the target BP.
        
        Parameters
        ----------
        patient_profile : dict
            Patient parameters (age, baseline_sbp, etc.)
        target_sbp : float
            Desired systolic blood pressure (mmHg)
        target_dbp : float
            Desired diastolic blood pressure (mmHg)
        
        Returns
        -------
        list of dict
            Sorted list of treatment options, best first.
            Each dict contains:
                - drug_class, drug_name, dosage
                - predicted_sbp, predicted_dbp
                - delta_sbp, delta_dbp
                - distance (error from target)
                - risk_level
        """
        baseline_sbp = patient_profile['baseline_sbp']
        baseline_dbp = patient_profile['baseline_dbp']
        
        # Desired change
        desired_delta_sbp = target_sbp - baseline_sbp
        desired_delta_dbp = target_dbp - baseline_dbp
        
        results = []
        
        for drug_class in self.drug_classes:
            drug_info = DRUG_CATALOG[drug_class]
            drug_name = drug_info['names'][0]  # Use primary name
            
            for dosage in self.dosage_grid:
                dosage = round(dosage, 1)
                
                # Predict
                delta_sbp, delta_dbp = self._predict(patient_profile, drug_class, dosage)
                
                # Predicted absolute BP
                predicted_sbp = baseline_sbp + delta_sbp
                predicted_dbp = baseline_dbp + delta_dbp
                
                # Distance from target (weighted: SBP matters more)
                distance = np.sqrt(
                    2.0 * (predicted_sbp - target_sbp) ** 2 +
                    1.0 * (predicted_dbp - target_dbp) ** 2
                )
                
                # Risk assessment
                if dosage > 2.0:
                    risk_level = "Caution: High Dose"
                elif predicted_sbp < 90:
                    risk_level = "Risk: Hypotension"
                elif predicted_sbp > 180:
                    risk_level = "Risk: Hypertension"
                elif abs(delta_sbp) > 40:
                    risk_level = "Caution: Large Change"
                else:
                    risk_level = "Safe"
                
                results.append({
                    'drug_class': drug_class,
                    'drug_name': drug_name,
                    'mechanism': drug_info['mechanism'],
                    'dosage': dosage,
                    'delta_sbp': delta_sbp,
                    'delta_dbp': delta_dbp,
                    'predicted_sbp': predicted_sbp,
                    'predicted_dbp': predicted_dbp,
                    'distance': distance,
                    'risk_level': risk_level
                })
        
        # Sort by distance (closest to target first)
        results.sort(key=lambda x: x['distance'])
        
        return results
    
    def optimize(self, patient_profile, target_sbp, target_dbp):
        """
        Find the single best treatment to achieve the target BP.
        
        Parameters
        ----------
        patient_profile : dict
            Patient parameters
        target_sbp : float
            Target systolic BP
        target_dbp : float
            Target diastolic BP
        
        Returns
        -------
        dict
            Best treatment recommendation with:
                - best: The optimal treatment
                - alternatives: Top 5 alternative treatments
                - baseline: Current patient BP
                - target: Desired BP
                - improvement: How much closer to target
        """
        all_treatments = self.rank_treatments(patient_profile, target_sbp, target_dbp)
        
        best = all_treatments[0]
        
        # Get top alternatives (different drug classes only)
        seen_classes = {best['drug_class']}
        alternatives = []
        for t in all_treatments[1:]:
            if t['drug_class'] not in seen_classes:
                alternatives.append(t)
                seen_classes.add(t['drug_class'])
            if len(alternatives) >= 4:
                break
        
        # Compute improvement
        current_distance = np.sqrt(
            2.0 * (patient_profile['baseline_sbp'] - target_sbp) ** 2 +
            1.0 * (patient_profile['baseline_dbp'] - target_dbp) ** 2
        )
        
        improvement_pct = ((current_distance - best['distance']) / current_distance * 100
                           if current_distance > 0 else 0)
        
        return {
            'best': best,
            'alternatives': alternatives,
            'baseline': {
                'sbp': patient_profile['baseline_sbp'],
                'dbp': patient_profile['baseline_dbp']
            },
            'target': {
                'sbp': target_sbp,
                'dbp': target_dbp
            },
            'improvement_pct': improvement_pct,
            'total_evaluated': len(all_treatments)
        }


if __name__ == "__main__":
    print("=" * 60)
    print("TREATMENT OPTIMIZER — SELF TEST")
    print("=" * 60)
    
    optimizer = TreatmentOptimizer()
    
    # Test Case: Hypertensive patient wants to reach 120/80
    profile = {
        'age': 60,
        'baseline_sbp': 155,
        'baseline_dbp': 95,
        'heart_rate': 80,
        'risk_group': 'high',
        'drug_class': 'none',
        'dosage': 0.0
    }
    
    target_sbp = 120
    target_dbp = 80
    
    print(f"\nPatient: Age {profile['age']}, BP {profile['baseline_sbp']}/{profile['baseline_dbp']}")
    print(f"Target:  BP {target_sbp}/{target_dbp}")
    print(f"Need:    ΔSBP = {target_sbp - profile['baseline_sbp']:+.0f}, ΔDBP = {target_dbp - profile['baseline_dbp']:+.0f}")
    
    result = optimizer.optimize(profile, target_sbp, target_dbp)
    
    best = result['best']
    print(f"\n{'='*60}")
    print(f"🎯 RECOMMENDED TREATMENT")
    print(f"{'='*60}")
    print(f"  Drug:      {best['drug_name']} ({best['drug_class']})")
    print(f"  Dosage:    {best['dosage']:.1f}x")
    print(f"  Predicted: {best['predicted_sbp']:.0f}/{best['predicted_dbp']:.0f} mmHg")
    print(f"  Change:    ΔSBP={best['delta_sbp']:+.1f}, ΔDBP={best['delta_dbp']:+.1f}")
    print(f"  Risk:      {best['risk_level']}")
    print(f"  Accuracy:  {result['improvement_pct']:.1f}% closer to target")
    
    print(f"\n{'='*60}")
    print(f"📋 ALTERNATIVES")
    print(f"{'='*60}")
    for i, alt in enumerate(result['alternatives'], 1):
        print(f"  {i}. {alt['drug_name']} @ {alt['dosage']:.1f}x → "
              f"{alt['predicted_sbp']:.0f}/{alt['predicted_dbp']:.0f} "
              f"({alt['risk_level']})")
    
    print(f"\n  Total combinations evaluated: {result['total_evaluated']}")
    print(f"\n{'='*60}")
    print("✓ Optimizer test complete!")
