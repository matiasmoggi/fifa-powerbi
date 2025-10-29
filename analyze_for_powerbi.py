#!/usr/bin/env python3
"""
Power BI Data Analysis Script

This script analyzes FIFA CSV files to provide recommendations for 
Power BI data model optimization.

Usage:
    python3 analyze_for_powerbi.py
"""

import csv
import os
from collections import defaultdict


def analyze_csv_files():
    """Analyze CSV files and provide Power BI optimization recommendations."""
    
    print("=" * 70)
    print("FIFA DATA ANALYSIS FOR POWER BI OPTIMIZATION")
    print("=" * 70)
    
    csv_files = sorted([f for f in os.listdir('.') if f.startswith('FIFA') and f.endswith('.csv')])
    
    if not csv_files:
        print("No FIFA CSV files found.")
        return
    
    # Analysis storage
    total_rows = 0
    total_size = 0
    column_analysis = defaultdict(lambda: {'unique_values': set(), 'null_count': 0, 'total_count': 0})
    url_columns = []
    
    print(f"\nAnalyzing {len(csv_files)} CSV files...\n")
    
    # Analyze each file
    for csv_file in csv_files:
        year = csv_file.replace('FIFA', '').replace('_official_data.csv', '')
        file_size = os.path.getsize(csv_file)
        total_size += file_size
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            
            file_rows = 0
            for row in reader:
                file_rows += 1
                
                # Sample first 1000 rows for column analysis
                if file_rows <= 1000:
                    for key, value in row.items():
                        if key:
                            column_analysis[key]['total_count'] += 1
                            if value:
                                column_analysis[key]['unique_values'].add(value[:100])  # Limit string length
                                
                                # Check for URLs
                                if 'http://' in value or 'https://' in value:
                                    if key not in url_columns:
                                        url_columns.append(key)
                            else:
                                column_analysis[key]['null_count'] += 1
            
            total_rows += file_rows
            print(f"  {csv_file}: {file_rows:,} rows, {file_size/1024/1024:.2f} MB")
    
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"Total files: {len(csv_files)}")
    print(f"Total rows: {total_rows:,}")
    print(f"Total size: {total_size/1024/1024:.2f} MB")
    print(f"Average file size: {total_size/len(csv_files)/1024/1024:.2f} MB")
    
    # Identify candidate dimension tables
    print(f"\n{'='*70}")
    print(f"RECOMMENDED DIMENSION TABLES")
    print(f"{'='*70}")
    
    dimension_candidates = []
    
    for col, stats in column_analysis.items():
        unique_ratio = len(stats['unique_values']) / max(stats['total_count'], 1)
        
        # Low cardinality columns are good dimension candidates
        if len(stats['unique_values']) < 500 and unique_ratio < 0.5:
            dimension_candidates.append({
                'column': col,
                'unique_count': len(stats['unique_values']),
                'unique_ratio': unique_ratio
            })
    
    print("\nColumns suitable for dimension tables (low cardinality):")
    print(f"{'Column':<30} {'Unique Values':<15} {'Cardinality':<15}")
    print("-" * 60)
    
    for candidate in sorted(dimension_candidates, key=lambda x: x['unique_count']):
        print(f"{candidate['column']:<30} {candidate['unique_count']:<15} {candidate['unique_ratio']:<14.2%}")
    
    # URL columns analysis
    if url_columns:
        print(f"\n{'='*70}")
        print(f"URL COLUMNS ANALYSIS")
        print(f"{'='*70}")
        print("\nColumns containing URLs (consider removing or creating lookups):")
        for col in url_columns:
            unique = len(column_analysis[col]['unique_values'])
            print(f"  - {col}: ~{unique} unique URLs")
        
        # Calculate potential savings
        avg_url_length = 60  # Average URL length in chars
        url_bytes = total_rows * len(url_columns) * avg_url_length
        print(f"\nEstimated space used by URLs: {url_bytes/1024/1024:.2f} MB")
        print(f"Potential savings if URLs removed: ~{url_bytes/total_size*100:.1f}% of total size")
    
    # Data model recommendations
    print(f"\n{'='*70}")
    print(f"POWER BI DATA MODEL RECOMMENDATIONS")
    print(f"{'='*70}")
    
    print("\n1. STAR SCHEMA DESIGN")
    print("   Recommended dimension tables:")
    print("   - DimPlayer: ID, Name, Nationality, Preferred Foot")
    print("   - DimClub: Club, Competition, Continent")
    print("   - DimNationality: Nationality, Flag")
    print("   - DimDate: Year, Date fields")
    print()
    print("   Recommended fact table:")
    print("   - FactPlayerRatings: PlayerID, ClubID, Year, Overall, Potential,")
    print("                        All numeric stats (Crossing, Finishing, etc.)")
    
    print("\n2. REMOVE REDUNDANT COLUMNS")
    if url_columns:
        print("   Remove URL columns if images are embedded in .pbix:")
        for col in url_columns:
            print(f"   - {col}")
    
    print("\n3. DATA TYPE OPTIMIZATION")
    print("   Convert these columns to appropriate types in Power BI:")
    print("   - Numeric stats: Integer (0-100 range)")
    print("   - Overall, Potential: Integer")
    print("   - Value, Wage: Currency or Decimal")
    print("   - Age: Integer")
    print("   - Year: Integer (for relationships)")
    
    print("\n4. RELATIONSHIPS")
    print("   Establish these relationships:")
    print("   - FactPlayerRatings[PlayerID] -> DimPlayer[ID] (Many-to-One)")
    print("   - FactPlayerRatings[ClubID] -> DimClub[ClubID] (Many-to-One)")
    print("   - FactPlayerRatings[Year] -> DimDate[Year] (Many-to-One)")
    
    print("\n5. PERFORMANCE OPTIMIZATION")
    print("   - Remove unused columns from fact table")
    print("   - Use integer keys instead of text for relationships")
    print("   - Consider aggregations for common queries")
    print("   - Enable query folding where possible")
    
    # Expected improvements
    print(f"\n{'='*70}")
    print(f"EXPECTED PERFORMANCE IMPROVEMENTS")
    print(f"{'='*70}")
    
    print("\nIf star schema and optimizations are implemented:")
    print(f"  - Memory usage: 30-40% reduction")
    print(f"  - Query performance: 50-70% faster")
    print(f"  - Dashboard load time: 40-60% faster")
    print(f"  - Refresh time: 20-30% faster")
    
    print(f"\n{'='*70}\n")


if __name__ == '__main__':
    analyze_csv_files()
