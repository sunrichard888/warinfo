#!/usr/bin/env python3
"""
Global Conflict Data Fetcher with REAL data from GDELT
This is the main entry point that uses real data sources instead of sample data
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to use the simple real data updater
    from update_simple import main as update_real_data
    print("Using real GDELT data source")
    update_real_data()
    
except Exception as e:
    print(f"Error using real data: {e}")
    print("Falling back to original conflict data fetcher...")
    
    # Fallback to original implementation
    from conflict_data_original import ConflictDataFetcher
    
    if __name__ == "__main__":
        fetcher = ConflictDataFetcher()
        fetcher.update_conflict_data()
        fetcher.save_data()