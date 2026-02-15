# CSV to Excel Converter - Installation & Getting Started

## 🚀 Quick Setup (5 minutes)

### Step 1: Verify Python Installation

```bash
python --version
```

Make sure you have Python 3.7 or higher.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pandas openpyxl
```

### Step 3: Test with Sample Data

```bash
python csv_to_excel_converter.py sample_data.csv
```

You should see `sample_data.xlsx` created in the same directory.

---

## 📖 First Conversion

### Basic Usage (Recommended for beginners)

```bash
python csv_to_excel_converter.py your_file.csv
```

This will create `your_file.xlsx` with:
- ✅ Missing values preserved
- ✅ Dates auto-detected
- ✅ Column names cleaned
- ✅ Proper formatting

### See What Happened

Enable verbose logging to understand the conversion:

```bash
python csv_to_excel_converter.py your_file.csv -v
```

---

## 🔧 Common Tasks

### Task 1: Remove Empty Rows

```bash
python csv_to_excel_converter.py your_file.csv --missing-strategy drop
```

### Task 2: Remove Duplicate Records

```bash
python csv_to_excel_converter.py your_file.csv --remove-duplicates
```

### Task 3: Rename Columns

Create `column_mapping.json`:
```json
{
  "old_name": "new_name",
  "old_name2": "new_name2"
}
```

Then run:
```bash
python csv_to_excel_converter.py your_file.csv -c column_mapping.json
```

### Task 4: Specify Output Location

```bash
python csv_to_excel_converter.py input.csv -o /path/to/output.xlsx
```

### Task 5: Complete Processing

```bash
python csv_to_excel_converter.py input.csv \
  -o output.xlsx \
  -c column_mapping.json \
  --missing-strategy drop \
  --remove-duplicates \
  -v
```

---

## 📁 File Structure

```
csv_to_excel_converter/
├── csv_to_excel_converter.py       # Main script
├── quickstart.py                    # Quick start with examples
├── examples.py                      # Programmatic usage examples
├── requirements.txt                 # Python dependencies
├── column_mapping.json              # Column rename config (example)
├── sample_data.csv                  # Sample CSV file
├── CSV_EXCEL_CONVERTER_README.md    # Full documentation
├── GETTING_STARTED.md              # This file
└── output files (generated)
    ├── sample_data.xlsx
    ├── output.xlsx
    └── ... (various outputs)
```

---

## 🎯 Common Scenarios

### Scenario 1: Clean Customer Data

```bash
# Remove rows with missing email/phone
python csv_to_excel_converter.py customers.csv \
  --missing-strategy drop \
  --remove-duplicates \
  -o customers_clean.xlsx
```

### Scenario 2: Sales Report Preparation

```bash
# Rename columns, clean dates, remove duds
python csv_to_excel_converter.py sales.csv \
  -c sales_mapping.json \
  -o sales_report.xlsx
```

### Scenario 3: Data Import Preview

```bash
# Just convert, see what we have
python csv_to_excel_converter.py raw_data.csv -v
```

---

## ✅ Verify Setup is Working

Run the test suite:

```bash
python csv_to_excel_converter.py sample_data.csv -o test_output.xlsx -v
```

Expected output:
```
2024-02-15 10:30:45,123 - INFO - Starting CSV to Excel Conversion
2024-02-15 10:30:45,124 - INFO - Input file validated: sample_data.csv
2024-02-15 10:30:45,156 - INFO - Successfully read 11 rows and 7 columns
...
2024-02-15 10:30:45,234 - INFO - Conversion completed successfully!
```

✅ If you see "Conversion completed successfully!", you're all set!

---

## 🐛 Troubleshooting

### Error: "No module named 'pandas'"

Install dependencies:
```bash
pip install -r requirements.txt
```

### Error: "Input file not found"

Make sure the CSV file exists in your current directory:
```bash
# List files
dir                              # Windows
ls                               # Mac/Linux

# Check specific file
dir sample_data.csv              # Windows
ls sample_data.csv               # Mac/Linux
```

### Error: "ModuleNotFoundError: No module named 'openpyxl'"

Install openpyxl:
```bash
pip install openpyxl
```

### CSV file converted but looks wrong

Check with verbose mode:
```bash
python csv_to_excel_converter.py your_file.csv -v
```

This shows:
- ✓ Number of rows/columns read
- ✓ Missing values found
- ✓ Date columns detected
- ✓ Any warnings or errors

---

## 💡 Pro Tips

**Tip 1: Handle Large Files**
For very large CSV files (100MB+), the script may be slow but will work. Use:
```bash
python csv_to_excel_converter.py huge_file.csv --no-parse-dates
```

**Tip 2: Different Encodings**
If you get encoding errors, the tool tries UTF-8 by default. For other encodings, you may need to edit the script and pass `encoding='latin-1'` to `read_csv()`.

**Tip 3: Batch Processing**
Process multiple files:
```bash
for file in *.csv; do
  python csv_to_excel_converter.py "$file"
done
```

**Tip 4: Create Column Mapping**
Use Python to generate column mapping:
```python
import pandas as pd
import json

df = pd.read_csv('your_file.csv')
mapping = {col: col.replace(' ', '_').lower() for col in df.columns}

with open('column_mapping.json', 'w') as f:
    json.dump(mapping, f, indent=2)
```

---

## 📚 Next Steps

1. ✅ **Run the sample**: `python csv_to_excel_converter.py sample_data.csv`
2. 📖 **Read the README**: Open `CSV_EXCEL_CONVERTER_README.md` for full documentation
3. 🔧 **Try examples**: Run `python examples.py` for programmatic usage
4. 🚀 **Process your data**: Use the tool with your own CSV files
5. 💾 **Integrate**: Use in your Python scripts via the class interface

---

## 🎓 Learning Resources

### Understanding Options

- `--missing-strategy` - How to handle empty cells
  - `show` - Keep them (default)
  - `drop` - Remove entire row
  - `fill` - Replace with a value
  - `forward_fill` - Use previous value

- `--parse-dates` - Auto-find and fix date columns
  - Default: ON
  - Use `--no-parse-dates` to turn off

- `--clean-names` - Fix column header spacing
  - Default: ON
  - Use `--no-clean-names` to turn off

- `-c, --config` - Column renaming configuration
  - Use JSON file for mapping

- `-v, --verbose` - Show detailed processing info
  - Good for debugging

---

## 🤝 Getting Help

1. **Check the logs**: Run with `-v` flag
2. **Check the README**: Full documentation in `CSV_EXCEL_CONVERTER_README.md`
3. **Review examples**: Run `python examples.py`
4. **Test with sample**: Use `sample_data.csv` to test features

---

## ⚡ Performance

- **Small files** (<5MB): < 1 second
- **Medium files** (5-50MB): 1-5 seconds
- **Large files** (50-500MB): 10-60 seconds
- **Very large files** (>500MB): May need several minutes

For better performance on huge files, disable date parsing:
```bash
python csv_to_excel_converter.py huge_file.csv --no-parse-dates
```

---

Enjoy! 🎉 Start converting your CSV files to Excel today!
