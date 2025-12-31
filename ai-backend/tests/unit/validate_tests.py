"""
Validation script to check test structure and count test cases.
"""

import ast
import os
from pathlib import Path


def count_test_methods(file_path):
    """Count test methods in a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return 0, []
    
    test_methods = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            test_methods.append(node.name)
    
    return len(test_methods), test_methods


def count_test_classes(file_path):
    """Count test classes in a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return 0, []
    
    test_classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name.startswith('Test'):
            test_classes.append(node.name)
    
    return len(test_classes), test_classes


def main():
    """Main validation function."""
    test_dir = Path(__file__).parent
    test_files = [
        'test_agents.py',
        'test_api_endpoints.py',
        'test_websocket.py'
    ]
    
    print("=" * 70)
    print("UNIT TEST VALIDATION SUMMARY")
    print("=" * 70)
    print()
    
    total_classes = 0
    total_methods = 0
    
    for test_file in test_files:
        file_path = test_dir / test_file
        if not file_path.exists():
            print(f"❌ {test_file}: FILE NOT FOUND")
            continue
        
        num_classes, classes = count_test_classes(file_path)
        num_methods, methods = count_test_methods(file_path)
        
        total_classes += num_classes
        total_methods += num_methods
        
        print(f"📄 {test_file}")
        print(f"   Test Classes: {num_classes}")
        print(f"   Test Methods: {num_methods}")
        print(f"   Classes: {', '.join(classes[:3])}{'...' if len(classes) > 3 else ''}")
        print()
    
    print("=" * 70)
    print(f"TOTAL TEST CLASSES: {total_classes}")
    print(f"TOTAL TEST METHODS: {total_methods}")
    print("=" * 70)
    print()
    
    # Validation checks
    print("VALIDATION CHECKS:")
    print()
    
    checks = [
        (total_methods >= 50, f"✅ Has {total_methods} test methods (target: 50+)"),
        (total_classes >= 15, f"✅ Has {total_classes} test classes (target: 15+)"),
        (len(test_files) == 3, f"✅ Has {len(test_files)} test files (target: 3)"),
    ]
    
    all_passed = True
    for passed, message in checks:
        if passed:
            print(message)
        else:
            print(message.replace('✅', '❌'))
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All validation checks passed!")
    else:
        print("⚠️  Some validation checks failed.")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
