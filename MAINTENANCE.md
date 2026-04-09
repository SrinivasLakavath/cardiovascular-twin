# Maintenance & Development Guide
## Cardiovascular Digital Twin Project

**Last Updated**: April 9, 2026  
**Project Status**: ✅ All pipelines operational and validated

---

## 📋 BEFORE ADDING ANY NEW FEATURES

### Checklist
```bash
# 1. Verify current state
python create_inventory.py
python validate_imports.py

# 2. Read project context
cat AI_CONTEXT.md

# 3. Create feature branch
git checkout -b feature/your-feature-name

# 4. Make changes (modify existing files, don't create duplicates)
# 5. Test changes
python -m pytest tests/ -v

# 6. Commit
git add .
git commit -m "Clear description of changes"
git push origin feature/your-feature-name
```

---

## 🛠️ COMMON MAINTENANCE TASKS

### Task 1: Add a New Feature to V1 Pipeline
```bash
# Example: Adding a new intervention type to data generator

# 1. Read AI_CONTEXT.md to find the file
# 2. Location: src/synthetic_layer/data_generator.py

# 3. Edit the file (don't create duplicate)
code src/synthetic_layer/data_generator.py

# 4. Test
python scripts/demo.py

# 5. Run validation
python validate_imports.py

# 6. Commit
git add src/synthetic_layer/data_generator.py
git commit -m "Add new intervention type: ACE_inhibitor"
```

### Task 2: Update UI Panel
```bash
# Example: Modify the methodology panel

# 1. File: ui/sections/methodology_panel.py
code ui/sections/methodology_panel.py

# 2. Changes will appear immediately when running:
streamlit run ui/app.py  # Auto-reloads on save

# 3. Commit when satisfied
git add ui/sections/methodology_panel.py
git commit -m "Update methodology panel with better explanations"
```

### Task 3: Add New Test
```bash
# Example: Test new feature in V2

# 1. Create test file
code tests/test_new_feature.py

# 2. Test structure
def test_new_feature():
    from new_module import new_function
    result = new_function(test_input)
    assert result == expected_output

# 3. Run test
pytest tests/test_new_feature.py -v

# 4. Add to CI/CD
git add tests/test_new_feature.py
git commit -m "Add test for new feature"
```

---

## 🚨 CRITICAL RULES

### Rule 1: NO FILE DUPLICATION
❌ **WRONG**: Create `model_v2.py`, `train_old.py`, `calibration_backup.py`  
✅ **RIGHT**: Edit `src/twin_model/model.py` directly

**Why**: Duplicates cause AI hallucinations and maintenance confusion.

### Rule 2: V1 vs V2 Separation
- **V1 Files**: `src/synthetic_layer/`, `src/twin_model/`, `src/explainability/`
- **V2 Files**: `src/v2_real_world/`, `src/real_world/`
- **Don't mix**: V1 code stays independent, V2 extends it

### Rule 3: Always Keep AI_CONTEXT.md Updated
If you create new files:
```
# Update AI_CONTEXT.md
git add AI_CONTEXT.md
git commit -m "Update: Added new_module.py to file structure"
```

### Rule 4: Run Validation After Changes
```bash
# After ANY code changes, run:
python validate_imports.py
pytest tests/ -v
```

---

## 📞 WHEN WORKING WITH AI ASSISTANTS

### Session Start Template
Copy this when asking AI to work on the project:

```
I'm working on the Cardiovascular Digital Twin project.

BEFORE YOU MAKE ANY CHANGES:
1. Read AI_CONTEXT.md - shows exact file structure
2. Check if file already exists in PROJECT_INVENTORY.json
3. If it exists → modify existing file using str_replace
4. If new → ask me first before creating

Read AI_CONTEXT.md for:
- Exact file paths
- Import patterns used
- Architecture constraints
- What NOT to do

Current task: [Your specific task]
```

### If AI Suggests New File
```
⚠️ BEFORE CREATING: 
1. Check: Already exists in AI_CONTEXT.md?
2. If yes → Modify existing instead
3. If no → Confirm I want new file
```

### After AI Work
```bash
# Verify everything works
python validate_imports.py
pytest tests/ -v
python scripts/demo.py
```

---

## 📅 MONTHLY MAINTENANCE CHECKLIST

- [ ] Run all demo scripts (no errors?)
  ```bash
  python scripts/demo.py
  python src/v2_real_world/demos/demo_v2_real_world.py
  ```

- [ ] Check for outdated dependencies
  ```bash
  pip list --outdated
  ```

- [ ] Update requirements.txt if needed
  ```bash
  pip freeze > requirements.txt
  ```

- [ ] Review git history for duplicate files
  ```bash
  python create_inventory.py  # Check "duplicates" section
  ```

- [ ] Run full test suite with coverage
  ```bash
  pytest tests/ --cov=src --cov-report=html
  open htmlcov/index.html
  ```

- [ ] Check import health
  ```bash
  python validate_imports.py
  ```

---

## 🆘 TROUBLESHOOTING

### Problem: "ModuleNotFoundError"
```bash
# Solution: Verify module exists
python create_inventory.py
# Check if module appears in PROJECT_INVENTORY.json

# If not found, check file paths:
ls -la src/module_name/
```

### Problem: "Import already exists" (duplicate file)
```bash
# Solution: Find and compare duplicates
python create_inventory.py
# Review duplicates section

# Keep one version, delete other:
git rm src/old_version/model.py
git commit -m "Remove duplicate model file"
```

### Problem: Tests failing after changes
```bash
# Solution: Debug step by step
pytest tests/ -v  # See which test failed
pytest tests/specific_test.py -v --tb=long  # Get details
python -c "import modified_module; print('OK')"  # Test imports
```

### Problem: Merge conflicts in git
```bash
# Solution: Resolve manually
git status  # See conflicted files
code conflicted_file.py  # Edit and remove conflict markers
git add conflicted_file.py
git commit -m "Resolved merge conflict"
```

---

## 🔄 DEPLOYMENT PROCESS

### Step 1: Feature Complete
- Code works locally: `python scripts/demo.py` ✓
- Imports valid: `python validate_imports.py` ✓  
- Tests pass: `pytest tests/ -v` ✓

### Step 2: Commit & Push
```bash
git add .
git commit -m "Feature complete: [description]"
git push origin feature/branch-name
```

### Step 3: Create Pull Request
- Go to GitHub
- Create PR from `feature/branch-name` → `main`
- Add description of changes
- Wait for CI/CD to pass

### Step 4: Merge to Main
```bash
git checkout main
git merge feature/branch-name
git push origin main
```

### Step 5: Deploy UI (if changed)
```bash
# Push to deployment service (Streamlit, Heroku, etc)
streamlit run ui/app.py  # Local test first
```

---

## 📊 PROJECT STRUCTURE REMINDER

```
cardiovascular-digital-twin/
├── src/                    # Core modules
│   ├── synthetic_layer/    # V1: Data generation
│   ├── twin_model/         # V1: ML surrogate
│   ├── explainability/     # V1: SHAP analysis
│   ├── v2_real_world/      # V2: Real-world grounding
│   ├── real_world/         # V2: Calibration
│   └── validation/         # V2: Verification
├── ui/                     # Streamlit interface
│   ├── app.py             # Main entry
│   ├── sections/          # 7 UI panels
│   └── assets/            # Icons, styling
├── tests/                  # Test suite (10 test files)
├── scripts/                # Demo scripts
├── docs/                   # Documentation
├── AI_CONTEXT.md          # FILE STRUCTURE (READ FIRST)
├── MAINTENANCE.md         # THIS FILE
├── requirements.txt        # Dependencies
└── .github/workflows/      # CI/CD pipelines
```

---

## 🎯 GOALS & NON-GOALS

### We ARE building
✅ Transparent ML model explanation  
✅ Synthetic+real-world comparison  
✅ Research demonstration tool  
✅ Educational cardiovascular simulator  
✅ Modular, extensible architecture  

### We ARE NOT building
❌ Clinical decision support system  
❌ Real patient prediction tool  
❌ Production-grade deployment  
❌ Real-time continuous monitoring  
❌ FDA-regulated medical device  

**Keep this in mind when adding features!**

---

## 📞 GETTING HELP

1. **Code issue?** → Check `AI_CONTEXT.md` file structure
2. **Import error?** → Run `python validate_imports.py`
3. **Test failure?** → Run `pytest tests/ -v`
4. **Duplicate file?** → Run `python create_inventory.py`
5. **Deployment?** → Check README.md
6. **AI assistant confusion?** → Share `AI_CONTEXT.md` with them

---

## ✅ MAINTENANCE CHECKLIST - FIRST TIME

- [ ] Read this entire file
- [ ] Understand the 4 critical rules
- [ ] Know where AI_CONTEXT.md is located
- [ ] Know how to run validate_imports.py
- [ ] Know how to run tests: pytest tests/ -v
- [ ] Bookmark this file for reference

**Remember**: This project is COMPLETE. New work is EXTENSION, not RECREATION.

---

**Last Maintenance Check**: April 9, 2026  
**Status**: ✅ All systems operational  
**Next Check**: Monthly or after major changes
