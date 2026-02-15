#!/usr/bin/env python3
"""
Verification script to test if CSV to Excel converter is set up correctly.
"""

import sys
import subprocess
from pathlib import Path

def print_status(message: str, success: bool = True):
    """Print status message with emoji."""
    emoji = "✅" if success else "❌"
    print(f"{emoji} {message}")

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    message = f"Python version: {version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 7:
        print_status(message, True)
        return True
    else:
        print_status(f"{message} (requires 3.7+)", False)
        return False

def check_file_exists(filepath: str):
    """Check if a file exists."""
    path = Path(filepath)
    exists = path.exists()
    print_status(f"File '{filepath}' exists", exists)
    return exists

def check_module_installed(module_name: str):
    """Check if a Python module is installed."""
    try:
        __import__(module_name)
        print_status(f"Module '{module_name}' installed", True)
        return True
    except ImportError:
        print_status(f"Module '{module_name}' installed", False)
        return False

def run_test_conversion():
    """Run a test conversion with sample data."""
    try:
        import pandas as pd
        from csv_to_excel_converter import CSVtoExcelConverter
        
        # Create a simple test CSV in memory
        test_data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com']
        }
        df = pd.DataFrame(test_data)
        test_csv = Path('./test_verification.csv')
        df.to_csv(test_csv, index=False)
        
        # Try conversion
        converter = CSVtoExcelConverter(
            input_file=str(test_csv),
            output_file='./test_verification.xlsx'
        )
        
        success = converter.convert()
        
        # Cleanup
        test_csv.unlink(missing_ok=True)
        Path('./test_verification.xlsx').unlink(missing_ok=True)
        
        print_status("Test conversion successful", success)
        return success
    except Exception as e:
        print_status(f"Test conversion failed: {e}", False)
        return False

def main():
    """Run all verification checks."""
    print("\n" + "="*70)
    print("  CSV to Excel Converter - Verification")
    print("="*70 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Module: pandas", lambda: check_module_installed('pandas')),
        ("Module: openpyxl", lambda: check_module_installed('openpyxl')),
        ("File: csv_to_excel_converter.py", lambda: check_file_exists('csv_to_excel_converter.py')),
        ("File: sample_data.csv", lambda: check_file_exists('sample_data.csv')),
        ("File: column_mapping.json", lambda: check_file_exists('column_mapping.json')),
        ("File: requirements.txt", lambda: check_file_exists('requirements.txt')),
        ("File: CSV_EXCEL_CONVERTER_README.md", lambda: check_file_exists('CSV_EXCEL_CONVERTER_README.md')),
        ("File: GETTING_STARTED.md", lambda: check_file_exists('GETTING_STARTED.md')),
    ]
    
    results = {}
    for name, check_func in checks:
        print(f"\n{name}:")
        results[name] = check_func()
    
    print(f"\n\nTest Conversion:")
    test_result = run_test_conversion()
    results['Test Conversion'] = test_result
    
    print("\n" + "="*70)
    print("  Summary")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All checks passed! Ready to use.\n")
        print("Next steps:")
        print("  1. Read GETTING_STARTED.md for quick setup")
        print("  2. Run: python csv_to_excel_converter.py sample_data.csv")
        print("  3. For examples, run: python quickstart.py")
        print("  4. For help, run: python csv_to_excel_converter.py --help\n")
        return 0
    else:
        print("\n❌ Some checks failed. See above for details.\n")
        print("Troubleshooting:")
        print("  • Missing modules? Run: pip install -r requirements.txt")
        print("  • Missing files? Check file locations and names")
        print("  • Other issues? Check error messages above\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
