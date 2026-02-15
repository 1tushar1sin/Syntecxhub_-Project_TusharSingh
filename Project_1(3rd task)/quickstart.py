#!/usr/bin/env python3
"""
Quick Start Examples for CSV to Excel Converter
Run this file to see examples of different conversion scenarios.
"""

import subprocess
import sys
from pathlib import Path

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def run_example(description, command):
    """Run a command and show output."""
    print(f"📌 {description}")
    print(f"Command: {command}\n")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            print("✅ Success!\n")
        else:
            print("❌ Failed!\n")
    except Exception as e:
        print(f"Error running command: {e}\n")

def main():
    """Run quick start examples."""
    
    script_path = Path(__file__).parent / "csv_to_excel_converter.py"
    sample_csv = Path(__file__).parent / "sample_data.csv"
    mapping_json = Path(__file__).parent / "column_mapping.json"
    
    # Check if required files exist
    if not script_path.exists():
        print("❌ csv_to_excel_converter.py not found!")
        sys.exit(1)
    
    if not sample_csv.exists():
        print("❌ sample_data.csv not found!")
        sys.exit(1)
    
    print_section("CSV to Excel Converter - Quick Start Examples")
    
    # Example 1: Basic conversion
    run_example(
        "Example 1: Basic Conversion (default settings)",
        f"python {script_path} {sample_csv}"
    )
    
    # Example 2: Specify output file
    run_example(
        "Example 2: Specify Output File",
        f"python {script_path} {sample_csv} -o sample_output.xlsx"
    )
    
    # Example 3: Drop missing values
    run_example(
        "Example 3: Drop Rows with Missing Values",
        f"python {script_path} {sample_csv} -o sample_no_missing.xlsx --missing-strategy drop"
    )
    
    # Example 4: Remove duplicates
    run_example(
        "Example 4: Remove Duplicate Rows",
        f"python {script_path} {sample_csv} -o sample_no_duplicates.xlsx --remove-duplicates"
    )
    
    # Example 5: With column mapping (if mapping file exists)
    if mapping_json.exists():
        run_example(
            "Example 5: Apply Column Mapping",
            f"python {script_path} {sample_csv} -o sample_mapped.xlsx -c {mapping_json}"
        )
    
    # Example 6: Full processing
    run_example(
        "Example 6: Full Processing (all features)",
        f"python {script_path} {sample_csv} -o sample_complete.xlsx "
        f"-c {mapping_json} --missing-strategy drop --remove-duplicates"
    )
    
    # Example 7: Verbose logging
    run_example(
        "Example 7: With Verbose Logging",
        f"python {script_path} {sample_csv} -o sample_verbose.xlsx -v"
    )
    
    print_section("Available Commands")
    print("View full help:")
    print(f"  python {script_path} --help\n")
    
    print_section("Summary")
    print("""
✨ Key Features Used in Examples:
  • Basic conversion with auto-detection
  • Custom output file specification
  • Missing data handling strategies
  • Duplicate row removal
  • Column name mapping and renaming
  • Comprehensive logging

📊 Generated Files:
  • sample_data.xlsx              (Example 1)
  • sample_output.xlsx            (Example 2)
  • sample_no_missing.xlsx        (Example 3)
  • sample_no_duplicates.xlsx     (Example 4)
  • sample_mapped.xlsx            (Example 5)
  • sample_complete.xlsx          (Example 6)
  • sample_verbose.xlsx           (Example 7)

🎯 Next Steps:
  1. Check the generated .xlsx files in Excel
  2. Review the README for detailed documentation
  3. Customize column_mapping.json for your data
  4. Integrate into your automation scripts
    """)

if __name__ == "__main__":
    main()
