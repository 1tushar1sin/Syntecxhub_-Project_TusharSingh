"""
Programmatic Usage Examples for CSV to Excel Converter
Shows how to use the converter in your own Python scripts.
"""

import logging
from csv_to_excel_converter import CSVtoExcelConverter
from pathlib import Path

# Enable detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def example_1_basic_conversion():
    """Example 1: Basic conversion with minimal options."""
    print("\n" + "="*70)
    print("  Example 1: Basic Conversion")
    print("="*70)
    
    converter = CSVtoExcelConverter(
        input_file='sample_data.csv',
        output_file='example1_basic.xlsx'
    )
    
    converter.convert()
    

def example_2_with_column_mapping():
    """Example 2: Conversion with column name mapping."""
    print("\n" + "="*70)
    print("  Example 2: With Column Mapping")
    print("="*70)
    
    converter = CSVtoExcelConverter(
        input_file='sample_data.csv',
        output_file='example2_mapped.xlsx',
        config_file='column_mapping.json'
    )
    
    converter.convert()


def example_3_drop_missing_values():
    """Example 3: Conversion with missing value handling."""
    print("\n" + "="*70)
    print("  Example 3: Drop Rows with Missing Values")
    print("="*70)
    
    converter = CSVtoExcelConverter(
        input_file='sample_data.csv',
        output_file='example3_no_missing.xlsx'
    )
    
    converter.convert(missing_value_strategy='drop')


def example_4_remove_duplicates():
    """Example 4: Conversion with duplicate removal."""
    print("\n" + "="*70)
    print("  Example 4: Remove Duplicates")
    print("="*70)
    
    converter = CSVtoExcelConverter(
        input_file='sample_data.csv',
        output_file='example4_no_dups.xlsx'
    )
    
    converter.convert(remove_dups=True)


def example_5_full_processing():
    """Example 5: Full processing with all features."""
    print("\n" + "="*70)
    print("  Example 5: Full Processing")
    print("="*70)
    
    converter = CSVtoExcelConverter(
        input_file='sample_data.csv',
        output_file='example5_complete.xlsx',
        config_file='column_mapping.json'
    )
    
    converter.convert(
        missing_value_strategy='drop',
        parse_dates_auto=True,
        clean_names=True,
        remove_dups=True
    )


def example_6_custom_processing():
    """Example 6: Custom step-by-step processing."""
    print("\n" + "="*70)
    print("  Example 6: Custom Processing Steps")
    print("="*70)
    
    converter = CSVtoExcelConverter(
        input_file='sample_data.csv',
        output_file='example6_custom.xlsx'
    )
    
    # Step 1: Validate and read
    if not converter.validate_input_file():
        return
    
    converter.set_default_output_file()
    
    if not converter.read_csv():
        return
    
    # Step 2: Clean names
    converter.clean_column_names(strip_whitespace=True, lowercase=False)
    
    # Step 3: Handle missing values
    converter.handle_missing_values(strategy='drop')
    
    # Step 4: Parse dates
    converter.parse_dates()
    
    # Step 5: Remove duplicates
    converter.remove_duplicates()
    
    # Step 6: Rename columns
    converter.load_column_mapping()
    converter.rename_columns()
    
    # Step 7: Export
    converter.export_to_excel(
        sheet_name='ProcessedData',
        include_index=False,
        freeze_panes=(1, 0)
    )


def example_7_multiple_files():
    """Example 7: Process multiple CSV files."""
    print("\n" + "="*70)
    print("  Example 7: Process Multiple Files")
    print("="*70)
    
    input_dir = Path('.')
    csv_files = list(input_dir.glob('*.csv'))
    
    if not csv_files:
        print("No CSV files found in current directory")
        return
    
    for i, csv_file in enumerate(csv_files, 1):
        output_file = csv_file.with_suffix('.xlsx')
        
        print(f"\nProcessing file {i}/{len(csv_files)}: {csv_file.name}")
        
        converter = CSVtoExcelConverter(
            input_file=str(csv_file),
            output_file=str(output_file)
        )
        
        converter.convert(
            missing_value_strategy='show',
            parse_dates_auto=True,
            clean_names=True,
            remove_dups=False
        )


def example_8_error_handling():
    """Example 8: Error handling and logging."""
    print("\n" + "="*70)
    print("  Example 8: Error Handling")
    print("="*70)
    
    # Try to convert a non-existent file
    print("\nAttempting to convert non-existent file:")
    converter = CSVtoExcelConverter(
        input_file='nonexistent.csv',
        output_file='nonexistent.xlsx'
    )
    
    success = converter.convert()
    if not success:
        print("❌ Conversion failed (as expected for missing file)")
    
    # Try with invalid CSV file
    print("\nError handling works for:")
    print("  • Missing input files")
    print("  • Invalid file formats")
    print("  • Encoding errors")
    print("  • Malformed CSV data")
    print("  • Invalid column mappings")


def example_9_verbose_logging():
    """Example 9: Enable verbose logging for debugging."""
    print("\n" + "="*70)
    print("  Example 9: Verbose Logging")
    print("="*70)
    
    # Set logging to DEBUG level
    logging.getLogger().setLevel(logging.DEBUG)
    
    converter = CSVtoExcelConverter(
        input_file='sample_data.csv',
        output_file='example9_debug.xlsx',
        config_file='column_mapping.json'
    )
    
    converter.convert(
        missing_value_strategy='drop',
        parse_dates_auto=True,
        clean_names=True,
        remove_dups=True
    )
    
    # Reset logging
    logging.getLogger().setLevel(logging.INFO)


def main():
    """Run all examples."""
    
    print("\n" + "="*70)
    print("  CSV to Excel Converter - Programmatic Usage Examples")
    print("="*70)
    
    examples = [
        ("Example 1: Basic", example_1_basic_conversion),
        ("Example 2: With Mapping", example_2_with_column_mapping),
        ("Example 3: Drop Missing", example_3_drop_missing_values),
        ("Example 4: Remove Dups", example_4_remove_duplicates),
        ("Example 5: Full Processing", example_5_full_processing),
        ("Example 6: Custom Steps", example_6_custom_processing),
        ("Example 7: Multiple Files", example_7_multiple_files),
        ("Example 8: Error Handling", example_8_error_handling),
        ("Example 9: Verbose Logging", example_9_verbose_logging),
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nEnter example number to run (1-9), or press Enter to run all:")
    try:
        user_input = input(">>> ").strip()
        
        if user_input == "":
            # Run all
            for name, example_func in examples:
                try:
                    example_func()
                except Exception as e:
                    print(f"❌ Error in {name}: {e}")
        else:
            example_num = int(user_input)
            if 1 <= example_num <= len(examples):
                example_func = examples[example_num - 1][1]
                example_func()
            else:
                print(f"❌ Invalid example number. Please enter 1-{len(examples)}")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n" + "="*70)
    print("  Examples Complete!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
