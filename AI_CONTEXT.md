# AI ASSISTANT CONTEXT - SOURCE OF TRUTH
## Explainable Cardiovascular Digital Twin

**Last Updated**: April 9, 2026  
**Last Validated**: Complete project scan + AST import verification  
**Total Files**: 51 Python files (9,808 lines of code)

---

## 🎯 PROJECT OVERVIEW

**Mission**: Create a transparent, interpretable ML digital twin of cardiovascular system dynamics that bridges synthetic training (V1) with real-world applications (V2).

**Architecture**:
- **V1**: Synthetic-only pipeline (generates data → trains model → explains)
- **V2**: Real-world grounded (calibration, noise models, uncertainty)
- **UI**: Streamlit research interface with 7 specialized panels

---

## 📁 DEFINITIVE FILE STRUCTURE (SOURCE OF TRUTH)

### Root Level Files (2)
```
create_inventory.py      (133 lines) - Project inventory scanner
validate_imports.py      (182 lines) - Import validation tool
PROJECT_INVENTORY.json   - Machine-readable inventory
AI_CONTEXT.md           - This file (AI source-of-truth)
masters_request.md      - Phase 1 validation results
```

### docs/ (1 file)
```
convert_to_word.py      (120 lines) - Markdown→Word converter
```

### scripts/ (3 files)
```
demo.py                 (238 lines) - V1 complete workflow demo
check_calibration.py    (32 lines)  - Calibration testing
reproduce_sensitivity.py (46 lines) - Sensitivity analysis
```

### src/ (25 files) - CORE PROJECT CODE

#### src/explainability/ (3 files, 651 lines)
```
shap_global.py          (153 lines) - Global feature importance
shap_local.py           (166 lines) - Local instance explanations  
xai_engine.py           (332 lines) - Main XAI orchestration
```

#### src/physio_engine/windkessel/ (2 files, 203 lines)
```
__init__.py             (11 lines)  - Package marker [⚠️ FIX: use relative import]
core.py                 (192 lines) - Main Windkessel ODE model
```

#### src/real_world/ (4 files, 1,396 lines)
```
calibration.py          (314 lines) - Parameter calibration
readiness_scorecard.py  (385 lines) - Medical readiness scoring
scale_adapter.py        (355 lines) - Domain scaling/normalization
uncertainty.py          (342 lines) - Uncertainty quantification
```

#### src/synthetic_layer/ (3 files, 596 lines)
```
data_generator.py       (192 lines) - Patient data generation
intervention_mapper.py  (239 lines) - Treatment effect mapping
patient_sampler.py      (165 lines) - Synthetic patient profiles
```

#### src/treatment_optimizer/ (2 files, 298 lines)
```
__init__.py             (2 lines)   - Package marker
optimizer.py            (296 lines) - Treatment optimization engine
```

#### src/twin_model/ (3 files, 561 lines)
```
model.py                (154 lines) - ML surrogate (GradientBoosting)
train.py                (175 lines) - Training pipeline
evaluate.py             (232 lines) - Evaluation metrics
```

#### src/v2_real_world/ (8 files, 1,423 lines)
```
README_v2.md            - V2 documentation
data/
  bp_statistics.json    - BP statistics reference
  kaggle_bp_data.csv    - Real BP data sample

data_ingestion/
  kaggle_loader.py      (224 lines) - Kaggle dataset loading

demos/
  demo_v2_real_world.py (222 lines) - V2 complete workflow

domain_shift/
  domain_shift_tests.py (324 lines) - Domain shift analysis ✅ INTENTIONAL DUPLICATE

noise_model/
  noise_injector.py     (324 lines) - Realistic noise model

statistics/
  bp_statistics.py      (274 lines) - Statistical utilities

uncertainty/
  uncertainty_wrapper.py (279 lines) - Uncertainty quantification
```

#### src/validation/ (2 files, 534 lines)
```
domain_shift_tests.py   (304 lines) - Domain shift tests (V1 version)
physiological_checks.py (230 lines) - Physiological validation
```

### ui/ (10 files, 2,109 lines) - STREAMLIT INTERFACE

```
app.py                  (253 lines) - Main entry point

sections/               (7 files, 1,656 lines)
  input_panel.py        (137 lines) - Patient input form
  output_panel.py       (914 lines) - Results visualization [LARGEST]
  metrics_panel.py      (152 lines) - KPI dashboard
  methodology_panel.py  (176 lines) - Tech explanation
  optimizer_panel.py    (222 lines) - Treatment optimizer UI
  transparency_panel.py (88 lines)  - Model transparency
  disclaimer_panel.py   (73 lines)  - Safety disclaimers

assets/                 (2 files)
  __init__.py           (1 line)    - Package marker
  icons.py              (93 lines)  - Icon definitions
```

### tests/ (11 files, 1,062 lines)

```
test_backend_ui_match.py      (96 lines)  - V1↔V2 consistency
test_custom_integration.py    (56 lines)  - Integration tests
test_optimizer.py             (122 lines) - Optimizer validation
test_stability_assessment.py  (175 lines) - Stability checks
test_surrogate.py             (62 lines)  - Model validation
test_ui_simulation.py         (101 lines) - UI functionality
test_v1_v2_difference.py      (123 lines) - V1 vs V2 comparison
test_v2_uncertainty.py        (85 lines)  - Uncertainty testing
test_vital_context.py         (150 lines) - Physiological context
ui/
  test_connection.py          (92 lines)  - UI connection tests
```

---

## 🚨 CRITICAL CONSTRAINTS

### DO NOT ❌
- ❌ Create duplicate files with `_v2`, `_old`, `_backup` suffixes
- ❌ Create new versions of `model.py` - modify existing one
- ❌ Ignore the `domain_shift_tests.py` duplicate - it's **INTENTIONAL** (V1 vs V2 versions)
- ❌ Assume files exist without checking `PROJECT_INVENTORY.json`
- ❌ Modify V1 code when working on V2 features (use separate branches)
- ❌ Mix relative and absolute imports in the same module

### DO ✅
- ✅ Check `masters_request.md` BEFORE proposing changes
- ✅ Verify file exists in `PROJECT_INVENTORY.json` before modifying
- ✅ Use `git branch` for experimental work
- ✅ Commit changes with descriptive messages
- ✅ Run `validate_imports.py` after adding new imports
- ✅ Run `pytest tests/` before considering work complete

---

## 🚀 HOW TO VALIDATE FILE EXISTENCE

**Option 1: Quick lookup**
```bash
python -c "
import json
with open('PROJECT_INVENTORY.json') as f:
    inv = json.load(f)
    files = [f['path'] for f in inv['files']]
    if 'src/twin_model/model.py' in files:
        print('✅ File exists')
    else:
        print('❌ File not found')
"
```

**Option 2: Visual check**
Open `PROJECT_INVENTORY.json` and search for the filename.

**Option 3: Use inventory script**
```bash
python create_inventory.py  # Re-scans and generates fresh inventory
```

---

## 📦 EXTERNAL DEPENDENCIES (MUST BE INSTALLED)

| Package | Version | Usage |
|---------|---------|-------|
| numpy | Latest | Numerical computing |
| pandas | Latest | Data manipulation |
| scikit-learn | Latest | Machine learning |
| scipy | Latest | Scientific computing |
| shap | Latest | Model explanation |
| plotly | Latest | Interactive visualization |
| streamlit | Latest | UI framework |
| joblib | Latest | Model persistence |
| kagglehub | Latest | Dataset access |
| python-docx | Latest | Word document generation |

**Verify installation**:
```bash
pip list | grep -E "numpy|pandas|scikit|shap|plotly|streamlit|joblib"
```

---

## 🔧 IMPORT PATTERNS IN USE

### Pattern 1: sys.path manipulation (Used in scripts/)
```python
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
from synthetic_layer.patient_sampler import sample_patient  # ✅ Works
```

### Pattern 2: Relative imports (Used in UI)
```python
from sections.input_panel import render_input_panel  # ✅ Works from ui/ root
from assets.icons import icon                        # ✅ Works from ui/ root
```

### Pattern 3: Absolute imports (Recommended for src/ modules)
```python
from src.synthetic_layer.patient_sampler import sample_patient  # ✅ Clean
from src.twin_model.model import SurrogateTwin                  # ✅ Clean
```

---

## ⚠️ KNOWN ISSUES TO FIX

### Priority 1: Windkessel relative import
**File**: `src/physio_engine/windkessel/__init__.py`  
**Current**: `from core import simulate_bp, windkessel_ode`  
**Fix**: `from .core import simulate_bp, windkessel_ode`  
**Why**: Explicit relative imports prevent import errors when used as package

**Status**: ⏳ NEEDS FIXING

---

## 📝 BEFORE MAKING CHANGES

**ALWAYS follow this checklist**:

1. ✅ **Verify file exists**
   - Check `PROJECT_INVENTORY.json` or run `create_inventory.py`
   
2. ✅ **Check git status**
   ```bash
   git status  # See what's changed
   ```

3. ✅ **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. ✅ **Make changes** to existing files (don't create new ones)

5. ✅ **Run validation**
   ```bash
   python validate_imports.py
   pytest tests/ -v
   ```

6. ✅ **Commit locally**
   ```bash
   git add .
   git commit -m "Clear description of changes"
   ```

7. ✅ **Merge to main when stable**
   ```bash
   git checkout main
   git merge feature/your-feature-name
   ```

---

## 🎯 CURRENT STATE (As of April 9, 2026)

| Component | Status | Notes |
|-----------|--------|-------|
| V1 Pipeline (Synthetic) | ✅ COMPLETE | Fully functional, tested |
| V2 Pipeline (Real-world) | ✅ COMPLETE | Domain adaptation working |
| UI Layer | ✅ COMPLETE | 7 panels, all functional |
| Test Suite | ✅ COMPLETE | 10 test files covering core |
| Documentation | ✅ ADEQUATE | README + docs/ folder |
| GitHub Repo | ⏳ PENDING | Need to create |
| CI/CD Pipeline | ⏳ PENDING | Need to set up |
| Pre-commit Hooks | ⏳ PENDING | Need to configure |

---

## 🔍 FILE VERIFICATION CHECKLIST

Use this when AI or human asks "does X file exist?":

- [✅] `create_inventory.py` - Exists (133 lines)
- [✅] `validate_imports.py` - Exists (182 lines)
- [✅] `src/twin_model/model.py` - Exists (154 lines)
- [✅] `ui/app.py` - Exists (253 lines)
- [✅] `scripts/demo.py` - Exists (238 lines)
- [❌] `models/trained_model.pkl` - DOES NOT EXIST (save location TBD)
- [❌] `requirements-dev.txt` - DOES NOT EXIST (needs creation)
- [❌] `.pre-commit-config.yaml` - DOES NOT EXIST (needs creation)

---

## 📞 WHEN TO CONSULT THIS FILE

**Consult AI_CONTEXT.md when**:
- Starting a new task on this project
- Switching between AI models/tools
- Proposing file structure changes
- Unsure if a file exists
- Need to understand import patterns
- Planning major refactoring

**Update AI_CONTEXT.md when**:
- Adding new modules
- Creating new files
- Fixing known issues
- Changing import strategies
- Updating dependencies

---

## 🚀 NEXT ACTIONS FOR AI ASSISTANT

1. **Before any task**: Read this file completely
2. **For file modifications**: 
   - Search `PROJECT_INVENTORY.json` for filename
   - If found: modify existing file
   - If not found: ask user before creating
3. **For imports**: 
   - Verify module exists first
   - Use consistent import pattern
   - Run `validate_imports.py` after changes
4. **For large changes**: 
   - Communicate plan to user first
   - Test locally before finalizing
   - Provide clear commit messages

---

**This document is the source-of-truth for project structure.**  
**All AI interactions should reference this file to prevent hallucinations.**  
**Last verified**: April 9, 2026 via full project AST scan.
