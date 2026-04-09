#!/usr/bin/env python3
"""
Import Validation Script
Checks for missing/invalid imports and ensures all local imports are resolvable
"""
import ast
import sys
from pathlib import Path
from collections import defaultdict

# Standard library & common external packages
EXTERNAL_PACKAGES = {
    'numpy', 'np', 'pandas', 'pd', 'sklearn', 'scipy', 'shap', 'plotly', 
    'streamlit', 'st', 'kagglehub', 'requests', 'matplotlib', 'seaborn',
    'json', 'pickle', 'os', 'sys', 're', 'datetime', 'warnings', 'math',
    'random', 'functools', 'itertools', 'collections', 'typing', 'logging'
}

def extract_imports(file_path):
    """Extract all imports from a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            tree = ast.parse(f.read())
        
        imports = {'modules': [], 'froms': []}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports['modules'].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports['froms'].append({
                        'module': node.module,
                        'names': [alias.name for alias in node.names]
                    })
        
        return imports
    except Exception as e:
        return {'modules': [], 'froms': [], 'error': str(e)}

def resolve_local_import(root_dir, import_name):
    """Check if a local import can be resolved"""
    # Replace dots with path separators
    parts = import_name.split('.')
    
    # Check as package (__init__.py)
    package_path = Path(root_dir) / Path(*parts) / '__init__.py'
    if package_path.exists():
        return True, 'package'
    
    # Check as module (.py file)
    module_path = Path(root_dir) / (Path(*parts).with_suffix('.py'))
    if module_path.exists():
        return True, 'module'
    
    return False, None

def is_local_import(import_name):
    """Determine if an import is local to the project"""
    # Exclude standard library and common external packages
    root_module = import_name.split('.')[0]
    
    return root_module not in EXTERNAL_PACKAGES and not root_module.startswith('_')

def validate_all_imports(root_dir):
    """Check if all local imports exist"""
    issues = {
        'missing': [],
        'invalid_syntax': [],
        'files_processed': 0,
        'total_imports': 0
    }
    
    all_files = {}  # Track all found files
    
    # First pass: find all available local modules
    for py_file in Path(root_dir).rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        rel_path = str(py_file.relative_to(root_dir)).replace('\\', '/')
        module_name = rel_path.replace('/', '.').replace('.py', '')
        all_files[module_name] = py_file
    
    # Second pass: validate imports
    for py_file in Path(root_dir).rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        
        rel_path = str(py_file.relative_to(root_dir)).replace('\\', '/')
        imports = extract_imports(py_file)
        issues['files_processed'] += 1
        
        if 'error' in imports:
            issues['invalid_syntax'].append({
                'file': rel_path,
                'error': imports['error']
            })
            continue
        
        # Check module imports
        for module_import in imports['modules']:
            issues['total_imports'] += 1
            if is_local_import(module_import):
                exists, import_type = resolve_local_import(root_dir, module_import)
                if not exists:
                    issues['missing'].append({
                        'file': rel_path,
                        'import': module_import,
                        'type': 'direct_import'
                    })
        
        # Check from...import statements
        for from_import in imports['froms']:
            issues['total_imports'] += 1
            module = from_import['module']
            if is_local_import(module):
                exists, import_type = resolve_local_import(root_dir, module)
                if not exists:
                    issues['missing'].append({
                        'file': rel_path,
                        'import': module,
                        'type': 'from_import',
                        'names': from_import['names']
                    })
    
    return issues, all_files

def print_validation_report(issues, all_files):
    """Pretty print validation report"""
    print("\n" + "="*80)
    print("IMPORT VALIDATION REPORT".center(80))
    print("="*80 + "\n")
    
    print(f"📊 STATISTICS:")
    print(f"   Files Processed: {issues['files_processed']}")
    print(f"   Total Imports: {issues['total_imports']}")
    print(f"   Available Local Modules: {len(all_files)}\n")
    
    if issues['invalid_syntax']:
        print(f"⚠️  SYNTAX ERRORS ({len(issues['invalid_syntax'])} files):")
        for item in issues['invalid_syntax']:
            print(f"   {item['file']}: {item['error']}")
        print()
    
    if issues['missing']:
        print(f"❌ MISSING IMPORTS ({len(issues['missing'])} issues):")
        for item in issues['missing']:
            import_type = item['type']
            if import_type == 'from_import':
                print(f"   {item['file']}")
                print(f"      └─ from {item['import']} import {', '.join(item['names'])}")
            else:
                print(f"   {item['file']}")
                print(f"      └─ import {item['import']}")
        print()
    else:
        print("✅ ALL LOCAL IMPORTS ARE VALID\n")
    
    print(f"📦 AVAILABLE LOCAL MODULES ({len(all_files)}):")
    for module_name in sorted(all_files.keys())[:20]:  # Show first 20
        print(f"   {module_name}")
    if len(all_files) > 20:
        print(f"   ... and {len(all_files) - 20} more modules")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    root = "."
    print("🔍 Validating all imports...")
    
    issues, all_files = validate_all_imports(root)
    print_validation_report(issues, all_files)
    
    # Return exit code based on issues
    if issues['missing'] or issues['invalid_syntax']:
        print("\n⚠️  ISSUES FOUND - Review above for details")
        sys.exit(1)
    else:
        print("\n✅ PROJECT IMPORTS VALIDATED SUCCESSFULLY")
        sys.exit(0)
