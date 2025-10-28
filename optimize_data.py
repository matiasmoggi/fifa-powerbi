#!/usr/bin/env python3
"""
FIFA Data Optimization Script

This script optimizes FIFA CSV files for better Power BI performance by:
1. Fixing encoding issues
2. Consolidating yearly files into one master file
3. Removing redundant URL columns
4. Creating dimension tables for better data modeling
5. Reducing file size and improving query performance

Usage:
    python3 optimize_data.py
"""

import csv
import os
import chardet
import sys
from collections import defaultdict


def detect_encoding(file_path):
    """Detect file encoding using chardet."""
    with open(file_path, 'rb') as f:
        raw_data = f.read(100000)
        result = chardet.detect(raw_data)
        return result['encoding']


def fix_encoding(input_file, output_file, source_encoding='ISO-8859-1'):
    """
    Fix encoding issues by converting to UTF-8.
    
    Args:
        input_file: Source CSV file
        output_file: Destination CSV file
        source_encoding: Source file encoding (default: ISO-8859-1)
    """
    print(f"Converting {input_file} from {source_encoding} to UTF-8...")
    
    with open(input_file, 'r', encoding=source_encoding, errors='ignore') as infile:
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            # Read and write line by line to handle large files efficiently
            for line in infile:
                outfile.write(line)
    
    print(f"  -> Created {output_file}")


def consolidate_yearly_files(input_files, output_file, remove_url_columns=True):
    """
    Consolidate multiple yearly CSV files into one master file with a Year column.
    
    Args:
        input_files: List of (year, filepath) tuples
        output_file: Output consolidated CSV file
        remove_url_columns: If True, removes URL columns to reduce size
    """
    print(f"\nConsolidating {len(input_files)} files into {output_file}...")
    
    # Columns to remove for optimization (URL columns that bloat file size)
    columns_to_remove = ['Photo', 'Flag', 'Club Logo'] if remove_url_columns else []
    
    total_rows = 0
    
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = None
        
        for year, filepath in input_files:
            print(f"  Processing {os.path.basename(filepath)} (Year: {year})...")
            
            # Detect encoding for this file
            encoding = detect_encoding(filepath)
            
            with open(filepath, 'r', encoding=encoding, errors='ignore') as infile:
                reader = csv.DictReader(infile)
                
                if writer is None:
                    # Initialize writer with headers from first file, adding Year column
                    fieldnames = [f for f in reader.fieldnames if f not in columns_to_remove]
                    fieldnames.insert(1, 'Year')  # Add Year column after ID
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                    writer.writeheader()
                
                # Write rows with Year column
                for row in reader:
                    # Remove URL columns
                    for col in columns_to_remove:
                        row.pop(col, None)
                    
                    # Add year
                    row['Year'] = year
                    
                    # Write only the fields we want
                    filtered_row = {k: row.get(k, '') for k in fieldnames}
                    writer.writerow(filtered_row)
                    total_rows += 1
    
    file_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"\n  -> Created {output_file}")
    print(f"  -> Total rows: {total_rows:,}")
    print(f"  -> File size: {file_size:.2f} MB")
    print(f"  -> Removed columns: {columns_to_remove}")


def create_dimension_tables(consolidated_file, output_dir='dimension_tables'):
    """
    Create dimension tables for star schema optimization.
    
    Args:
        consolidated_file: The consolidated master file
        output_dir: Directory to store dimension tables
    """
    print(f"\nCreating dimension tables in {output_dir}/...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Detect encoding
    encoding = detect_encoding(consolidated_file)
    
    # Collect unique values for dimension tables
    clubs = {}  # club_name -> (competition, continent)
    nationalities = set()
    
    with open(consolidated_file, 'r', encoding=encoding, errors='ignore') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Clubs dimension
            club = row.get('Club', '').strip()
            # Filter out URLs and empty values
            if club and not club.startswith('http'):
                if club not in clubs:
                    clubs[club] = {
                        'competition': row.get('competicizontinente', '').strip(),
                    }
            
            # Nationalities dimension
            nationality = row.get('Nationality', '').strip()
            # Filter out URLs that may have been incorrectly placed in nationality field
            if nationality and not nationality.startswith('http'):
                nationalities.add(nationality)
    
    # Write Clubs dimension table
    clubs_file = os.path.join(output_dir, 'dim_clubs.csv')
    with open(clubs_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ClubID', 'ClubName', 'Competition'])
        for idx, (club, info) in enumerate(sorted(clubs.items()), 1):
            writer.writerow([idx, club, info['competition']])
    
    print(f"  -> Created {clubs_file} ({len(clubs):,} unique clubs)")
    
    # Write Nationalities dimension table
    nationalities_file = os.path.join(output_dir, 'dim_nationalities.csv')
    with open(nationalities_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['NationalityID', 'NationalityName'])
        for idx, nationality in enumerate(sorted(nationalities), 1):
            writer.writerow([idx, nationality])
    
    print(f"  -> Created {nationalities_file} ({len(nationalities):,} unique nationalities)")


def generate_optimization_report(original_files, optimized_file):
    """Generate a report comparing original vs optimized data."""
    print("\n" + "=" * 80)
    print("OPTIMIZATION REPORT")
    print("=" * 80)
    
    # Calculate original size
    original_size = sum(os.path.getsize(f) for _, f in original_files) / (1024 * 1024)
    
    # Calculate optimized size
    optimized_size = os.path.getsize(optimized_file) / (1024 * 1024)
    
    # Calculate savings
    savings = original_size - optimized_size
    savings_pct = (savings / original_size) * 100
    
    print(f"\nOriginal total size: {original_size:.2f} MB")
    print(f"Optimized size: {optimized_size:.2f} MB")
    print(f"Space saved: {savings:.2f} MB ({savings_pct:.1f}% reduction)")
    
    print("\nOptimizations applied:")
    print("  ✓ Fixed encoding issues (converted to UTF-8)")
    print("  ✓ Consolidated 6 yearly files into 1 master file")
    print("  ✓ Removed redundant URL columns (Photo, Flag, Club Logo)")
    print("  ✓ Added Year column for temporal analysis")
    print("  ✓ Created dimension tables for star schema")
    
    print("\nNext steps for Power BI:")
    print("  1. Import 'fifa_data_consolidated.csv' instead of individual year files")
    print("  2. Import dimension tables from 'dimension_tables/' folder")
    print("  3. Create relationships between fact and dimension tables")
    print("  4. Remove old data sources from Power BI model")
    print("  5. Refresh data model and verify queries")
    
    print("=" * 80)


def main():
    """Main execution function."""
    print("FIFA Data Optimization Tool")
    print("=" * 80)
    
    # Define input files (year, filepath)
    yearly_files = [
        (2017, 'FIFA17_official_data.csv'),
        (2018, 'FIFA18_official_data.csv'),
        (2019, 'FIFA19_official_data.csv'),
        (2020, 'FIFA20_official_data.csv'),
        (2021, 'FIFA21_official_data.csv'),
        (2022, 'FIFA22_official_data.csv'),
    ]
    
    # Check if all files exist
    missing_files = [f for _, f in yearly_files if not os.path.exists(f)]
    if missing_files:
        print(f"ERROR: Missing files: {missing_files}")
        return 1
    
    # Output file
    consolidated_file = 'fifa_data_consolidated.csv'
    
    # Step 1: Consolidate files with optimizations
    consolidate_yearly_files(yearly_files, consolidated_file, remove_url_columns=True)
    
    # Step 2: Create dimension tables
    create_dimension_tables(consolidated_file)
    
    # Step 3: Generate report
    generate_optimization_report(yearly_files, consolidated_file)
    
    print("\n✓ Optimization complete!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
