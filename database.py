#!/usr/bin/env python3
"""
Conflict data storage and management system
Supports SQLite database operations for warinfo project
"""

import sqlite3
import json
import os
from datetime import datetime, date
from typing import List, Dict, Any, Optional


class ConflictDatabase:
    def __init__(self, db_path: str = "conflict_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conflicts daily events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conflicts_daily (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                country VARCHAR(100) NOT NULL,
                region VARCHAR(200),
                event_type VARCHAR(100),
                fatalities INTEGER DEFAULT 0,
                injuries INTEGER DEFAULT 0,
                description TEXT,
                source_url TEXT,
                acled_id VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, acled_id)
            )
        ''')
        
        # Countries intensity tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS countries_intensity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                country VARCHAR(100) NOT NULL,
                intensity_score INTEGER NOT NULL CHECK (intensity_score >= 0 AND intensity_score <= 100),
                event_count INTEGER DEFAULT 0,
                total_fatalities INTEGER DEFAULT 0,
                total_injuries INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, country)
            )
        ''')
        
        # Summary statistics table (for faster reporting)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS summary_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_type VARCHAR(20) NOT NULL, -- 'daily', 'weekly', 'monthly', 'quarterly', 'annual'
                period_key VARCHAR(20) NOT NULL,  -- '2026-02', '2026-Q1', '2026', etc.
                total_events INTEGER DEFAULT 0,
                total_countries INTEGER DEFAULT 0,
                total_fatalities INTEGER DEFAULT 0,
                avg_intensity REAL DEFAULT 0.0,
                peak_intensity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(period_type, period_key)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database initialized at {self.db_path}")
    
    def store_conflicts_daily(self, conflict_events: List[List[Any]]) -> int:
        """
        Store daily conflict events
        
        Args:
            conflict_events: List of [date, country, description, killed, wounded] 
                           or extended format with more fields
            
        Returns:
            Number of records inserted
        """
        if not conflict_events:
            return 0
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        inserted_count = 0
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        for event in conflict_events:
            try:
                # Handle different event formats
                if len(event) >= 5:
                    # Extended format: [date, country, region, event_type, fatalities, injuries, description, source_url, acled_id]
                    if len(event) == 9:
                        event_date, country, region, event_type, fatalities, injuries, description, source_url, acled_id = event
                    # Basic format from recent_conflicts.py: [date, country, description, killed, wounded]
                    elif len(event) == 5:
                        event_date, country, description, fatalities, injuries = event
                        region = country
                        event_type = "Unspecified"
                        source_url = ""
                        acled_id = f"{event_date}_{country}_{fatalities}"
                    else:
                        continue
                    
                    # Ensure fatalities and injuries are integers
                    fatalities = int(fatalities) if fatalities else 0
                    injuries = int(injuries) if injuries else 0
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO conflicts_daily 
                        (date, country, region, event_type, fatalities, injuries, description, source_url, acled_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (event_date, country, region, event_type, fatalities, injuries, description, source_url, acled_id))
                    
                    inserted_count += 1
                    
            except Exception as e:
                print(f"Error storing event {event}: {e}")
                continue
        
        conn.commit()
        conn.close()
        print(f"Stored {inserted_count} conflict events")
        return inserted_count
    
    def store_countries_intensity(self, intensity_data: Dict[str, Dict[str, Any]]) -> int:
        """
        Store country intensity data
        
        Args:
            intensity_data: Dict with country names as keys and intensity info as values
                           Format: {country: {'intensity': score, 'events': count, 'fatalities': total}}
            
        Returns:
            Number of records inserted
        """
        if not intensity_data:
            return 0
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        inserted_count = 0
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        for country, data in intensity_data.items():
            try:
                intensity_score = int(data.get('intensity', 0))
                event_count = int(data.get('events', 0))
                total_fatalities = int(data.get('fatalities', 0))
                total_injuries = int(data.get('injuries', 0))
                
                # Clamp intensity to 0-100 range
                intensity_score = max(0, min(100, intensity_score))
                
                cursor.execute('''
                    INSERT OR REPLACE INTO countries_intensity 
                    (date, country, intensity_score, event_count, total_fatalities, total_injuries)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (current_date, country, intensity_score, event_count, total_fatalities, total_injuries))
                
                inserted_count += 1
                
            except Exception as e:
                print(f"Error storing intensity data for {country}: {e}")
                continue
        
        conn.commit()
        conn.close()
        print(f"Stored intensity data for {inserted_count} countries")
        return inserted_count
    
    def get_daily_conflicts(self, date_str: str = None) -> List[Dict[str, Any]]:
        """Get conflicts for a specific date"""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, country, region, event_type, fatalities, injuries, description, source_url, acled_id
            FROM conflicts_daily 
            WHERE date = ?
            ORDER BY fatalities DESC, injuries DESC
        ''', (date_str,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'date': row[0],
                'country': row[1],
                'region': row[2],
                'event_type': row[3],
                'fatalities': row[4],
                'injuries': row[5],
                'description': row[6],
                'source_url': row[7],
                'acled_id': row[8]
            }
            for row in rows
        ]
    
    def get_country_intensity_history(self, country: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get intensity history for a specific country"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, intensity_score, event_count, total_fatalities, total_injuries
            FROM countries_intensity 
            WHERE country = ?
            ORDER BY date DESC
            LIMIT ?
        ''', (country, days))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'date': row[0],
                'intensity_score': row[1],
                'event_count': row[2],
                'total_fatalities': row[3],
                'total_injuries': row[4]
            }
            for row in rows
        ]
    
    def get_all_countries_current(self) -> List[Dict[str, Any]]:
        """Get current intensity data for all countries"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT country, intensity_score, event_count, total_fatalities, total_injuries
            FROM countries_intensity 
            WHERE date = ?
            ORDER BY intensity_score DESC
        ''', (current_date,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'country': row[0],
                'intensity_score': row[1],
                'event_count': row[2],
                'total_fatalities': row[3],
                'total_injuries': row[4]
            }
            for row in rows
        ]
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total events
        cursor.execute('SELECT COUNT(*) FROM conflicts_daily')
        total_events = cursor.fetchone()[0]
        
        # Date range
        cursor.execute('SELECT MIN(date), MAX(date) FROM conflicts_daily')
        date_range = cursor.fetchone()
        
        # Total countries
        cursor.execute('SELECT COUNT(DISTINCT country) FROM conflicts_daily')
        total_countries = cursor.fetchone()[0]
        
        # Recent activity
        current_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(*) FROM conflicts_daily WHERE date = ?', (current_date,))
        today_events = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_events': total_events,
            'date_range': {
                'start': date_range[0],
                'end': date_range[1]
            },
            'total_countries': total_countries,
            'today_events': today_events,
            'last_updated': datetime.now().isoformat()
        }


# Helper functions for integration with existing code
def load_sample_intensity_data() -> Dict[str, Dict[str, Any]]:
    """Load sample intensity data for testing"""
    return {
        "Ukraine": {"intensity": 85, "events": 12, "fatalities": 45},
        "Gaza": {"intensity": 90, "events": 8, "fatalities": 23},
        "Sudan": {"intensity": 75, "events": 15, "fatalities": 30},
        "Myanmar": {"intensity": 65, "events": 6, "fatalities": 18},
        "Israel": {"intensity": 70, "events": 2, "fatalities": 12},
        "Syria": {"intensity": 60, "events": 9, "fatalities": 7},
        "Yemen": {"intensity": 55, "events": 3, "fatalities": 15}
    }


if __name__ == "__main__":
    # Test the database
    db = ConflictDatabase()
    
    # Test with sample data
    sample_events = [
        ["2026-02-25", "Ukraine", "Kyiv", "Missile Strike", 12, 45, "Russian missile strike on Kyiv residential area", "https://example.com", "20260225_UA_12"],
        ["2026-02-24", "Gaza", "Rafah", "Airstrike", 8, 23, "Israeli airstrike on Rafah", "https://example.com", "20260224_GZ_8"]
    ]
    
    sample_intensity = load_sample_intensity_data()
    
    db.store_conflicts_daily(sample_events)
    db.store_countries_intensity(sample_intensity)
    
    print("Database test completed!")
    print("Stats:", db.get_database_stats())