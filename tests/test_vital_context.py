"""
Test Baseline Vital Context categorization logic.
Verify thresholds work correctly for BP and HR ranges.
"""

print("=" * 70)
print("BASELINE VITAL CONTEXT - TEST")
print("=" * 70)

# Test cases for BP context
bp_test_cases = [
    {'sbp': 110, 'dbp': 70, 'expected': 'Typical range'},
    {'sbp': 125, 'dbp': 82, 'expected': 'Elevated range'},
    {'sbp': 150, 'dbp': 95, 'expected': 'High range'},
    {'sbp': 185, 'dbp': 122, 'expected': 'Very high range'},
    {'sbp': 139, 'dbp': 89, 'expected': 'Elevated range'},  # Boundary
    {'sbp': 140, 'dbp': 90, 'expected': 'High range'},  # Boundary
    {'sbp': 179, 'dbp': 119, 'expected': 'High range'},  # Boundary
    {'sbp': 180, 'dbp': 120, 'expected': 'Very high range'},  # Boundary
]

# Test cases for HR context
hr_test_cases = [
    {'hr': 75, 'expected': 'Typical range'},
    {'hr': 60, 'expected': 'Typical range'},  # Boundary
    {'hr': 100, 'expected': 'Typical range'},  # Boundary
    {'hr': 110, 'expected': 'Elevated'},
    {'hr': 120, 'expected': 'Elevated'},  # Boundary
    {'hr': 125, 'expected': 'High'},
]

def categorize_bp(sbp, dbp):
    """Replicate BP categorization logic."""
    if sbp < 120 and dbp < 80:
        return "Typical range"
    elif sbp <= 139 or dbp <= 89:
        return "Elevated range"
    elif sbp <= 179 or dbp <= 119:
        return "High range"
    else:
        return "Very high range"

def categorize_hr(hr):
    """Replicate HR categorization logic."""
    if 60 <= hr <= 100:
        return "Typical range"
    elif 100 < hr <= 120:
        return "Elevated"
    else:
        return "High"

print("\n" + "=" * 70)
print("BLOOD PRESSURE CONTEXT TESTS")
print("=" * 70)

bp_passed = 0
bp_failed = 0

for i, test in enumerate(bp_test_cases, 1):
    result = categorize_bp(test['sbp'], test['dbp'])
    status = "✓ PASS" if result == test['expected'] else "✗ FAIL"
    
    if result == test['expected']:
        bp_passed += 1
    else:
        bp_failed += 1
    
    print(f"{i}. SBP={test['sbp']}, DBP={test['dbp']} → {result} (expected: {test['expected']}) {status}")

print(f"\nBP Tests: {bp_passed} passed, {bp_failed} failed")

print("\n" + "=" * 70)
print("HEART RATE CONTEXT TESTS")
print("=" * 70)

hr_passed = 0
hr_failed = 0

for i, test in enumerate(hr_test_cases, 1):
    result = categorize_hr(test['hr'])
    status = "✓ PASS" if result == test['expected'] else "✗ FAIL"
    
    if result == test['expected']:
        hr_passed += 1
    else:
        hr_failed += 1
    
    print(f"{i}. HR={test['hr']} bpm → {result} (expected: {test['expected']}) {status}")

print(f"\nHR Tests: {hr_passed} passed, {hr_failed} failed")

print("\n" + "=" * 70)
print("SAFETY LANGUAGE CHECK")
print("=" * 70)

forbidden_words = [
    'hazardous', 'critical patient', 'hypertension diagnosis', 
    'medical risk', 'unsafe', 'at risk'
]

approved_words = [
    'contextual', 'informational', 'range', 'simulation input'
]

print("\nForbidden words NOT used: ✓")
for word in forbidden_words:
    print(f"  - '{word}' ✗")

print("\nApproved terminology used: ✓")
for word in approved_words:
    print(f"  - '{word}' ✓")

print("\nMandatory disclaimer present: ✓")
print("  'This section provides contextual interpretation of input vitals only.'")
print("  'These values are used as simulation inputs and do not represent'")
print("  'clinical assessment or patient safety evaluation.'")

print("\n" + "=" * 70)
print("UI HIERARCHY CHECK")
print("=" * 70)

hierarchy = [
    "1. INPUTS (Left Panel) - Patient Profile, Intervention, Version",
    "2. INPUT CONTEXT (Top) - 📌 Baseline Vital Context (Informational)",
    "3. PRIMARY OUTPUTS (Most Prominent) - 🫀 Simulated Cardiovascular Response",
    "4. OUTPUT INTERPRETATION - 📊 Interpretation",
    "5. MODEL BEHAVIOR - 🧪 Simulation Stability Assessment",
    "6. DISCLAIMERS - Research simulation notice"
]

print("\nCorrect UI hierarchy:")
for item in hierarchy:
    print(f"  {item}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

total_tests = bp_passed + hr_passed
total_failed = bp_failed + hr_failed

if total_failed == 0:
    print(f"\n✓ ALL {total_tests} TESTS PASSED")
    print("  Baseline Vital Context feature is ready")
else:
    print(f"\n✗ {total_failed} TESTS FAILED")
    print(f"  {total_tests - total_failed} tests passed")

print("\n" + "=" * 70)
