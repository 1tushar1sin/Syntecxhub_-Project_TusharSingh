# CSV to Excel Converter

A comprehensive command-line tool for converting CSV files to Excel format with built-in data cleaning, normalization, and error handling.

## Features

✨ **Data Cleaning & Normalization**
- Handle missing values (show, drop, fill, forward fill strategies)
- Auto-detect and parse date columns
- Clean column names (strip whitespace, etc.)
- Remove duplicate rows
- Custom column renaming via JSON config

🔧 **CLI Interface**
- Simple command-line flags for customization
- Input and output file specification
- Config file support for column mapping
- Verbose logging for debugging

📊 **Data Processing**
- Support for large CSV files via pandas
- Openpyxl integration for Excel formatting
- Freeze panes support for better readability
- Proper error handling and logging

## Installation

### Requirements
- Python 3.7+
- pandas
- openpyxl

### Setup

```bash
# Install required packages
pip install pandas openpyxl
```

## Usage

### Basic Usage

Convert a CSV file to Excel with default settings:

```bash
python csv_to_excel_converter.py input.csv
```

Output: `input.xlsx` (same directory as input)

### Specify Output File

```bash
python csv_to_excel_converter.py input.csv -o output.xlsx
```

Or with long flag:

```bash
python csv_to_excel_converter.py input.csv --output output.xlsx
```

### Handle Missing Values

Drop rows with any missing values:

```bash
python csv_to_excel_converter.py input.csv --missing-strategy drop
```

Options:
- `show` (default): Keep missing values in output
- `drop`: Remove rows with missing values
- `fill`: Fill with a specified value (requires additional implementation)
- `forward_fill`: Use previous value to fill missing data

### Remove Duplicates

```bash
python csv_to_excel_converter.py input.csv --remove-duplicates
```

### Column Mapping / Renaming

Create a `column_mapping.json` file:

```json
{
  "Old Column Name": "New Column Name",
  "First Name": "FirstName",
  "Email Address": "Email",
  "Created Date": "CreatedDate"
}
```

Use it during conversion:

```bash
python csv_to_excel_converter.py input.csv -c column_mapping.json
```

### Date Parsing

By default, dates are automatically detected and parsed. To disable:

```bash
python csv_to_excel_converter.py input.csv --no-parse-dates
```

### Column Name Cleaning

By default, column names are cleaned (whitespace stripped). To disable:

```bash
python csv_to_excel_converter.py input.csv --no-clean-names
```

### Verbose Logging

Enable detailed logging for debugging:

```bash
python csv_to_excel_converter.py input.csv -v
```

Or:

```bash
python csv_to_excel_converter.py input.csv --verbose
```

## Examples

### Example 1: Complete Processing

```bash
python csv_to_excel_converter.py sales.csv -o sales_clean.xlsx \
  -c column_mapping.json \
  --missing-strategy drop \
  --remove-duplicates \
  -v
```

This will:
1. Read `sales.csv`
2. Clean column names
3. Auto-detect and parse dates
4. Drop rows with missing values
5. Remove duplicate rows
6. Rename columns using mapping
7. Export to `sales_clean.xlsx`
8. Show verbose logging

### Example 2: Simple Conversion

```bash
python csv_to_excel_converter.py data.csv
```

Creates `data.xlsx` with:
- Missing values preserved
- Auto-detected dates
- Cleaned column names
- No duplicates removed

### Example 3: With Custom Column Mapping

Create `mapping.json`:
```json
{
  "product_name": "Product",
  "unit_price": "Price",
  "qty_sold": "Quantity",
  "order_date": "Date"
}
```

Run:
```bash
python csv_to_excel_converter.py orders.csv -o orders_processed.xlsx -c mapping.json
```

## Sample CSV File

A `sample_data.csv` file is included with:
- Mixed data types (text, numeric, dates)
- Missing values
- Extra whitespace in column names
- Duplicate rows
- Inconsistent date formats

Test with:
```bash
python csv_to_excel_converter.py sample_data.csv -o sample_output.xlsx \
  -c column_mapping.json \
  --missing-strategy drop \
  --remove-duplicates \
  -v
```

## CLI Help

View all available options:

```bash
python csv_to_excel_converter.py --help
```

Output:
```
usage: csv_to_excel_converter.py [-h] [-o OUTPUT] [-c CONFIG]
                                [--missing-strategy {show,drop,fill,forward_fill}]
                                [--parse-dates] [--no-parse-dates]
                                [--clean-names] [--no-clean-names]
                                [-r] [-v]
                                input_file

Convert CSV files to Excel format with data cleaning and normalization.

positional arguments:
  input_file            Path to the input CSV file

optional arguments:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Path to the output Excel file (default: same name as
                        input with .xlsx extension)
  -c, --config CONFIG   Path to JSON config file for column mapping
  --missing-strategy {show,drop,fill,forward_fill}
                        Strategy for handling missing values (default: show)
  --parse-dates         Auto-detect and parse date columns (default: True)
  --no-parse-dates      Disable date parsing
  --clean-names         Clean column names by stripping whitespace (default:
                        True)
  --no-clean-names      Disable column name cleaning
  -r, --remove-duplicates
                        Remove duplicate rows
  -v, --verbose         Enable verbose logging
```

## Logging

The tool provides comprehensive logging:

**INFO Level** (default):
- File validation
- Data statistics (rows, columns)
- Missing values summary
- Processing steps completed
- Export confirmation and file size

**DEBUG Level** (with `-v` flag):
- Column lists
- Column mapping details
- Column name changes
- Detailed transformation steps

Example log output:
```
2024-02-15 10:30:45,123 - INFO - ============================================================
2024-02-15 10:30:45,123 - INFO - Starting CSV to Excel Conversion
2024-02-15 10:30:45,123 - INFO - ============================================================
2024-02-15 10:30:45,124 - INFO - Input file validated: sample_data.csv
2024-02-15 10:30:45,125 - INFO - Output file not specified, using: sample_data.xlsx
2024-02-15 10:30:45,156 - INFO - Reading CSV file: sample_data.csv
2024-02-15 10:30:45,168 - INFO - Successfully read 11 rows and 7 columns
2024-02-15 10:30:45,169 - INFO - Column names cleaned
2024-02-15 10:30:45,170 - WARNING - Found 4 missing values:
2024-02-15 10:30:45,170 - WARNING -   Phone Number: 2 missing values
2024-02-15 10:30:45,170 - WARNING -   Last Updated: 2 missing values
2024-02-15 10:30:45,170 - WARNING -   Sales Amount: 1 missing values
2024-02-15 10:30:45,170 - INFO - Keeping missing values in output
2024-02-15 10:30:45,189 - INFO - Auto-detected and parsed dates in column: Created Date
2024-02-15 10:30:45,190 - INFO - Auto-detected and parsed dates in column: Last Updated
2024-02-15 10:30:45,191 - INFO - Renamed 7 columns
2024-02-15 10:30:45,192 - INFO - No duplicate rows found
2024-02-15 10:30:45,195 - INFO - Exporting to Excel: sample_data.xlsx
2024-02-15 10:30:45,234 - INFO - Successfully exported to sample_data.xlsx
2024-02-15 10:30:45,234 - INFO - File size: 5.23 KB
2024-02-15 10:30:45,234 - INFO - ============================================================
2024-02-15 10:30:45,234 - INFO - Conversion completed successfully!
2024-02-15 10:30:45,234 - INFO - ============================================================
```

## Error Handling

The tool handles various error scenarios:

| Error | Example | Solution |
|-------|---------|----------|
| File not found | `input.csv` doesn't exist | Check file path |
| Wrong file type | `.txt` instead of `.csv` | Use CSV format |
| Invalid encoding | Special characters fail | Tool tries UTF-8 by default |
| Empty CSV | 0 rows | Check CSV content |
| Invalid JSON config | Malformed `column_mapping.json` | Fix JSON syntax |
| Missing columns | Column doesn't exist in CSV | Fix column names in config |

## Use Cases

📈 **Business Analytics**
- Prepare sales data for Excel reports
- Clean customer databases before import
- Standardize date formats

📊 **Data Preparation**
- Normalize raw data dumps
- Remove duplicate records
- Handle missing values before analysis

🔄 **Automation**
- Batch process multiple CSV files
- Integrate into data pipelines
- Automate data export workflows

## Architecture

The converter is built with a class-based design:

```
CSVtoExcelConverter
├── validate_input_file()      # Validate input CSV
├── read_csv()                 # Load CSV with pandas
├── handle_missing_values()    # Process NaN values
├── parse_dates()              # Detect and parse dates
├── clean_column_names()       # Normalize column names
├── rename_columns()           # Apply custom mapping
├── remove_duplicates()        # Deduplicate rows
├── export_to_excel()          # Write to .xlsx files
└── convert()                  # Orchestrate full workflow
```

## Troubleshooting

### "Module not found" error

```bash
pip install pandas openpyxl
```

### "Input file not found"

Check the file path is correct:
```bash
# List files to verify
dir sample_data.csv
```

### Excel file already exists

The tool will overwrite existing files. Back up important files first.

### Memory issues with large files

For very large CSV files:
1. Try increasing available RAM
2. Process smaller chunks manually
3. Use `--missing-strategy drop` to reduce rows

## Advanced Usage

### Creating a Reusable Script

```python
from csv_to_excel_converter import CSVtoExcelConverter

# Custom processing
converter = CSVtoExcelConverter(
    input_file='data.csv',
    output_file='data_clean.xlsx',
    config_file='mapping.json'
)

converter.convert(
    missing_value_strategy='drop',
    parse_dates_auto=True,
    clean_names=True,
    remove_dups=True
)
```

### Programmatic Usage

```python
converter = CSVtoExcelConverter('input.csv', 'output.xlsx')
converter.read_csv()
converter.clean_column_names(strip_whitespace=True, lowercase=False)
converter.handle_missing_values(strategy='drop')
converter.parse_dates()
converter.remove_duplicates()
converter.export_to_excel()
```

## License

Free to use for personal and commercial projects.

## Support

For issues or questions, check the log output with `-v` (verbose) flag for detailed debugging information.
