#!/usr/bin/env python3
"""
Recent conflicts data with detailed event descriptions
"""

import json
from datetime import datetime, timedelta

def get_recent_conflict_events():
    """
    Get recent conflict events with detailed descriptions
    Returns a list of events from the past week
    """
    # Sample recent conflict events (last 7 days)
    # In production, this would fetch from ACLED or other real-time sources
    recent_events = [
        {
            "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "country": "Ukraine",
            "region": "Donetsk Oblast",
            "description": "Intense artillery exchange between Ukrainian and Russian forces near Bakhmut",
            "casualties": "15 killed, 23 wounded",
            "source": "Local military reports"
        },
        {
            "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "country": "Israel",
            "region": "Gaza Strip",
            "description": "Israeli airstrikes on Hamas targets in northern Gaza",
            "casualties": "8 killed, 12 wounded",
            "source": "Gaza Health Ministry"
        },
        {
            "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "country": "Sudan",
            "region": "Khartoum",
            "description": "Clashes between Sudanese Army and Rapid Support Forces in central Khartoum",
            "casualties": "12 killed, 18 wounded",
            "source": "Sudanese medical sources"
        },
        {
            "date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "country": "Myanmar",
            "region": "Shan State",
            "description": "Armed conflict between Myanmar military and ethnic armed groups",
            "casualties": "7 killed, 9 wounded",
            "source": "Local news reports"
        },
        {
            "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "country": "Syria",
            "region": "Idlib Province",
            "description": "Turkish-backed opposition forces clash with Syrian government troops",
            "casualties": "5 killed, 11 wounded",
            "source": "Syrian Observatory for Human Rights"
        },
        {
            "date": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"),
            "country": "Yemen",
            "region": "Marib Governorate",
            "description": "Houthi missile attack on coalition positions",
            "casualties": "6 killed, 8 wounded",
            "source": "Yemeni military sources"
        },
        {
            "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "country": "Afghanistan",
            "region": "Kabul",
            "description": "Taliban security forces clash with ISIS-K militants",
            "casualties": "4 killed, 7 wounded",
            "source": "Afghan interior ministry"
        },
        {
            "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "country": "Somalia",
            "region": "Mogadishu",
            "description": "Al-Shabaab suicide bombing targeting government building",
            "casualties": "10 killed, 15 wounded",
            "source": "Somali police"
        },
        {
            "date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "country": "Nigeria",
            "region": "Borno State",
            "description": "Boko Haram attack on military checkpoint",
            "casualties": "8 killed, 6 wounded",
            "source": "Nigerian army"
        },
        {
            "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "country": "Colombia",
            "region": "Cauca Department",
            "description": "Clash between rival drug cartels in rural area",
            "casualties": "6 killed, 3 wounded",
            "source": "Colombian police"
        },
        {
            "date": (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d"),
            "country": "Mexico",
            "region": "Michoacán",
            "description": "Cartel violence in small town, civilians caught in crossfire",
            "casualties": "9 killed, 4 wounded",
            "source": "Mexican authorities"
        },
        {
            "date": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"),
            "country": "Haiti",
            "region": "Port-au-Prince",
            "description": "Gang warfare intensifies in capital city neighborhoods",
            "casualties": "11 killed, 14 wounded",
            "source": "Haitian police"
        }
    ]
    
    return recent_events

def save_recent_events(filename="recent_conflicts.json"):
    """Save recent conflict events to JSON file"""
    events = get_recent_conflicts()
    data = {
        "last_updated": datetime.now().isoformat(),
        "events": events
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Recent events saved to {filename}")

if __name__ == "__main__":
    save_recent_events()