#!/usr/bin/env python3
"""
Project Inventory Scanner
Creates complete mapping of all files in the project to prevent AI hallucinations
"""
import os
import json
from pathlib import Path
from collections import defaultdict

def scan_project(root_dir):
    """Create complete project inventory"""
    inventory = {
        'metadata': {
            'total_py_files': 0,
            'total_lines': 0,
            'total_size_kb': 0,
            'scan_root': root_dir
        },
        'files': [],
        'by_directory': defaultdict(list),
        'duplicates': [],
        'file_summary': {}
    }
    
    # Track all .py files
    py_files = sorted(Path(root_dir).rglob('*.py'))
    
    for file in py_files:
        try:
            rel_path = file.relative_to(root_dir)
            size = file.stat().st_size
            content = file.read_text(encoding='utf-8', errors='ignore')
            lines = len(content.split('\n'))
            
            # Don't count __pycache__ files
            if '__pycache__' in str(rel_path):
                continue
            
            file_info = {
                'path': str(rel_path).replace('\\', '/'),
                'size_kb': round(size/1024, 2),
                'lines': lines,
                'directory': str(file.parent.relative_to(root_dir)).replace('\\', '/')
            }
            
            inventory['files'].append(file_info)
            inventory['by_directory'][file_info['directory']].append(str(rel_path))
            
            inventory['metadata']['total_py_files'] += 1
            inventory['metadata']['total_lines'] += lines
            inventory['metadata']['total_size_kb'] += round(size/1024, 2)
            
        except Exception as e:
            print(f"⚠️  Error processing {file}: {e}")
    
    # Find potential duplicates (same filename in different directories)
    filenames = {}
    for file_info in inventory['files']:
        filename = Path(file_info['path']).name
        if filename not in filenames:
            filenames[filename] = []
        filenames[filename].append(file_info['path'])
    
    for filename, paths in filenames.items():
        if len(paths) > 1:
            inventory['duplicates'].append({
                'filename': filename,
                'locations': paths
            })
    
    # Create summary by module
    for file_info in inventory['files']:
        dir_name = Path(file_info['path']).parts[0] if '/' in file_info['path'] else 'root'
        if dir_name not in inventory['file_summary']:
            inventory['file_summary'][dir_name] = {
                'count': 0,
                'total_lines': 0,
                'files': []
            }
        inventory['file_summary'][dir_name]['count'] += 1
        inventory['file_summary'][dir_name]['total_lines'] += file_info['lines']
        inventory['file_summary'][dir_name]['files'].append(file_info['path'])
    
    return inventory

def print_inventory_report(inventory):
    """Pretty print the inventory"""
    print("\n" + "="*80)
    print("PROJECT INVENTORY REPORT".center(80))
    print("="*80 + "\n")
    
    meta = inventory['metadata']
    print(f"📊 STATISTICS:")
    print(f"   Total Python Files: {meta['total_py_files']}")
    print(f"   Total Lines of Code: {meta['total_lines']:,}")
    print(f"   Total Size: {meta['total_size_kb']:.1f} KB\n")
    
    print(f"📁 BREAKDOWN BY DIRECTORY:")
    for dir_name, stats in sorted(inventory['file_summary'].items()):
        print(f"   {dir_name:30} {stats['count']:3} files  {stats['total_lines']:6,} lines")
    
    print(f"\n📄 ALL FILES ({len(inventory['files'])} total):")
    for file_info in sorted(inventory['files'], key=lambda x: x['path']):
        print(f"   {file_info['path']:50} {file_info['lines']:6} lines  {file_info['size_kb']:7.1f} KB")
    
    if inventory['duplicates']:
        print(f"\n⚠️  POTENTIAL DUPLICATES ({len(inventory['duplicates'])} found):")
        for dup in inventory['duplicates']:
            print(f"   Filename: {dup['filename']}")
            for loc in dup['locations']:
                print(f"     └─ {loc}")
    else:
        print(f"\n✅ NO DUPLICATE FILENAMES DETECTED")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    root = "."
    print("🔍 Scanning project structure...")
    
    inv = scan_project(root)
    print_inventory_report(inv)
    
    # Save JSON for programmatic access
    output_file = 'PROJECT_INVENTORY.json'
    with open(output_file, 'w') as f:
        # Convert defaultdict to regular dict for JSON serialization
        inv['by_directory'] = dict(inv['by_directory'])
        json.dump(inv, f, indent=2)
    
    print(f"\n💾 Complete inventory saved to: {output_file}\n")
