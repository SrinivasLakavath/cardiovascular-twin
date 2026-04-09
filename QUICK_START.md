# QUICK START GUIDE
## Explainable Cardiovascular Digital Twin

**Last Updated**: April 9, 2026

---

## 🚀 GETTING STARTED IN 5 MINUTES

### Step 1: Clone or Open Project
```bash
cd d:\Major\ Project
```

### Step 2: Activate Virtual Environment
```bash
# Windows
.\.venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "
import sys
packages = ['numpy', 'pandas', 'sklearn', 'shap', 'plotly', 'streamlit', 'joblib', 'kagglehub']
missing = [p for p in packages if __import__(p.replace('-', '_'), fromlist=['']) is None]
if missing:
    print(f'❌ Missing: {missing}')
else:
    print('✅ All dependencies installed!')
"
```

### Step 5: Run Demo
```bash
# Option A: Full V1 workflow
python scripts/demo.py

# Option B: V2 Real-world workflow
python src/v2_real_world/demos/demo_v2_real_world.py

# Option C: Launch UI (browser-based)
streamlit run ui/app.py
```

---

## 📋 COMMON COMMANDS

### View Project Structure
```bash
# See complete file listing
python create_inventory.py

# See import validation
python validate_imports.py

# Generate JSON inventory
python -c "import json; inv = json.load(open('PROJECT_INVENTORY.json')); print(f'Files: {inv[\"metadata\"][\"total_py_files\"]}')"
```

### Run Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_surrogate.py -v
```

### Code Quality Checks
```bash
# Lint code
flake8 src/ tests/ ui/ --max-line-length=100

# Type checking
mypy src/ --ignore-missing-imports

# Format code
black src/ tests/ ui/
```

### Git Operations
```bash
# Check status
git status

# Create feature branch
git checkout -b feature/your-feature

# Commit changes
git add .
git commit -m "Clear description of changes"

# Push to GitHub
git push origin feature/your-feature

# Create pull request - use GitHub web interface
```

---

## 📁 KEY FILES TO KNOW

| File | Purpose |
|------|---------|
| `AI_CONTEXT.md` | **Read this first!** - Project source-of-truth |
| `masters_request.md` | Detailed validation results & analysis |
| `PROJECT_INVENTORY.json` | Machine-readable file listing |
| `requirements.txt` | All dependencies |
| `scripts/demo.py` | Simple V1 workflow example |
| `src/v2_real_world/demos/demo_v2_real_world.py` | V2 workflow example |
| `ui/app.py` | Streamlit UI entry point |
| `tests/` | Test suite (10 test files) |

---

## 🔍 BEFORE WORKING ON ANYTHING

**ALWAYS check**:

1. Read `AI_CONTEXT.md` - Updates project state
2. Check `PROJECT_INVENTORY.json` - Verify file exists
3. Check `masters_request.md` - See known issues
4. Run tests - `pytest tests/ -v --tb=short`
5. Create feature branch - `git checkout -b feature/name`

```bash
# One-liner to do all checks
echo "=== Reading context ===" && head -20 AI_CONTEXT.md && \
echo "=== Checking inventory ===" && python create_inventory.py && \
echo "=== Running tests ===" && pytest tests/ -v --tb=short
```

---

## 🎯 WORKING WITH THE CODE

### Understanding the Architecture

**V1 Pipeline (Synthetic)**:
```
scripts/demo.py
  ├─ synthetic_layer/data_generator.py     (Create synthetic patients)
  ├─ synthetic_layer/patient_sampler.py    (Sample from profiles)
  ├─ physio_engine/windkessel/core.py      (Simulate cardiovascular dynamics)
  ├─ treatment_optimizer/optimizer.py      (Optimize treatments)
  ├─ twin_model/train.py                   (Train ML surrogate)
  └─ explainability/xai_engine.py          (Generate explanations)
```

**V2 Pipeline (Real-world)**:
```
src/v2_real_world/demos/demo_v2_real_world.py
  ├─ v2_real_world/data_ingestion/        (Load real BP data)
  ├─ real_world/scale_adapter.py           (Domain scaling)
  ├─ v2_real_world/noise_model/            (Add realistic noise)
  ├─ real_world/uncertainty.py             (Quantify uncertainty)
  └─ real_world/calibration.py             (Calibrate to real data)
```

**UI Layer**:
```
ui/app.py (Main entry)
  ├─ sections/input_panel.py               (User input)
  ├─ sections/output_panel.py              (Results visualization)
  ├─ sections/metrics_panel.py             (KPI dashboard)
  ├─ sections/optimizer_panel.py           (Treatment optimization UI)
  ├─ sections/methodology_panel.py         (Technical details)
  ├─ sections/transparency_panel.py        (Model transparency)
  └─ sections/disclaimer_panel.py          (Safety warnings)
```

### Modifying Code

**Example: Add new feature to patient sampler**
```bash
# 1. Create feature branch
git checkout -b feature/enhanced-patient-sampling

# 2. Edit file
code src/synthetic_layer/patient_sampler.py

# 3. Verify imports
python validate_imports.py

# 4. Add tests
code tests/test_new_feature.py

# 5. Run tests
pytest tests/test_new_feature.py -v

# 6. Commit
git add .
git commit -m "Add enhanced patient sampling with new parameters"

# 7. Merge when ready
git checkout main
git merge feature/enhanced-patient-sampling
```

---

## 🚨 TROUBLESHOOTING

### Issue: ModuleNotFoundError
```
Error: ModuleNotFoundError: No module named 'joblib'

Solution:
pip install joblib
```

### Issue: Import Error in UI
```
Error: ImportError: No module named 'sections'

Solution:
# Run from project root, not from ui/ directory
cd d:\Major\ Project
streamlit run ui/app.py
```

### Issue: Tests Failing
```
Error: Some tests are failing

Solution:
# 1. Check all dependencies
pip install -r requirements.txt

# 2. Run validation
python validate_imports.py

# 3. Run tests with verbose output
pytest tests/ -v --tb=long

# 4. Check specific test
pytest tests/test_surrogate.py -v
```

### Issue: Git Conflicts
```
Error: Merge conflict in some file

Solution:
# 1. Check status
git status

# 2. Resolve conflicts in editor
code conflicted_file.py

# 3. Mark as resolved and commit
git add conflicted_file.py
git commit -m "Resolved merge conflict"
```

---

## 📚 FURTHER READING

| Document | Content |
|----------|---------|
| `AI_CONTEXT.md` | Complete file structure & import patterns |
| `masters_request.md` | Detailed validation analysis & next steps |
| `docs/Comprehensive_Guide.md` | Medical/technical background |
| `src/v2_real_world/README_v2.md` | V2 design decisions |
| `ui/README_UI.md` | UI architecture & components |

---

## ✅ VERIFICATION CHECKLIST

Before claiming a task is complete:

- [ ] Code runs without errors: `python your_script.py`
- [ ] Imports validate: `python validate_imports.py`
- [ ] Tests pass: `pytest tests/ -v`
- [ ] No new warnings: `flake8 modified_files.py`
- [ ] Changes committed: `git log --oneline -5`
- [ ] AI_CONTEXT.md updated if needed
- [ ] masters_request.md reviewed

```bash
# One-liner to verify everything
python validate_imports.py && pytest tests/ -q && flake8 src/ --count --quiet && git log --oneline -1
```

---

## 🤝 GETTING HELP

1. **Check `AI_CONTEXT.md`** - Most answers are there
2. **Check `masters_request.md`** - Known issues documented
3. **Search existing code** - Solution likely already exists
4. **Review tests** - Tests show how to use code correctly
5. **Check docs/** - Background and methodology

---

## 📝 WORKING WITH AI ASSISTANTS

When asking an AI to work on this project:

1. **Provide context**:
   ```
   I'm working on the Cardiovascular Digital Twin project.
   Context: Read AI_CONTEXT.md for complete file structure.
   Current task: [Your specific task]
   ```

2. **Be specific**:
   ```
   ✅ GOOD: "Add a new feature to patient_sampler.py that..."
   ❌ AVOID: "Improve the code"
   ```

3. **Verify completion**:
   - All imports valid: `python validate_imports.py`
   - Tests pass: `pytest tests/ -v`
   - No duplicates created
   - Files match PROJECT_INVENTORY.json

---

**Happy coding! 🚀**

For detailed technical information, see `AI_CONTEXT.md` and `masters_request.md`.
