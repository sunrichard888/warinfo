#!/usr/bin/env python3
"""
Conflict Report Generator with Weekly Support
Generates weekly, monthly, quarterly, and annual reports from stored conflict data
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import argparse
import sys

class ConflictReportGenerator:
    def __init__(self, db_path="conflict_data.db"):
        self.db_path = db_path
        self.reports_dir = "reports"
        self._ensure_reports_directory()
    
    def _ensure_reports_directory(self):
        """Ensure reports directory exists"""
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
        # Create subdirectories
        for subdir in ['weekly', 'monthly', 'quarterly', 'annual']:
            subdir_path = os.path.join(self.reports_dir, subdir)
            if not os.path.exists(subdir_path):
                os.makedirs(subdir_path)
    
    def get_weekly_report(self, start_date=None, end_date=None):
        """
        Generate weekly conflict report
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format (optional)
            end_date (str): End date in YYYY-MM-DD format (optional)
            
        Returns:
            dict: Weekly report data
        """
        if start_date is None or end_date is None:
            # Default to last 7 days
            today = datetime.now()
            end_date = today.strftime('%Y-%m-%d')
            start_date = (today - timedelta(days=6)).strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.db_path)
        
        try:
            # Get weekly statistics
            weekly_stats_query = f'''
                SELECT 
                    COUNT(*) as total_days,
                    SUM(event_count) as total_events,
                    SUM(total_fatalities) as total_fatalities,
                    AVG(intensity_score) as avg_intensity_score,
                    MAX(intensity_score) as peak_intensity_score
                FROM countries_intensity 
                WHERE date >= '{start_date}' AND date <= '{end_date}'
            '''
            weekly_stats_df = pd.read_sql_query(weekly_stats_query, conn)
            
            # Get top conflict countries for the week
            top_countries_query = f'''
                SELECT 
                    country,
                    SUM(event_count) as total_events,
                    SUM(total_fatalities) as total_fatalities,
                    AVG(intensity_score) as avg_intensity,
                    MAX(intensity_score) as peak_intensity
                FROM countries_intensity 
                WHERE date >= '{start_date}' AND date <= '{end_date}'
                GROUP BY country
                ORDER BY avg_intensity DESC
                LIMIT 10
            '''
            top_countries_df = pd.read_sql_query(top_countries_query, conn)
            
            # Get daily breakdown for the week
            daily_breakdown_query = f'''
                SELECT 
                    date,
                    AVG(intensity_score) as daily_avg_intensity,
                    SUM(event_count) as daily_total_events,
                    SUM(total_fatalities) as daily_fatalities
                FROM countries_intensity 
                WHERE date >= '{start_date}' AND date <= '{end_date}'
                GROUP BY date
                ORDER BY date
            '''
            daily_breakdown_df = pd.read_sql_query(daily_breakdown_query, conn)
            
            # Get recent conflict events from the week
            recent_events_query = f'''
                SELECT 
                    date, country, description, fatalities, injuries, source_url
                FROM conflicts_daily 
                WHERE date >= '{start_date}' AND date <= '{end_date}'
                ORDER BY date DESC, fatalities DESC
                LIMIT 20
            '''
            recent_events_df = pd.read_sql_query(recent_events_query, conn)
            
            report = {
                'report_type': 'weekly',
                'period': f"{start_date} to {end_date}",
                'generated_at': datetime.now().isoformat(),
                'summary': {
                    'total_days': int(weekly_stats_df['total_days'].iloc[0] or 0),
                    'total_events': int(weekly_stats_df['total_events'].iloc[0] or 0),
                    'total_fatalities': int(weekly_stats_df['total_fatalities'].iloc[0] or 0),
                    'avg_intensity_score': float(weekly_stats_df['avg_intensity_score'].iloc[0] or 0),
                    'peak_intensity_score': float(weekly_stats_df['peak_intensity_score'].iloc[0] or 0)
                },
                'top_conflict_countries': top_countries_df.to_dict('records'),
                'daily_breakdown': daily_breakdown_df.to_dict('records'),
                'recent_conflict_events': recent_events_df.to_dict('records')
            }
            
            return report
            
        finally:
            conn.close()
    
    def get_monthly_report(self, year, month):
        """
        Generate monthly conflict report
        
        Args:
            year (int): Year for the report
            month (int): Month for the report (1-12)
            
        Returns:
            dict: Monthly report data
        """
        # Calculate date range
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        conn = sqlite3.connect(self.db_path)
        
        try:
            # Get monthly statistics
            monthly_stats_query = f'''
                SELECT 
                    COUNT(*) as total_events,
                    SUM(total_fatalities) as total_fatalities,
                    SUM(event_count) as total_conflict_days,
                    AVG(intensity_score) as avg_intensity_score,
                    MAX(intensity_score) as peak_intensity_score
                FROM countries_intensity 
                WHERE date >= '{start_date}' AND date < '{end_date}'
            '''
            monthly_stats_df = pd.read_sql_query(monthly_stats_query, conn)
            
            # Get top conflict countries
            top_countries_query = f'''
                SELECT 
                    country,
                    SUM(event_count) as total_events,
                    SUM(total_fatalities) as total_fatalities,
                    AVG(intensity_score) as avg_intensity,
                    MAX(intensity_score) as peak_intensity
                FROM countries_intensity 
                WHERE date >= '{start_date}' AND date < '{end_date}'
                GROUP BY country
                ORDER BY avg_intensity DESC
                LIMIT 10
            '''
            top_countries_df = pd.read_sql_query(top_countries_query, conn)
            
            # Get daily trend data
            daily_trend_query = f'''
                SELECT 
                    date,
                    AVG(intensity_score) as daily_avg_intensity,
                    SUM(event_count) as daily_total_events
                FROM countries_intensity 
                WHERE date >= '{start_date}' AND date < '{end_date}'
                GROUP BY date
                ORDER BY date
            '''
            daily_trend_df = pd.read_sql_query(daily_trend_query, conn)
            
            report = {
                'report_type': 'monthly',
                'period': f"{year}-{month:02d}",
                'generated_at': datetime.now().isoformat(),
                'summary': {
                    'total_events': int(monthly_stats_df['total_events'].iloc[0] or 0),
                    'total_fatalities': int(monthly_stats_df['total_fatalities'].iloc[0] or 0),
                    'total_conflict_days': int(monthly_stats_df['total_conflict_days'].iloc[0] or 0),
                    'avg_intensity_score': float(monthly_stats_df['avg_intensity_score'].iloc[0] or 0),
                    'peak_intensity_score': float(monthly_stats_df['peak_intensity_score'].iloc[0] or 0)
                },
                'top_conflict_countries': top_countries_df.to_dict('records'),
                'daily_trend': daily_trend_df.to_dict('records')
            }
            
            return report
            
        finally:
            conn.close()
    
    def get_quarterly_report(self, year, quarter):
        """
        Generate quarterly conflict report
        
        Args:
            year (int): Year for the report
            quarter (int): Quarter for the report (1-4)
            
        Returns:
            dict: Quarterly report data
        """
        quarters = {
            1: (1, 3), 2: (4, 6), 3: (7, 9), 4: (10, 12)
        }
        
        if quarter not in quarters:
            raise ValueError("Quarter must be 1, 2, 3, or 4")
        
        start_month, end_month = quarters[quarter]
        start_date = f"{year}-{start_month:02d}-01"
        if end_month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{end_month+1:02d}-01"
        
        conn = sqlite3.connect(self.db_path)
        
        try:
            # Get quarterly statistics
            quarterly_stats_query = f'''
                SELECT 
                    COUNT(*) as total_days,
                    SUM(event_count) as total_events,
                    SUM(total_fatalities) as total_fatalities,
                    AVG(intensity_score) as avg_intensity_score,
                    MAX(intensity_score) as peak_intensity_score
                FROM countries_intensity 
                WHERE date >= '{start_date}' AND date < '{end_date}'
            '''
            quarterly_stats_df = pd.read_sql_query(quarterly_stats_query, conn)
            
            # Get top countries by quarter
            top_countries_query = f'''
                SELECT 
                    country,
                    SUM(event_count) as total_events,
                    SUM(total_fatalities) as total_fatalities,
                    AVG(intensity_score) as avg_intensity,
                    MAX(intensity_score) as peak_intensity
                FROM countries_intensity 
                WHERE date >= '{start_date}' AND date < '{end_date}'
                GROUP BY country
                ORDER BY total_events DESC
                LIMIT 15
            '''
            top_countries_df = pd.read_sql_query(top_countries_query, conn)
            
            report = {
                'report_type': 'quarterly',
                'period': f"Q{quarter} {year}",
                'generated_at': datetime.now().isoformat(),
                'summary': {
                    'total_days': int(quarterly_stats_df['total_days'].iloc[0] or 0),
                    'total_events': int(quarterly_stats_df['total_events'].iloc[0] or 0),
                    'total_fatalities': int(quarterly_stats_df['total_fatalities'].iloc[0] or 0),
                    'avg_intensity_score': float(quarterly_stats_df['avg_intensity_score'].iloc[0] or 0),
                    'peak_intensity_score': float(quarterly_stats_df['peak_intensity_score'].iloc[0] or 0)
                },
                'top_conflict_countries': top_countries_df.to_dict('records')
            }
            
            return report
            
        finally:
            conn.close()
    
    def get_annual_report(self, year):
        """
        Generate annual conflict report
        
        Args:
            year (int): Year for the report
            
        Returns:
            dict: Annual report data
        """
        start_date = f"{year}-01-01"
        end_date = f"{year+1}-01-01"
        
        conn = sqlite3.connect(self.db_path)
        
        try:
            # Get annual statistics
            annual_stats_query = f'''
                SELECT 
                    COUNT(DISTINCT date) as active_conflict_days,
                    SUM(event_count) as total_events,
                    SUM(total_fatalities) as total_fatalities,
                    AVG(intensity_score) as avg_intensity_score,
                    MAX(intensity_score) as peak_intensity_score
                FROM countries_intensity 
                WHERE date >= '{start_date}' AND date < '{end_date}'
            '''
            annual_stats_df = pd.read_sql_query(annual_stats_query, conn)
            
            # Get all countries with conflict data
            all_countries_query = f'''
                SELECT 
                    country,
                    COUNT(*) as days_with_data,
                    SUM(event_count) as total_events,
                    SUM(total_fatalities) as total_fatalities,
                    AVG(intensity_score) as avg_intensity,
                    MAX(intensity_score) as peak_intensity,
                    MIN(intensity_score) as min_intensity
                FROM countries_intensity 
                WHERE date >= '{start_date}' AND date < '{end_date}'
                GROUP BY country
                ORDER BY avg_intensity DESC
            '''
            all_countries_df = pd.read_sql_query(all_countries_query, conn)
            
            report = {
                'report_type': 'annual',
                'period': str(year),
                'generated_at': datetime.now().isoformat(),
                'summary': {
                    'active_conflict_days': int(annual_stats_df['active_conflict_days'].iloc[0] or 0),
                    'total_events': int(annual_stats_df['total_events'].iloc[0] or 0),
                    'total_fatalities': int(annual_stats_df['total_fatalities'].iloc[0] or 0),
                    'avg_intensity_score': float(annual_stats_df['avg_intensity_score'].iloc[0] or 0),
                    'peak_intensity_score': float(annual_stats_df['peak_intensity_score'].iloc[0] or 0)
                },
                'all_conflict_countries': all_countries_df.to_dict('records')
            }
            
            return report
            
        finally:
            conn.close()
    
    def save_report_to_file(self, report, filename=None):
        """
        Save report to JSON file
        
        Args:
            report (dict): Report data to save
            filename (str): Optional filename, auto-generated if not provided
        """
        if filename is None:
            period = report['period'].replace(' ', '_').replace('-', '_').replace('to', 'to')
            report_type = report['report_type']
            filename = f"{self.reports_dir}/{report_type}/{period}_conflict_report.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Report saved to {filename}")
        return filename
    
    def generate_and_save_weekly_report(self, start_date=None, end_date=None):
        """Generate and save weekly report"""
        report = self.get_weekly_report(start_date, end_date)
        filename = self.save_report_to_file(report)
        return filename
    
    def generate_and_save_monthly_report(self, year, month):
        """Generate and save monthly report"""
        report = self.get_monthly_report(year, month)
        filename = self.save_report_to_file(report)
        return filename
    
    def generate_and_save_quarterly_report(self, year, quarter):
        """Generate and save quarterly report"""
        report = self.get_quarterly_report(year, quarter)
        filename = self.save_report_to_file(report)
        return filename
    
    def generate_and_save_annual_report(self, year):
        """Generate and save annual report"""
        report = self.get_annual_report(year)
        filename = self.save_report_to_file(report)
        return filename

def main():
    parser = argparse.ArgumentParser(description='Generate conflict analysis reports')
    parser.add_argument('--type', choices=['weekly', 'monthly', 'quarterly', 'annual'], 
                       required=True, help='Type of report to generate')
    parser.add_argument('--year', type=int, default=datetime.now().year,
                       help='Year for the report (default: current year)')
    parser.add_argument('--month', type=int, 
                       help='Month for monthly report (1-12)')
    parser.add_argument('--quarter', type=int, choices=[1, 2, 3, 4],
                       help='Quarter for quarterly report (1-4)')
    parser.add_argument('--start-date', type=str,
                       help='Start date for weekly report (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str,
                       help='End date for weekly report (YYYY-MM-DD)')
    parser.add_argument('--output', type=str,
                       help='Output file path (optional, auto-generated if not provided)')
    
    args = parser.parse_args()
    
    generator = ConflictReportGenerator()
    
    try:
        if args.type == 'weekly':
            filename = generator.generate_and_save_weekly_report(args.start_date, args.end_date)
            
        elif args.type == 'monthly':
            if args.month is None:
                print("Error: --month is required for monthly reports")
                sys.exit(1)
            if not (1 <= args.month <= 12):
                print("Error: Month must be between 1 and 12")
                sys.exit(1)
            filename = generator.generate_and_save_monthly_report(args.year, args.month)
            
        elif args.type == 'quarterly':
            if args.quarter is None:
                print("Error: --quarter is required for quarterly reports")
                sys.exit(1)
            filename = generator.generate_and_save_quarterly_report(args.year, args.quarter)
            
        elif args.type == 'annual':
            filename = generator.generate_and_save_annual_report(args.year)
        
        print(f"Report generated successfully: {filename}")
        
    except Exception as e:
        print(f"Error generating report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()