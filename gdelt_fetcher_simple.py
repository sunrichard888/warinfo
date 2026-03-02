#!/usr/bin/env python3
"""
Simple GDELT fetcher that handles ZIP files properly
"""

import json
import requests
import zipfile
import io
import csv
from datetime import datetime, timedelta

def fetch_latest_gdelt_events():
    """Fetch the latest GDELT events data (handles ZIP properly)"""
    try:
        # Get the latest file info
        response = requests.get("http://data.gdeltproject.org/gdeltv2/lastupdate.txt", timeout=30)
        response.raise_for_status()
        
        lines = response.text.strip().split('\n')
        export_url = None
        for line in lines:
            if 'export.CSV.zip' in line:
                export_url = line.split()[-1]
                break
        
        if not export_url:
            return []
            
        # Download and extract ZIP
        print(f"Downloading GDELT data from: {export_url}")
        zip_response = requests.get(export_url, timeout=60)
        zip_response.raise_for_status()
        
        # Extract CSV from ZIP
        with zipfile.ZipFile(io.BytesIO(zip_response.content)) as zip_file:
            csv_filename = [f for f in zip_file.namelist() if f.endswith('.CSV')][0]
            with zip_file.open(csv_filename) as csv_file:
                content = csv_file.read().decode('utf-8', errors='ignore')
                
        # Parse CSV
        csv_reader = csv.reader(io.StringIO(content), delimiter='\t')
        events = []
        for row in csv_reader:
            if len(row) >= 61:
                events.append(row)
                if len(events) >= 1000:  # Limit for testing
                    break
                    
        print(f"Fetched {len(events)} events")
        return events
        
    except Exception as e:
        print(f"Error fetching GDELT data: {e}")
        return []

def extract_iran_events(events):
    """Extract events related to Iran"""
    iran_events = []
    for event in events:
        # Check if either actor is Iran (country code IR)
        actor1_country = event[7] if len(event) > 7 else ""
        actor2_country = event[17] if len(event) > 17 else ""
        
        if "IR" in [actor1_country, actor2_country]:
            # Extract relevant info
            date = event[1] if len(event) > 1 else "Unknown"
            actor1 = event[6] if len(event) > 6 else "Unknown"
            actor2 = event[16] if len(event) > 16 else "Unknown"
            event_code = event[26] if len(event) > 26 else "Unknown"
            url = event[59] if len(event) > 59 else "Unknown"
            
            iran_events.append({
                'date': date,
                'actor1': actor1,
                'actor2': actor2,
                'event_code': event_code,
                'url': url
            })
    
    return iran_events

if __name__ == "__main__":
    events = fetch_latest_gdelt_events()
    if events:
        iran_events = extract_iran_events(events)
        print(f"\nFound {len(iran_events)} Iran-related events:")
        for event in iran_events[:5]:  # Show first 5
            print(f"Date: {event['date']}, Actors: {event['actor1']} vs {event['actor2']}, URL: {event['url']}")
    else:
        print("No events fetched")