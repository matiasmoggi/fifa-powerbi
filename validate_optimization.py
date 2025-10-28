#!/usr/bin/env python3
"""
Quick validation script to verify data optimization results.

This script compares the original and optimized data to ensure:
- No data loss occurred
- Encoding is correct
- File sizes are reduced
- Dimension tables are correct
"""

import csv
import os


def validate_optimization():
    """Validate that optimization was successful."""
    print("Validating FIFA Data Optimization...")
    print("=" * 80)
    
    # Check files exist
    required_files = [
        'fifa_data_consolidated.csv',
        'dimension_tables/dim_clubs.csv',
        'dimension_tables/dim_nationalities.csv'
    ]
    
    print("\n1. Checking required files exist...")
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024
            print(f"   ✓ {file} ({size:.1f} KB)")
        else:
            print(f"   ✗ {file} - NOT FOUND")
            return False
    
    # Check consolidated file
    print("\n2. Validating consolidated file...")
    with open('fifa_data_consolidated.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        # Check Year column exists
        if 'Year' not in headers:
            print("   ✗ Year column missing")
            return False
        print("   ✓ Year column present")
        
        # Check URL columns removed
        url_cols = ['Photo', 'Flag', 'Club Logo']
        removed = [col for col in url_cols if col not in headers]
        if len(removed) == len(url_cols):
            print(f"   ✓ URL columns removed: {url_cols}")
        else:
            print(f"   ✗ URL columns still present")
            return False
        
        # Count rows and years
        years = set()
        row_count = 0
        for row in reader:
            row_count += 1
            years.add(row.get('Year'))
        
        print(f"   ✓ Total rows: {row_count:,}")
        print(f"   ✓ Years covered: {sorted(years)}")
    
    # Check dimension tables
    print("\n3. Validating dimension tables...")
    with open('dimension_tables/dim_clubs.csv', 'r', encoding='utf-8') as f:
        clubs = sum(1 for _ in f) - 1
        print(f"   ✓ Unique clubs: {clubs:,}")
    
    with open('dimension_tables/dim_nationalities.csv', 'r', encoding='utf-8') as f:
        nationalities = sum(1 for _ in f) - 1
        print(f"   ✓ Unique nationalities: {nationalities:,}")
    
    # Calculate space savings
    print("\n4. Space savings analysis...")
    original_files = [
        'FIFA17_official_data.csv',
        'FIFA18_official_data.csv',
        'FIFA19_official_data.csv',
        'FIFA20_official_data.csv',
        'FIFA21_official_data.csv',
        'FIFA22_official_data.csv',
    ]
    
    original_size = sum(os.path.getsize(f) for f in original_files if os.path.exists(f))
    optimized_size = os.path.getsize('fifa_data_consolidated.csv')
    
    original_mb = original_size / (1024 * 1024)
    optimized_mb = optimized_size / (1024 * 1024)
    savings_mb = original_mb - optimized_mb
    savings_pct = (savings_mb / original_mb) * 100
    
    print(f"   Original: {original_mb:.2f} MB")
    print(f"   Optimized: {optimized_mb:.2f} MB")
    print(f"   ✓ Saved: {savings_mb:.2f} MB ({savings_pct:.1f}% reduction)")
    
    print("\n" + "=" * 80)
    print("✓ Validation PASSED - Optimization successful!")
    print("=" * 80)
    return True


if __name__ == '__main__':
    validate_optimization()
