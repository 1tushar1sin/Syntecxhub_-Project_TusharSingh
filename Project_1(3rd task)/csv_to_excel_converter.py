"""
CSV to Excel Converter
Converts CSV files to Excel format with data cleaning, normalization, and error handling.
"""

import pandas as pd
import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, Dict
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CSVtoExcelConverter:
    """Handles CSV to Excel conversion with data cleaning and normalization."""
    
    def __init__(self, input_file: str, output_file: Optional[str] = None, 
                 config_file: Optional[str] = None):
        """
        Initialize the converter.
        
        Args:
            input_file: Path to the input CSV file
            output_file: Path to the output Excel file (optional)
            config_file: Path to JSON config file for column renaming (optional)
        """
        self.input_file = Path(input_file)
        self.output_file = Path(output_file) if output_file else None
        self.config_file = Path(config_file) if config_file else None
        self.df = None
        self.column_mapping = {}
        
    def validate_input_file(self) -> bool:
        """Validate that the input file exists and is readable."""
        if not self.input_file.exists():
            logger.error(f"Input file not found: {self.input_file}")
            return False
        if not self.input_file.suffix.lower() == '.csv':
            logger.error(f"File must be a CSV file. Got: {self.input_file.suffix}")
            return False
        if not self.input_file.is_file():
            logger.error(f"Input path is not a file: {self.input_file}")
            return False
        logger.info(f"Input file validated: {self.input_file}")
        return True
    
    def set_default_output_file(self):
        """Set default output file if not provided."""
        if self.output_file is None:
            self.output_file = self.input_file.with_suffix('.xlsx')
            logger.info(f"Output file not specified, using: {self.output_file}")
    
    def load_column_mapping(self):
        """Load column mapping from config file if provided."""
        if self.config_file and self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.column_mapping = json.load(f)
                logger.info(f"Column mapping loaded from {self.config_file}")
                logger.debug(f"Mapping: {self.column_mapping}")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in config file: {e}")
                return False
            except Exception as e:
                logger.error(f"Error loading config file: {e}")
                return False
        return True
    
    def read_csv(self, encoding: str = 'utf-8', skip_rows: int = 0) -> bool:
        """
        Read CSV file with error handling.
        
        Args:
            encoding: File encoding (default: utf-8)
            skip_rows: Number of rows to skip (default: 0)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info(f"Reading CSV file: {self.input_file}")
            self.df = pd.read_csv(self.input_file, encoding=encoding, skiprows=skip_rows)
            logger.info(f"Successfully read {len(self.df)} rows and {len(self.df.columns)} columns")
            logger.debug(f"Columns: {list(self.df.columns)}")
            return True
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error. Try a different encoding: {e}")
            return False
        except pd.errors.EmptyDataError:
            logger.error("CSV file is empty")
            return False
        except pd.errors.ParserError as e:
            logger.error(f"CSV parsing error: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to read CSV file: {e}")
            return False
    
    def handle_missing_values(self, strategy: str = 'show', fill_value=None, 
                              forward_fill: bool = False) -> bool:
        """
        Handle missing values in the dataset.
        
        Args:
            strategy: 'show' (log), 'drop' (remove rows), 'fill' (fill with value)
            fill_value: Value to fill missing cells with (for 'fill' strategy)
            forward_fill: Whether to use forward fill for NaN values
            
        Returns:
            bool: True if successful
        """
        if self.df is None:
            logger.error("No data loaded. Read CSV first.")
            return False
        
        missing_summary = self.df.isnull().sum()
        missing_total = missing_summary.sum()
        
        if missing_total > 0:
            logger.warning(f"Found {missing_total} missing values:")
            for col, count in missing_summary[missing_summary > 0].items():
                logger.warning(f"  {col}: {count} missing values")
            
            if strategy.lower() == 'show':
                logger.info("Keeping missing values in output")
            elif strategy.lower() == 'drop':
                initial_rows = len(self.df)
                self.df.dropna(inplace=True)
                logger.info(f"Dropped {initial_rows - len(self.df)} rows with missing values")
            elif strategy.lower() == 'fill':
                if fill_value is None:
                    logger.warning("No fill_value provided, using strategy='show' instead")
                else:
                    self.df.fillna(fill_value, inplace=True)
                    logger.info(f"Filled missing values with: {fill_value}")
            elif strategy.lower() == 'forward_fill':
                self.df.fillna(method='ffill', inplace=True)
                logger.info("Applied forward fill to missing values")
        else:
            logger.info("No missing values found")
        
        return True
    
    def parse_dates(self, date_columns: Optional[list] = None, 
                    infer_datetime_format: bool = True) -> bool:
        """
        Parse date columns.
        
        Args:
            date_columns: List of column names to parse as dates
            infer_datetime_format: Whether to infer datetime format
            
        Returns:
            bool: True if successful
        """
        if self.df is None:
            logger.error("No data loaded. Read CSV first.")
            return False
        
        try:
            if date_columns:
                for col in date_columns:
                    if col in self.df.columns:
                        self.df[col] = pd.to_datetime(
                            self.df[col], 
                            infer_datetime_format=infer_datetime_format,
                            errors='coerce'
                        )
                        logger.info(f"Parsed dates in column: {col}")
                    else:
                        logger.warning(f"Column not found for date parsing: {col}")
            else:
                # Auto-detect and parse date columns
                for col in self.df.columns:
                    try:
                        parsed = pd.to_datetime(self.df[col], infer_datetime_format=True, errors='coerce')
                        if parsed.notna().sum() > 0:
                            self.df[col] = parsed
                            logger.info(f"Auto-detected and parsed dates in column: {col}")
                    except:
                        pass
            return True
        except Exception as e:
            logger.error(f"Error parsing dates: {e}")
            return False
    
    def rename_columns(self, custom_mapping: Optional[Dict] = None) -> bool:
        """
        Rename columns using provided mapping or config file.
        
        Args:
            custom_mapping: Optional dictionary of {old_name: new_name}
            
        Returns:
            bool: True if successful
        """
        if self.df is None:
            logger.error("No data loaded. Read CSV first.")
            return False
        
        mapping = custom_mapping or self.column_mapping
        
        if mapping:
            try:
                self.df.rename(columns=mapping, inplace=True)
                logger.info(f"Renamed {len(mapping)} columns")
                for old, new in mapping.items():
                    logger.debug(f"  {old} -> {new}")
                return True
            except Exception as e:
                logger.error(f"Error renaming columns: {e}")
                return False
        else:
            logger.info("No column mapping provided, skipping rename")
            return True
    
    def clean_column_names(self, strip_whitespace: bool = True, 
                          lowercase: bool = False) -> bool:
        """
        Clean column names (strip whitespace, etc.).
        
        Args:
            strip_whitespace: Remove leading/trailing whitespace
            lowercase: Convert column names to lowercase
            
        Returns:
            bool: True if successful
        """
        if self.df is None:
            logger.error("No data loaded. Read CSV first.")
            return False
        
        try:
            original_cols = list(self.df.columns)
            
            if strip_whitespace:
                self.df.columns = self.df.columns.str.strip()
            
            if lowercase:
                self.df.columns = self.df.columns.str.lower()
            
            new_cols = list(self.df.columns)
            if original_cols != new_cols:
                logger.info("Column names cleaned")
                logger.debug(f"Changes: {[(o, n) for o, n in zip(original_cols, new_cols) if o != n]}")
            
            return True
        except Exception as e:
            logger.error(f"Error cleaning column names: {e}")
            return False
    
    def remove_duplicates(self, subset: Optional[list] = None) -> bool:
        """
        Remove duplicate rows.
        
        Args:
            subset: Column names to consider for identifying duplicates
            
        Returns:
            bool: True if successful
        """
        if self.df is None:
            logger.error("No data loaded. Read CSV first.")
            return False
        
        try:
            initial_rows = len(self.df)
            self.df.drop_duplicates(subset=subset, inplace=True)
            removed = initial_rows - len(self.df)
            
            if removed > 0:
                logger.info(f"Removed {removed} duplicate rows")
            else:
                logger.info("No duplicate rows found")
            
            return True
        except Exception as e:
            logger.error(f"Error removing duplicates: {e}")
            return False
    
    def export_to_excel(self, sheet_name: str = 'Data', 
                       include_index: bool = False,
                       freeze_panes: tuple = (1, 0)) -> bool:
        """
        Export data to Excel file.
        
        Args:
            sheet_name: Name of the Excel sheet
            include_index: Whether to include the index column
            freeze_panes: Tuple (row, col) for freezing panes
            
        Returns:
            bool: True if successful
        """
        if self.df is None:
            logger.error("No data loaded. Read CSV first.")
            return False
        
        try:
            # Create output directory if it doesn't exist
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Exporting to Excel: {self.output_file}")
            
            with pd.ExcelWriter(self.output_file, engine='openpyxl') as writer:
                self.df.to_excel(writer, sheet_name=sheet_name, index=include_index)
                
                # Freeze panes if openpyxl is available
                if freeze_panes and freeze_panes != (0, 0):
                    try:
                        from openpyxl import load_workbook
                        workbook = writer.book
                        worksheet = writer.sheets[sheet_name]
                        worksheet.freeze_panes = f'{freeze_panes[0] + 1}{chr(65 + freeze_panes[1])}'
                        logger.debug(f"Froze panes at {freeze_panes}")
                    except Exception as e:
                        logger.warning(f"Could not freeze panes: {e}")
            
            logger.info(f"Successfully exported to {self.output_file}")
            logger.info(f"File size: {self.output_file.stat().st_size / 1024:.2f} KB")
            return True
        except Exception as e:
            logger.error(f"Failed to export to Excel: {e}")
            return False
    
    def convert(self, missing_value_strategy: str = 'show', 
                parse_dates_auto: bool = True,
                clean_names: bool = True,
                remove_dups: bool = False) -> bool:
        """
        Execute the complete conversion process.
        
        Args:
            missing_value_strategy: Strategy for handling missing values
            parse_dates_auto: Whether to auto-detect and parse dates
            clean_names: Whether to clean column names
            remove_dups: Whether to remove duplicate rows
            
        Returns:
            bool: True if successful
        """
        logger.info("=" * 60)
        logger.info("Starting CSV to Excel Conversion")
        logger.info("=" * 60)
        
        if not self.validate_input_file():
            return False
        
        self.set_default_output_file()
        
        if not self.load_column_mapping():
            return False
        
        if not self.read_csv():
            return False
        
        if clean_names and not self.clean_column_names(strip_whitespace=True):
            return False
        
        if not self.handle_missing_values(strategy=missing_value_strategy):
            return False
        
        if parse_dates_auto and not self.parse_dates():
            return False
        
        if not self.rename_columns():
            return False
        
        if remove_dups and not self.remove_duplicates():
            return False
        
        if not self.export_to_excel():
            return False
        
        logger.info("=" * 60)
        logger.info("Conversion completed successfully!")
        logger.info("=" * 60)
        return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Convert CSV files to Excel format with data cleaning and normalization.',
        epilog='''
Examples:
  python csv_to_excel_converter.py input.csv
  python csv_to_excel_converter.py input.csv -o output.xlsx
  python csv_to_excel_converter.py input.csv -c columns.json
  python csv_to_excel_converter.py input.csv --missing-strategy drop --remove-duplicates
        '''
    )
    
    parser.add_argument(
        'input_file',
        help='Path to the input CSV file'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Path to the output Excel file (default: same name as input with .xlsx extension)',
        default=None
    )
    
    parser.add_argument(
        '-c', '--config',
        help='Path to JSON config file for column mapping',
        default=None
    )
    
    parser.add_argument(
        '--missing-strategy',
        choices=['show', 'drop', 'fill', 'forward_fill'],
        default='show',
        help='Strategy for handling missing values (default: show)'
    )
    
    parser.add_argument(
        '--parse-dates',
        action='store_true',
        default=True,
        help='Auto-detect and parse date columns (default: True)'
    )
    
    parser.add_argument(
        '--no-parse-dates',
        action='store_false',
        dest='parse_dates',
        help='Disable date parsing'
    )
    
    parser.add_argument(
        '--clean-names',
        action='store_true',
        default=True,
        help='Clean column names by stripping whitespace (default: True)'
    )
    
    parser.add_argument(
        '--no-clean-names',
        action='store_false',
        dest='clean_names',
        help='Disable column name cleaning'
    )
    
    parser.add_argument(
        '-r', '--remove-duplicates',
        action='store_true',
        help='Remove duplicate rows'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    converter = CSVtoExcelConverter(
        input_file=args.input_file,
        output_file=args.output,
        config_file=args.config
    )
    
    success = converter.convert(
        missing_value_strategy=args.missing_strategy,
        parse_dates_auto=args.parse_dates,
        clean_names=args.clean_names,
        remove_dups=args.remove_duplicates
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
