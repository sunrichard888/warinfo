#!/usr/bin/env python3
"""
Global Conflict Data Fetcher
Fetches conflict data from public sources and creates heatmaps
"""

import json
import requests
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup

class ConflictDataFetcher:
    def __init__(self):
        self.conflict_data = {}
        self.recent_events = []
        self.last_updated = None
        
    def fetch_acled_data(self):
        """
        Fetch data from ACLED (Armed Conflict Location & Event Data Project)
        ACLED provides real-time data on political violence and protest events
        """
        try:
            # ACLED has an API but requires registration
            # For demo purposes, we'll use a mock dataset
            print("Note: ACLED API requires registration. Using sample data.")
            return self.get_sample_conflict_data(), self.get_sample_recent_events()
        except Exception as e:
            print(f"Error fetching ACLED data: {e}")
            return self.get_sample_conflict_data(), self.get_sample_recent_events()
    
    def get_sample_conflict_data(self):
        """
        Sample conflict data for demonstration
        In production, this would be replaced with real API calls
        """
        # Sample data based on known active conflicts (2026)
        sample_data = {
            "Ukraine": {"intensity": 95, "events_last_7days": 120, "type": "International War"},
            "Israel": {"intensity": 90, "events_last_7days": 85, "type": "Regional Conflict"},
            "Gaza": {"intensity": 92, "events_last_7days": 90, "type": "Regional Conflict"},
            "Sudan": {"intensity": 85, "events_last_7days": 65, "type": "Civil War"},
            "Myanmar": {"intensity": 80, "events_last_7days": 55, "type": "Civil War"},
            "Syria": {"intensity": 75, "events_last_7days": 45, "type": "Ongoing Conflict"},
            "Yemen": {"intensity": 70, "events_last_7days": 40, "type": "Civil War"},
            "Afghanistan": {"intensity": 65, "events_last_7days": 35, "type": "Insurgency"},
            "Somalia": {"intensity": 60, "events_last_7days": 30, "type": "Insurgency"},
            "Nigeria": {"intensity": 55, "events_last_7days": 25, "type": "Terrorism"},
            "Colombia": {"intensity": 50, "events_last_7days": 20, "type": "Drug War"},
            "Mexico": {"intensity": 45, "events_last_7days": 18, "type": "Drug War"},
            "Haiti": {"intensity": 40, "events_last_7days": 15, "type": "Gang Violence"},
            "Pakistan": {"intensity": 35, "events_last_7days": 12, "type": "Terrorism"},
            "India": {"intensity": 30, "events_last_7days": 10, "type": "Insurgency"},
            "Philippines": {"intensity": 25, "events_last_7days": 8, "type": "Insurgency"},
            "Russia": {"intensity": 20, "events_last_7days": 5, "type": "Terrorism"},
            "Turkey": {"intensity": 15, "events_last_7days": 3, "type": "Kurdish Conflict"}
        }
        
        return sample_data
    
    def get_sample_recent_events(self):
        """
        Sample recent conflict events for the last 7 days
        Format: [date, country, event_description, fatalities, injuries]
        """
        from datetime import datetime, timedelta
        
        # Generate dates for the last 7 days
        today = datetime.now()
        recent_events = []
        
        # Ukraine events
        recent_events.extend([
            [today.strftime("%Y-%m-%d"), "Ukraine", "Russian missile strike on Kyiv residential area", 12, 45],
            [(today - timedelta(days=1)).strftime("%Y-%m-%d"), "Ukraine", "Artillery exchange in Donetsk region", 8, 23],
            [(today - timedelta(days=2)).strftime("%Y-%m-%d"), "Ukraine", "Drone attack on military base in Kharkiv", 3, 15],
            [(today - timedelta(days=3)).strftime("%Y-%m-%d"), "Ukraine", "Ground assault repelled near Bakhmut", 15, 32],
            [(today - timedelta(days=5)).strftime("%Y-%m-%d"), "Ukraine", "Air defense intercepts cruise missiles over Odesa", 0, 7]
        ])
        
        # Gaza/Israel events
        recent_events.extend([
            [today.strftime("%Y-%m-%d"), "Gaza", "Israeli airstrike on Hamas command center", 25, 60],
            [(today - timedelta(days=1)).strftime("%Y-%m-%d"), "Israel", "Rocket barrage from Gaza intercepted by Iron Dome", 2, 18],
            [(today - timedelta(days=2)).strftime("%Y-%m-%d"), "Gaza", "Ground operation in northern Gaza Strip", 35, 80],
            [(today - timedelta(days=4)).strftime("%Y-%m-%d"), "Israel", "Hostage rescue operation in southern Israel", 5, 3]
        ])
        
        # Sudan events
        recent_events.extend([
            [today.strftime("%Y-%m-%d"), "Sudan", "Clashes between SAF and RSF in Khartoum", 18, 42],
            [(today - timedelta(days=2)).strftime("%Y-%m-%d"), "Sudan", "Airstrike on RSF positions in Darfur", 12, 28],
            [(today - timedelta(days=6)).strftime("%Y-%m-%d"), "Sudan", "Humanitarian convoy attacked in Kordofan", 7, 15]
        ])
        
        # Myanmar events
        recent_events.extend([
            [(today - timedelta(days=1)).strftime("%Y-%m-%d"), "Myanmar", "Military junta offensive against resistance forces in Sagaing", 22, 35],
            [(today - timedelta(days=3)).strftime("%Y-%m-%d"), "Myanmar", "Ethnic armed group ambush on military convoy", 14, 26],
            [(today - timedelta(days=5)).strftime("%Y-%m-%d"), "Myanmar", "Airstrike on civilian village in Karen State", 9, 31]
        ])
        
        # Syria events
        recent_events.extend([
            [(today - timedelta(days=2)).strftime("%Y-%m-%d"), "Syria", "ISIS attack on Syrian government checkpoint", 6, 12],
            [(today - timedelta(days=4)).strftime("%Y-%m-%d"), "Syria", "Turkish drone strike on PKK positions in northern Syria", 4, 8]
        ])
        
        # Yemen events
        recent_events.extend([
            [(today - timedelta(days=1)).strftime("%Y-%m-%d"), "Yemen", "Houthi missile attack on Saudi border town", 3, 15],
            [(today - timedelta(days=3)).strftime("%Y-%m-%d"), "Yemen", "Coalition airstrike on Houthi military facility", 11, 24]
        ])
        
        # Afghanistan events
        recent_events.extend([
            [(today - timedelta(days=2)).strftime("%Y-%m-%d"), "Afghanistan", "Taliban security operation against ISIS-K in Kabul", 8, 17],
            [(today - timedelta(days=5)).strftime("%Y-%m-%d"), "Afghanistan", "Suicide bombing at mosque in Herat", 15, 40]
        ])
        
        # Somalia events
        recent_events.extend([
            [(today - timedelta(days=1)).strftime("%Y-%m-%d"), "Somalia", "Al-Shabaab attack on military base near Mogadishu", 12, 28],
            [(today - timedelta(days=4)).strftime("%Y-%m-%d"), "Somalia", "African Union peacekeeping patrol ambushed", 7, 19]
        ])
        
        # Nigeria events
        recent_events.extend([
            [(today - timedelta(days=2)).strftime("%Y-%m-%d"), "Nigeria", "Boko Haram raid on village in Borno State", 18, 35],
            [(today - timedelta(days=6)).strftime("%Y-%m-%d"), "Nigeria", "Bandit attack on highway in Kaduna State", 9, 22]
        ])
        
        # Colombia events
        recent_events.extend([
            [(today - timedelta(days=3)).strftime("%Y-%m-%d"), "Colombia", "ELN guerrilla attack on oil pipeline", 2, 8],
            [(today - timedelta(days=5)).strftime("%Y-%m-%d"), "Colombia", "Drug cartel shootout in Medellin", 6, 14]
        ])
        
        # Sort by date (most recent first)
        recent_events.sort(key=lambda x: x[0], reverse=True)
        
        return recent_events[:20]  # Return top 20 most recent events
    
    def update_conflict_data(self):
        """Update conflict data from sources"""
        print("Fetching latest conflict data...")
        self.conflict_data, self.recent_events = self.fetch_acled_data()
        self.last_updated = datetime.now()
        print(f"Data updated at {self.last_updated}")
        
    def save_data(self, filename="conflict_data.json"):
        """Save conflict data to JSON file"""
        data_to_save = {
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "conflict_data": self.conflict_data,
            "recent_events": self.recent_events
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")
        
    def load_data(self, filename="conflict_data.json"):
        """Load conflict data from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.last_updated = datetime.fromisoformat(data["last_updated"]) if data["last_updated"] else None
                self.conflict_data = data["conflict_data"]
                self.recent_events = data["recent_events"]
            print(f"Data loaded from {filename}")
        except FileNotFoundError:
            print(f"{filename} not found. Using empty data.")
            self.conflict_data = {}
            self.recent_events = []
            self.last_updated = None

if __name__ == "__main__":
    fetcher = ConflictDataFetcher()
    fetcher.update_conflict_data()
    fetcher.save_data()