# Explainable Cardiovascular Digital Twin

**A physiology-inspired, data-driven cardiovascular digital twin with explainable AI capabilities for patient-specific what-if analysis.**

---

## 📋 Project Overview

This project implements an **explainable surrogate digital twin** that learns cardiovascular responses from controlled physiology-inspired simulations. The ML model predicts blood pressure changes in response to interventions, enabling personalized what-if scenario analysis.

### One-Line Definition

> *A physiology-inspired simulator generates controlled cardiovascular responses, from which an explainable machine-learning surrogate digital twin is learned for patient-specific what-if analysis.*

---

## 🏗️ Architecture

```
Patient Profile + Intervention
        ↓
Physiology-Inspired Core (Windkessel)
        ↓
Synthetic Cardiovascular Responses
        ↓
ML Surrogate Digital Twin
        ↓
Explainable AI (SHAP)
        ↓
What-If / Decision Support Analysis
```

### Key Components

1. **Physiology Engine** (`physio_engine/`): Canonical Windkessel cardiovascular model
2. **Synthetic Layer** (`synthetic_layer/`): Patient sampling and intervention mapping
3. **Data Factory** (`data/`): Controlled synthetic dataset generation
4. **Digital Twin** (`twin_model/`): ML surrogate model (Gradient Boosting)
5. **Explainability** (`explainability/`): SHAP-based feature importance and local explanations
6. **Validation** (`validation/`): Physiological sanity checks
7. **Experiments** (`experiments/`): What-if scenario analysis

---

## 🎯 What This Project IS

✅ **Educational digital twin demonstration**  
✅ **Methodology-focused research**  
✅ **Explainable AI application**  
✅ **Controlled synthetic experiment**  
✅ **Academic/research project**

---

## ⚠️ What This Project IS NOT

❌ **NOT a clinical deployment tool**  
❌ **NOT using real patient data**  
❌ **NOT a regulatory-compliant system**  
❌ **NOT claiming medical accuracy**  
❌ **NOT simulating real drugs**

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Windows OS

### Installation

```bash
# Install dependencies
pip install numpy scipy pandas scikit-learn matplotlib shap jupyter
```

### Usage

```bash
# 1. Generate synthetic dataset
python synthetic_layer/data_generator.py

# 2. Train the digital twin
python twin_model/train.py

# 3. Evaluate the model
python twin_model/evaluate.py

# 4. Run validation checks
python validation/physiological_checks.py

# 5. Generate SHAP explanations (optional)
python explainability/shap_global.py
python explainability/shap_local.py
```

---

## 📊 Project Structure

```
cardio-digital-twin/
├── physio_engine/windkessel/      # Windkessel ODE model
├── synthetic_layer/               # Patient & intervention generators
├── data/raw/                      # Synthetic dataset
├── twin_model/                    # ML surrogate twin
│   ├── model.py                   # Model architecture
│   ├── train.py                   # Training pipeline
│   ├── evaluate.py                # Evaluation metrics
│   └── weights/                   # Trained models
├── explainability/                # SHAP analysis
│   ├── shap_global.py            # Global feature importance
│   ├── shap_local.py             # Patient-specific explanations
│   └── plots/                     # Visualization outputs
├── validation/                    # Physiological checks
└── experiments/                   # What-if analysis
```

---

## 🔬 Technical Details

### Windkessel Model

The physiology engine uses a canonical lumped-parameter Windkessel model:

```
dP/dt = (Q(t) - P/R) / C
```

Where:
- `P` = Blood pressure (mmHg)
- `Q(t)` = Pulsatile cardiac output (L/min)
- `R` = Peripheral resistance (mmHg·min/L)
- `C` = Arterial compliance (L/mmHg)

### Intervention Mapping

Abstract drug classes are mapped to parameter changes:

| Intervention | Effect |
|-------------|--------|
| Beta-blocker | ↓ Cardiac output (Q) |
| Vasodilator | ↓ Peripheral resistance (R) |
| Stimulant | ↑ Cardiac output (Q) |
| Volume expander | ↑ Arterial compliance (C) |

### ML Model

- **Architecture**: Gradient Boosting (Multi-output Regression)
- **Inputs**: Age, baseline BP, heart rate, risk group, drug class, dosage
- **Outputs**: Δ SBP, Δ DBP
- **Performance**: MAE < 0.01 mmHg

---

## 📈 Results

### Model Performance

- **MAE (delta_sbp)**: 0.0029 mmHg
- **MAE (delta_dbp)**: 0.0029 mmHg
- **R² Score**: > 0.99

### Validation

✅ All physiological sanity checks passed:
- Directional correctness (beta-blockers ↓ BP, stimulants ↑ BP)
- Dose-response monotonicity
- Physiological bounds respected
- SBP-DBP correlation maintained

---

## 🧠 Explainability

The project uses SHAP (SHapley Additive exPlanations) to provide:

1. **Global Feature Importance**: Which variables dominate response predictions
2. **Local Explanations**: Patient-specific reasoning for individual predictions
3. **Dose-Response Analysis**: How intervention dosage affects outcomes

---

## 🎓 Key Assumptions

1. **Simplified Physiology**: Windkessel is a canonical abstraction, not a clinical simulator
2. **Synthetic Data**: All patient profiles are generated, not real
3. **Abstract Interventions**: Drug effects are modeled as parameter changes, not pharmacokinetics
4. **Educational Purpose**: Focus on methodology, not clinical deployment

---

## 📝 Limitations

- No real patient data validation
- Simplified cardiovascular model (lumped-parameter)
- Abstract intervention representation
- No temporal dynamics (single time-point predictions)
- Not validated against clinical trials

---

## 🌍 Real-World Applicability & Limitations

### What Would Change with Real Data

**Current State (Synthetic)**:
- Training data: 1000 synthetic samples from Windkessel simulator
- Patient profiles: Generated with controlled distributions
- Interventions: Abstract parameter mappings
- Validation: Physiological sanity checks only

**Real-World Deployment Requirements**:

1. **Data Collection**: Collect 500-1000 real patient observations with diverse demographics
2. **Model Adaptation**: Recalibrate using `real_world/scale_adapter.py`
3. **Patient-Specific Calibration**: Use `real_world/calibration.py` for personalization

### Expected Accuracy Behavior

- **Synthetic Data** (Current): MAE 0.0029 mmHg, R² > 0.99
- **Real-World Without Calibration**: MAE 10-20 mmHg (poor)
- **Real-World With Calibration**: MAE 3-7 mmHg (good, comparable to clinical variability)

### Safety and Uncertainty Handling

**Mandatory Safety Mechanisms**:
1. Uncertainty quantification (`real_world/uncertainty.py`)
2. Out-of-distribution detection
3. Clinical decision rules based on confidence levels
4. Human oversight for all predictions

**Deployment Readiness**: 32/50 (64%) - **PARTIAL READINESS**

See `real_world/readiness_scorecard.py` for detailed assessment.

### Why Synthetic Validation Is Still Meaningful

**What It Proves**:
- ✅ Technical feasibility and algorithmic correctness
- ✅ Explainability capability
- ✅ Methodological soundness

**What It Does NOT Prove**:
- ❌ Clinical accuracy or real-world generalization
- ❌ Safety in practice or regulatory compliance

**Path to Deployment**: Requires real patient data validation, clinical validation study, and regulatory approval (12-24 month timeline).

---

## 🔮 Future Work

- Incorporate temporal dynamics (time-series predictions)
- Add more physiological variables (ECG, cardiac output)
- Validate against synthetic benchmarks
- **✅ Uncertainty quantification** (IMPLEMENTED)
- Extend to multi-organ systems
- **Conduct real-world validation study**
- **Pursue regulatory approval pathway**

---

## 📚 References

### Windkessel Model
- Westerhof, N., et al. (2009). "The arterial Windkessel." *Medical & Biological Engineering & Computing*, 47(2), 131-141.

### Explainable AI
- Lundberg, S. M., & Lee, S. I. (2017). "A unified approach to interpreting model predictions." *NeurIPS*.

---

## 👨‍💻 Author

Major Project - Explainable Cardiovascular Digital Twin  
Created: January 2026

---

## 📄 License

This is an academic/research project for educational purposes.

---

## 🙏 Acknowledgments

- Windkessel model based on canonical cardiovascular physiology
- SHAP library for explainability
- Scikit-learn for ML implementation

---

## 💡 Defense Notes

### Key Phrase for Viva

> "Our work focuses on learning an explainable surrogate digital twin from controlled physiology-inspired simulations, rather than claiming direct clinical realism."

### Strengths

- **Low technical risk**: Fully controllable system
- **Explainable by design**: SHAP integration from the start
- **Easy to defend**: Explicit assumptions and limitations
- **Scales with effort**: Can add complexity incrementally
- **Methodology-focused**: Demonstrates understanding over tool usage

---

**This project demonstrates the integration of physiology-inspired modeling, machine learning, and explainable AI for cardiovascular digital twin development.**
