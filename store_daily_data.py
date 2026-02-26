#!/usr/bin/env python3
"""
Daily conflict data storage script
Stores the current day's conflict data to SQLite database
"""

import sys
import os
import json
from datetime import datetime
from database import ConflictDataStorage

def load_current_data():
    """Load current conflict data from JSON file"""
    try:
        with open('conflict_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("Error: conflict_data.json not found")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON in conflict_data.json")
        return None

def extract_conflict_events(data):
    """Extract conflict events from data structure"""
    events = []
    
    # Assuming recent_conflicts structure from your existing code
    if 'recent_conflicts' in data:
        for event in data['recent_conflicts']:
            # event format: [date, country, description, killed, wounded]
            if len(event) >= 5:
                events.append({
                    'date': event[0],
                    'country': event[1],
                    'description': event[2],
                    'fatalities': event[3],
                    'injuries': event[4],
                    'region': event[1],  # Default to country if no specific region
                    'event_type': 'general_conflict',  # Could be enhanced later
                    'source_url': '',  # Could be added from your source links
                    'acled_id': ''  # Could be added if using ACLED API
                })
    
    return events

def extract_intensity_data(data):
    """Extract intensity data for countries"""
    intensity_data = {}
    
    if 'conflict_data' in data:
        for country, info in data['conflict_data'].items():
            intensity_data[country] = {
                'intensity': info.get('intensity', 0),
                'events': info.get('events', 0),
                'fatalities': info.get('fatalities', 0)
            }
    
    return intensity_data

def main():
    """Main function to store daily data"""
    print("Starting daily conflict data storage...")
    
    # Load current data
    data = load_current_data()
    if not data:
        print("Failed to load conflict data. Exiting.")
        sys.exit(1)
    
    # Extract events and intensity data
    events = extract_conflict_events(data)
    intensity_data = extract_intensity_data(data)
    
    if not events and not intensity_data:
        print("No data to store. Exiting.")
        sys.exit(0)
    
    # Initialize database storage
    storage = ConflictDataStorage()
    
    # Store the data
    try:
        storage.store_daily_data(events, intensity_data)
        print(f"Successfully stored {len(events)} conflict events and {len(intensity_data)} country intensity records")
        
        # Also store a backup of the raw JSON with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'data_backups/conflict_data_{timestamp}.json'
        os.makedirs('data_backups', exist_ok=True)
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Raw data backup saved to {backup_file}")
        
    except Exception as e:
        print(f"Error storing data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()