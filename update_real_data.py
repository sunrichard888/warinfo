#!/usr/bin/env python3
"""
Update script to fetch real conflict data from GDELT
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conflict_data_real import RealConflictDataFetcher

def main():
    """Main function to update real conflict data"""
    print("Starting real conflict data update...")
    
    fetcher = RealConflictDataFetcher()
    fetcher.update_conflict_data()
    fetcher.save_data("conflict_data.json")  # Overwrite the original file
    
    print("Real conflict data update completed!")

if __name__ == "__main__":
    main()