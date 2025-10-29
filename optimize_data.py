#!/usr/bin/env python3
"""
FIFA Data Optimization Script

This script fixes data quality and performance issues in FIFA CSV files:
1. Standardizes encoding to UTF-8 without BOM
2. Fixes character encoding corruption
3. Standardizes delimiters to comma
4. Standardizes line endings to Unix (\n)
5. Removes HTML tags from data fields
6. Optionally removes URL columns to reduce file size

Usage:
    python3 optimize_data.py [--remove-urls] [--backup]
    
Options:
    --remove-urls    Remove Photo, Flag, and Club Logo URL columns
    --backup         Create backup of original files
"""

import csv
import re
import os
import sys
import shutil
from pathlib import Path


def detect_delimiter(file_path):
    """Detect the delimiter used in a CSV file."""
    with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        first_line = f.readline()
        if first_line.count(';') > first_line.count(','):
            return ';'
        return ','


def clean_html_tags(text):
    """Remove HTML tags from text."""
    if not isinstance(text, str):
        return text
    # Remove HTML tags but keep the content
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


def fix_encoding(text):
    """Fix common encoding corruption issues."""
    if not isinstance(text, str):
        return text
    
    # Common character corruption fixes
    replacements = {
        'M-|': 'ü',  # München
        'M-^': 'ô',  # Côte
        'M-sn': 'ón', # División
        'M-,': 'é',  # Common accent
        'M-3': 'ó',  # ó
        '�': '',     # Remove replacement character
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def optimize_csv_file(input_file, output_file, remove_urls=False):
    """
    Optimize a CSV file by fixing encoding, delimiters, and data quality issues.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        remove_urls: Whether to remove URL columns
    """
    print(f"Processing {input_file}...")
    
    # Detect input delimiter
    input_delimiter = detect_delimiter(input_file)
    output_delimiter = ','  # Standardize to comma
    
    # Columns to remove if remove_urls is True
    url_columns = {'Photo', 'Flag', 'Club Logo'}
    
    rows_processed = 0
    
    try:
        # Read with error handling for encoding issues
        with open(input_file, 'r', encoding='utf-8-sig', errors='ignore') as infile:
            reader = csv.DictReader(infile, delimiter=input_delimiter)
            
            # Filter headers if removing URLs
            if remove_urls:
                fieldnames = [h for h in reader.fieldnames if h not in url_columns]
            else:
                fieldnames = reader.fieldnames
            
            # Write with clean UTF-8 encoding and Unix line endings
            with open(output_file, 'w', encoding='utf-8', newline='\n') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=output_delimiter, 
                                       extrasaction='ignore')  # Ignore extra fields
                writer.writeheader()
                
                for row in reader:
                    rows_processed += 1
                    
                    # Process each field
                    cleaned_row = {}
                    for key, value in row.items():
                        # Skip None keys (extra fields) and URL columns if requested
                        if key is None:
                            continue
                        if remove_urls and key in url_columns:
                            continue
                        
                        # Clean the value
                        if value:
                            value = clean_html_tags(value)
                            value = fix_encoding(value)
                        
                        cleaned_row[key] = value
                    
                    writer.writerow(cleaned_row)
                    
                    if rows_processed % 1000 == 0:
                        print(f"  Processed {rows_processed} rows...")
        
        print(f"  Completed: {rows_processed} rows processed")
        
        # Report file size change
        original_size = os.path.getsize(input_file)
        new_size = os.path.getsize(output_file)
        reduction = (1 - new_size / original_size) * 100
        
        print(f"  Size: {original_size:,} bytes -> {new_size:,} bytes ({reduction:.1f}% reduction)")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return False


def main():
    """Main function to process all FIFA CSV files."""
    # Parse command line arguments
    remove_urls = '--remove-urls' in sys.argv
    create_backup = '--backup' in sys.argv
    
    print("FIFA Data Optimization Script")
    print("=" * 50)
    print(f"Remove URLs: {remove_urls}")
    print(f"Create backup: {create_backup}")
    print()
    
    # Find all FIFA CSV files
    csv_files = sorted([f for f in os.listdir('.') if f.startswith('FIFA') and f.endswith('.csv')])
    
    if not csv_files:
        print("No FIFA CSV files found in current directory.")
        return
    
    print(f"Found {len(csv_files)} CSV files to process")
    print()
    
    # Create backup directory if requested
    if create_backup:
        backup_dir = 'original_data_backup'
        os.makedirs(backup_dir, exist_ok=True)
        print(f"Backing up original files to {backup_dir}/")
    
    # Process each file
    success_count = 0
    for csv_file in csv_files:
        # Backup original if requested
        if create_backup:
            backup_path = os.path.join(backup_dir, csv_file)
            shutil.copy2(csv_file, backup_path)
        
        # Create temporary output file
        temp_file = f"{csv_file}.tmp"
        
        # Optimize the file
        if optimize_csv_file(csv_file, temp_file, remove_urls):
            # Replace original with optimized version
            os.replace(temp_file, csv_file)
            success_count += 1
        else:
            # Clean up temp file on error
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        print()
    
    print("=" * 50)
    print(f"Optimization complete: {success_count}/{len(csv_files)} files processed successfully")
    
    if create_backup:
        print(f"Original files backed up to: {backup_dir}/")


if __name__ == '__main__':
    main()
