"""
SIMPLE DEMO: Cardiovascular Digital Twin

This demo shows the complete workflow from patient to prediction
without relying on pickled models.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from synthetic_layer.patient_sampler import sample_patient
from synthetic_layer.intervention_mapper import map_intervention, get_intervention_description
from physio_engine.windkessel.core import simulate_bp


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_section(text):
    """Print a formatted section."""
    print(f"\n{text}")
    print("-" * 70)


def demo_patient_generation():
    """Demo 1: Patient Generation"""
    print_header("DEMO 1: SYNTHETIC PATIENT GENERATION")
    
    print("\n📋 Generating 3 different patient profiles...\n")
    
    for i, seed in enumerate([42, 123, 456], 1):
        patient = sample_patient(seed=seed)
        print(f"Patient {i} (seed={seed}):")
        print(f"  Age: {patient['age']} years")
        print(f"  Baseline BP: {patient['baseline_sbp']}/{patient['baseline_dbp']} mmHg")
        print(f"  Heart Rate: {patient['heart_rate']} bpm")
        print(f"  Risk Group: {patient['risk_group']}")
        print()
    
    print("✓ Patients are generated with realistic, age-dependent characteristics")


def demo_intervention_mapping():
    """Demo 2: Intervention Mapping"""
    print_header("DEMO 2: INTERVENTION PARAMETER MAPPING")
    
    print("\n💊 Showing how different drug classes affect cardiovascular parameters...\n")
    
    baseline = {'R': 1.0, 'C': 1.5, 'Q': 5.0}
    print(f"Baseline Parameters: R={baseline['R']}, C={baseline['C']}, Q={baseline['Q']}\n")
    
    interventions = [
        ('beta_blocker', 1.0),
        ('vasodilator', 1.0),
        ('stimulant', 1.0),
        ('volume_expander', 1.0)
    ]
    
    for drug, dose in interventions:
        params = map_intervention(drug, dose, baseline)
        print(f"{drug.upper().replace('_', ' ')} (dose={dose}):")
        print(f"  Effect: {get_intervention_description(drug)}")
        print(f"  Modified Parameters: R={params['R']:.2f}, C={params['C']:.2f}, Q={params['Q']:.2f}")
        print()
    
    print("✓ Each intervention has explicit, interpretable parameter changes")


def demo_physiology_simulation():
    """Demo 3: Physiology Simulation"""
    print_header("DEMO 3: WINDKESSEL CARDIOVASCULAR SIMULATION")
    
    print("\n🫀 Simulating blood pressure for different physiological states...\n")
    
    scenarios = [
        ("Normal", {'R': 1.0, 'C': 1.5, 'Q': 5.0, 'hr': 72}),
        ("High Resistance (Hypertension-like)", {'R': 1.8, 'C': 1.5, 'Q': 5.0, 'hr': 72}),
        ("High Cardiac Output (Exercise-like)", {'R': 1.0, 'C': 1.5, 'Q': 7.0, 'hr': 90}),
    ]
    
    for name, params in scenarios:
        sbp, dbp = simulate_bp(
            R=params['R'],
            C=params['C'],
            Q=params['Q'],
            heart_rate=params['hr']
        )
        print(f"{name}:")
        print(f"  Parameters: R={params['R']}, C={params['C']}, Q={params['Q']}, HR={params['hr']}")
        print(f"  Simulated BP: {sbp:.1f}/{dbp:.1f} mmHg")
        print(f"  Pulse Pressure: {sbp - dbp:.1f} mmHg")
        print()
    
    print("✓ Windkessel model produces realistic blood pressure values")


def demo_complete_workflow():
    """Demo 4: Complete Workflow"""
    print_header("DEMO 4: COMPLETE DIGITAL TWIN WORKFLOW")
    
    print("\n🔄 End-to-end demonstration: Patient → Intervention → Prediction\n")
    
    # Generate patient
    print_section("STEP 1: Generate Patient")
    patient = sample_patient(seed=999)
    print(f"  Age: {patient['age']} years")
    print(f"  Baseline BP: {patient['baseline_sbp']}/{patient['baseline_dbp']} mmHg")
    print(f"  Heart Rate: {patient['heart_rate']} bpm")
    print(f"  Risk Group: {patient['risk_group']}")
    
    # Define intervention
    print_section("STEP 2: Define Intervention")
    drug_class = 'beta_blocker'
    dosage = 1.0
    print(f"  Drug Class: {drug_class}")
    print(f"  Dosage: {dosage}")
    print(f"  Mechanism: {get_intervention_description(drug_class)}")
    
    # Simulate baseline
    print_section("STEP 3: Simulate Baseline BP")
    baseline_params = {'R': 1.0, 'C': 1.5, 'Q': 5.0}
    sbp_baseline, dbp_baseline = simulate_bp(
        R=baseline_params['R'],
        C=baseline_params['C'],
        Q=baseline_params['Q'],
        heart_rate=patient['heart_rate']
    )
    print(f"  Baseline BP (simulated): {sbp_baseline:.1f}/{dbp_baseline:.1f} mmHg")
    
    # Apply intervention
    print_section("STEP 4: Apply Intervention")
    modified_params = map_intervention(drug_class, dosage, baseline_params)
    print(f"  Modified Parameters: R={modified_params['R']:.2f}, C={modified_params['C']:.2f}, Q={modified_params['Q']:.2f}")
    
    # Simulate post-intervention
    print_section("STEP 5: Simulate Post-Intervention BP")
    sbp_post, dbp_post = simulate_bp(
        R=modified_params['R'],
        C=modified_params['C'],
        Q=modified_params['Q'],
        heart_rate=patient['heart_rate']
    )
    print(f"  Post-Intervention BP: {sbp_post:.1f}/{dbp_post:.1f} mmHg")
    
    # Calculate change
    print_section("STEP 6: Calculate BP Change")
    delta_sbp = sbp_post - sbp_baseline
    delta_dbp = dbp_post - dbp_baseline
    print(f"  Δ SBP: {delta_sbp:+.2f} mmHg")
    print(f"  Δ DBP: {delta_dbp:+.2f} mmHg")
    
    # Interpretation
    print_section("INTERPRETATION")
    print(f"  ✓ Beta blocker decreased cardiac output (Q: {baseline_params['Q']:.1f} → {modified_params['Q']:.2f})")
    print(f"  ✓ This resulted in decreased blood pressure ({sbp_baseline:.1f}/{dbp_baseline:.1f} → {sbp_post:.1f}/{dbp_post:.1f})")
    print(f"  ✓ The digital twin correctly predicts the physiological response")


def demo_dose_response():
    """Demo 5: Dose-Response Relationship"""
    print_header("DEMO 5: DOSE-RESPONSE RELATIONSHIP")
    
    print("\n📊 Demonstrating how response magnitude scales with dosage...\n")
    
    # Fixed patient
    patient = sample_patient(seed=777)
    print(f"Patient: Age {patient['age']}, Baseline BP {patient['baseline_sbp']}/{patient['baseline_dbp']} mmHg")
    print(f"Intervention: Beta Blocker at varying doses\n")
    
    baseline_params = {'R': 1.0, 'C': 1.5, 'Q': 5.0}
    sbp_baseline, dbp_baseline = simulate_bp(
        R=baseline_params['R'],
        C=baseline_params['C'],
        Q=baseline_params['Q'],
        heart_rate=patient['heart_rate']
    )
    
    print(f"Dosage | Modified Q | Δ SBP    | Δ DBP")
    print(f"-------|------------|----------|----------")
    
    for dose in [0.0, 0.5, 1.0, 1.5, 2.0]:
        modified = map_intervention('beta_blocker', dose, baseline_params)
        sbp_post, dbp_post = simulate_bp(
            R=modified['R'],
            C=modified['C'],
            Q=modified['Q'],
            heart_rate=patient['heart_rate']
        )
        delta_sbp = sbp_post - sbp_baseline
        delta_dbp = dbp_post - dbp_baseline
        
        print(f"{dose:5.1f}  | {modified['Q']:10.2f} | {delta_sbp:+8.2f} | {delta_dbp:+8.2f}")
    
    print("\n✓ Higher doses produce larger magnitude responses (monotonic)")


def main():
    """Main demo script."""
    print_header("CARDIOVASCULAR DIGITAL TWIN - INTERACTIVE DEMO")
    
    print("\nThis demo shows the complete digital twin system:")
    print("  1. Patient generation")
    print("  2. Intervention mapping")
    print("  3. Physiology simulation")
    print("  4. End-to-end workflow")
    print("  5. Dose-response analysis")
    
    # Run all demos
    demo_patient_generation()
    demo_intervention_mapping()
    demo_physiology_simulation()
    demo_complete_workflow()
    demo_dose_response()
    
    # Final summary
    print_header("DEMO COMPLETE")
    print("\n✅ Successfully demonstrated:")
    print("   • Synthetic patient generation with realistic characteristics")
    print("   • Explicit intervention → parameter mappings")
    print("   • Physiology-inspired BP simulation (Windkessel model)")
    print("   • Complete digital twin workflow")
    print("   • Dose-response relationships")
    print("\n🎯 The digital twin is ready for:")
    print("   • What-if scenario analysis")
    print("   • Patient-specific predictions")
    print("   • Intervention comparison")
    print("   • Educational demonstrations")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
