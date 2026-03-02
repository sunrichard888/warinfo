#!/usr/bin/env python3
"""
GDELT Data Fetcher - Real-time Global Conflict Data
Uses GDELT (Global Database of Events, Language, and Tone) API
GDELT provides free real-time data on global events every 15 minutes
"""

import requests
import json
from datetime import datetime, timedelta
import zipfile
import io

class GDELTFetcher:
    def __init__(self):
        self.base_url = "http://data.gdeltproject.org/gdeltv2"
        
    def get_latest_file_info(self):
        """Get the latest GDELT file URLs"""
        try:
            response = requests.get(f"{self.base_url}/lastupdate.txt", timeout=30)
            response.raise_for_status()
            
            lines = response.text.strip().split('\n')
            files = {}
            for line in lines:
                if 'export.CSV.zip' in line:
                    files['events'] = line.split()[-1]
                elif 'mentions.CSV.zip' in line:
                    files['mentions'] = line.split()[-1]
                elif 'gkg.csv.zip' in line:
                    files['gkg'] = line.split()[-1]
                    
            return files
        except Exception as e:
            print(f"Error fetching GDELT file info: {e}")
            return None
    
    def fetch_events_data(self, url):
        """Fetch and parse GDELT events data from ZIP file"""
        try:
            print(f"Fetching GDELT events from: {url}")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            # Handle ZIP file
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            csv_filename = [f for f in zip_file.namelist() if f.endswith('.CSV')][0]
            csv_content = zip_file.read(csv_filename).decode('utf-8')
            
            # Parse CSV data
            events = []
            lines = csv_content.strip().split('\n')
            for line in lines:
                if line.strip():
                    fields = line.split('\t')
                    if len(fields) >= 61:
                        event = {
                            'gdelt_id': fields[0],
                            'date': fields[1],
                            'actor1_name': fields[6],
                            'actor1_country_code': fields[7],
                            'actor2_name': fields[16],
                            'actor2_country_code': fields[17],
                            'event_code': fields[26],
                            'event_base_code': fields[27],
                            'goldstein_scale': float(fields[30]) if fields[30] else 0.0,
                            'num_mentions': int(fields[31]) if fields[31] else 0,
                            'num_sources': int(fields[32]) if fields[32] else 0,
                            'num_articles': int(fields[33]) if fields[33] else 0,
                            'avg_tone': float(fields[34]) if fields[34] else 0.0,
                            'actor1_geo_full_name': fields[36],
                            'actor1_geo_country_code': fields[37],
                            'actor1_geo_lat': float(fields[44]) if fields[44] else 0.0,
                            'actor1_geo_long': float(fields[45]) if fields[45] else 0.0,
                            'actor2_geo_full_name': fields[48],
                            'actor2_geo_country_code': fields[49],
                            'actor2_geo_lat': float(fields[56]) if fields[56] else 0.0,
                            'actor2_geo_long': float(fields[57]) if fields[57] else 0.0,
                            'url': fields[59]
                        }
                        events.append(event)
            
            print(f"Fetched {len(events)} events from GDELT")
            return events
            
        except Exception as e:
            print(f"Error fetching/parsing GDELT events: {e}")
            return []
    
    def filter_conflict_events(self, events, days_back=7):
        """Filter events to only include conflict-related ones"""
        conflict_events = []
        cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y%m%d')
        
        # Conflict-related CAMEO root codes
        conflict_root_codes = {'18', '19', '20', '17', '16', '15', '14', '13', '12', '11', '10', '09', '08', '07'}
        
        for event in events:
            if event['date'] >= cutoff_date and event['event_base_code'][:2] in conflict_root_codes:
                # Calculate casualties based on tone and mentions (rough estimation)
                fatalities = max(0, min(100, int(abs(event['avg_tone']) * event['num_mentions'] / 10)))
                injuries = max(0, min(200, int(abs(event['avg_tone']) * event['num_mentions'] / 5)))
                
                # Format date properly
                formatted_date = f"{event['date'][:4]}-{event['date'][4:6]}-{event['date'][6:8]}"
                
                # Get country name from code
                country_name = self.get_country_name(event['actor1_geo_country_code'])
                if not country_name:
                    country_name = event['actor1_geo_country_code'] or 'Unknown'
                
                # Get region/location
                region = event['actor1_geo_full_name'] or country_name
                
                # Get event description
                description = self.get_event_description(event['event_code'])
                
                conflict_events.append([
                    formatted_date,
                    country_name,
                    region,
                    description,
                    fatalities,
                    injuries,
                    f"{event['actor1_name']} vs {event['actor2_name']}" if event['actor2_name'] else event['actor1_name'],
                    event['url'],
                    event['gdelt_id']
                ])
        
        # Sort by date (most recent first) and limit to top 50
        conflict_events.sort(key=lambda x: x[0], reverse=True)
        return conflict_events[:50]
    
    def get_country_name(self, country_code):
        """Convert country code to full name"""
        country_map = {
            'US': 'United States', 'UA': 'Ukraine', 'IL': 'Israel', 'PS': 'Palestine',
            'SD': 'Sudan', 'MM': 'Myanmar', 'SY': 'Syria', 'YE': 'Yemen', 'AF': 'Afghanistan',
            'SO': 'Somalia', 'NG': 'Nigeria', 'CO': 'Colombia', 'MX': 'Mexico', 'HT': 'Haiti',
            'PK': 'Pakistan', 'IN': 'India', 'PH': 'Philippines', 'RU': 'Russia', 'TR': 'Turkey',
            'IR': 'Iran', 'CN': 'China', 'GB': 'United Kingdom', 'FR': 'France', 'DE': 'Germany',
            'IQ': 'Iraq', 'SA': 'Saudi Arabia', 'JO': 'Jordan', 'LB': 'Lebanon', 'EG': 'Egypt'
        }
        return country_map.get(country_code, country_code)
    
    def get_event_description(self, event_code):
        """Convert CAMEO event code to description"""
        descriptions = {
            '182': 'Abduct/Hostage Taking', '183': 'Physically Assault', '184': 'Sexually Assault',
            '185': 'Torture', '186': 'Kill By Physical Assault', '191': 'Impose Administrative Sanctions',
            '192': 'Arrest/Indict/Detain', '193': 'Investigate', '194': 'Confiscate Property',
            '195': 'Use Tactics of Violent Repression', '196': 'Attack Cybernetically',
            '201': 'Use Conventional Military Force', '202': 'Use Unconventional Violence',
            '203': 'Use Weapons of Mass Destruction', '171': 'Threaten Conventional Military Force',
            '172': 'Threaten Unconventional Violence', '173': 'Threaten Weapons of Mass Destruction'
        }
        return descriptions.get(event_code, f"Event {event_code}")
    
    def calculate_country_intensity(self, events):
        """Calculate conflict intensity for countries"""
        country_data = {}
        
        for event in events:
            country = event[1]
            if country == 'Unknown':
                continue
                
            if country not in country_data:
                country_data[country] = {
                    'intensity': 0,
                    'events': 0,
                    'fatalities': 0,
                    'injuries': 0
                }
            
            # Calculate intensity
            event_intensity = min(100, event[4] + event[5] + event[4])
            country_data[country]['intensity'] = max(country_data[country]['intensity'], event_intensity)
            country_data[country]['events'] += 1
            country_data[country]['fatalities'] += event[4]
            country_data[country]['injuries'] += event[5]
        
        return country_data