#!/usr/bin/env python3
"""
Daily Tracker Data Management
Handles Google Sheets storage and retrieval of daily entries
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import statistics
import gspread
from google.oauth2.service_account import Credentials


class DailyTracker:
    def __init__(self, use_sheets: bool = True, sheet_name: str = "TDEE Tracker Data"):
        """
        Initialize tracker with Google Sheets or JSON fallback
        
        Args:
            use_sheets: If True, use Google Sheets. If False or credentials missing, use JSON
            sheet_name: Name of the Google Sheet to use
        """
        self.use_sheets = use_sheets
        self.sheet_name = sheet_name
        self.data_file = "tracker_data.json"
        self.worksheet = None
        
        if use_sheets:
            try:
                self.worksheet = self._connect_to_sheets()
            except Exception as e:
                print(f"Failed to connect to Google Sheets: {e}")
                print("Falling back to JSON storage")
                self.use_sheets = False
        
        if not self.use_sheets:
            self.data = self.load_data()
    
    def _connect_to_sheets(self):
        """Connect to Google Sheets using service account credentials"""
        # Define the scope
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = None
        
        # Try to load credentials from Streamlit secrets first (for deployment)
        try:
            import streamlit as st
            # Check if secrets exist without triggering the warning
            try:
                if 'gcp_service_account' in st.secrets:
                    creds = Credentials.from_service_account_info(
                        st.secrets["gcp_service_account"],
                        scopes=scope
                    )
                    print("Using Streamlit secrets for Google Sheets")
            except:
                # Secrets don't exist, will use credentials.json
                pass
        except ImportError:
            # Streamlit not imported yet, will use credentials.json
            pass
        
        # Fall back to local credentials file if secrets not found
        if creds is None:
            if os.path.exists('credentials.json'):
                creds = Credentials.from_service_account_file(
                    'credentials.json',
                    scopes=scope
                )
                print("Using credentials.json for Google Sheets")
            else:
                raise FileNotFoundError(
                    "credentials.json not found. Please follow GOOGLE_SHEETS_SETUP.md to set up Google Sheets."
                )
        
        client = gspread.authorize(creds)
        
        # Try to open existing sheet first
        try:
            spreadsheet = client.open(self.sheet_name)
            print(f"Connected to existing sheet: {self.sheet_name}")
        except gspread.SpreadsheetNotFound:
            # If sheet doesn't exist, provide instructions
            raise FileNotFoundError(
                f"\n\nGoogle Sheet '{self.sheet_name}' not found.\n\n"
                f"Please create it manually:\n"
                f"1. Go to https://sheets.google.com\n"
                f"2. Create a new sheet named '{self.sheet_name}'\n"
                f"3. Share it with this email (found in credentials.json):\n"
                f"   {creds.service_account_email}\n"
                f"   Give it 'Editor' access\n"
                f"4. Restart the app\n"
            )
        
        # Get or create the main worksheet
        try:
            worksheet = spreadsheet.worksheet("Entries")
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title="Entries", rows=1000, cols=20)
            # Add header row
            headers = ['date', 'weight', 'calories', 'protein', 'carbs', 'fat', 'steps', 
                      'sleep_hours', 'sleep_quality', 'water_oz', 'workout_done', 
                      'workout_type', 'workout_duration', 'rest_time', 'training_style', 
                      'energy_level', 'notes']
            worksheet.update('A1:Q1', [headers])
            print("Created 'Entries' worksheet with headers")
        
        return worksheet
    
    def load_data(self) -> Dict:
        """Load data from JSON file (fallback method)"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_data(self):
        """Save data to JSON file (fallback method)"""
        if not self.use_sheets:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
    
    def _row_to_dict(self, row: List, headers: List) -> Dict:
        """Convert a spreadsheet row to a dictionary"""
        entry = {}
        for i, header in enumerate(headers):
            if i < len(row) and row[i]:
                value = row[i]
                # Convert strings to appropriate types
                if header in ['weight', 'calories', 'protein', 'carbs', 'fat', 
                             'steps', 'sleep_hours', 'water_oz', 'workout_duration']:
                    try:
                        entry[header] = float(value) if '.' in str(value) else int(value)
                    except (ValueError, TypeError):
                        entry[header] = value
                elif header == 'workout_done':
                    entry[header] = str(value).lower() in ['true', '1', 'yes']
                else:
                    entry[header] = value
        return entry
    
    def _dict_to_row(self, date: str, entry_data: Dict, headers: List) -> List:
        """Convert a dictionary to a spreadsheet row"""
        row = [date]  # Start with date
        for header in headers[1:]:  # Skip 'date' as we already added it
            value = entry_data.get(header, '')
            # Convert booleans to strings for sheets
            if isinstance(value, bool):
                row.append('TRUE' if value else 'FALSE')
            else:
                row.append(str(value) if value is not None else '')
        return row
    
    def add_entry(self, date: str, entry_data: Dict):
        """Add or update an entry for a specific date"""
        if self.use_sheets and self.worksheet:
            try:
                # Get all records to find if date exists
                all_records = self.worksheet.get_all_values()
                headers = all_records[0] if all_records else []
                
                # Find row with matching date
                row_index = None
                for i, row in enumerate(all_records[1:], start=2):
                    if row and row[0] == date:
                        row_index = i
                        break
                
                # Prepare the row data
                row_data = self._dict_to_row(date, entry_data, headers)
                
                if row_index:
                    # Update existing row
                    self.worksheet.update(f'A{row_index}:Q{row_index}', [row_data])
                else:
                    # Append new row
                    self.worksheet.append_row(row_data)
                
            except Exception as e:
                print(f"Error saving to Google Sheets: {e}")
                print("Falling back to JSON")
                self.use_sheets = False
                self.data = self.load_data()
                self.data[date] = entry_data
                self.save_data()
        else:
            self.data[date] = entry_data
            self.save_data()
    
    def get_entry(self, date: str) -> Optional[Dict]:
        """Get entry for a specific date"""
        if self.use_sheets and self.worksheet:
            try:
                all_records = self.worksheet.get_all_values()
                if len(all_records) < 2:
                    return None
                
                headers = all_records[0]
                for row in all_records[1:]:
                    if row and row[0] == date:
                        return self._row_to_dict(row, headers)
                return None
            except Exception as e:
                print(f"Error reading from Google Sheets: {e}")
                return self.data.get(date) if hasattr(self, 'data') else None
        else:
            return self.data.get(date)
    
    def get_previous_entry(self, current_date: str) -> Optional[Dict]:
        """Get the most recent entry before the current date"""
        if self.use_sheets and self.worksheet:
            try:
                all_records = self.worksheet.get_all_values()
                if len(all_records) < 2:
                    return None, None
                
                headers = all_records[0]
                dates = [(row[0], row) for row in all_records[1:] if row and row[0] < current_date]
                if dates:
                    dates.sort(reverse=True)
                    prev_date, prev_row = dates[0]
                    return self._row_to_dict(prev_row, headers), prev_date
                return None, None
            except Exception as e:
                print(f"Error reading from Google Sheets: {e}")
                if hasattr(self, 'data'):
                    dates = sorted([d for d in self.data.keys() if d < current_date], reverse=True)
                    if dates:
                        return self.data[dates[0]], dates[0]
                return None, None
        else:
            dates = sorted([d for d in self.data.keys() if d < current_date], reverse=True)
            if dates:
                return self.data[dates[0]], dates[0]
            return None, None
    
    def get_week_entries(self, end_date: str, days: int = 7) -> List[Dict]:
        """Get entries for the past N days"""
        end = datetime.strptime(end_date, '%Y-%m-%d')
        start = end - timedelta(days=days-1)
        
        if self.use_sheets and self.worksheet:
            try:
                all_records = self.worksheet.get_all_values()
                if len(all_records) < 2:
                    return []
                
                headers = all_records[0]
                entries = []
                for row in all_records[1:]:
                    if row and row[0]:
                        entry_date = datetime.strptime(row[0], '%Y-%m-%d')
                        if start <= entry_date <= end:
                            entry_dict = self._row_to_dict(row, headers)
                            entry_dict['date'] = row[0]
                            entries.append(entry_dict)
                
                return sorted(entries, key=lambda x: x['date'])
            except Exception as e:
                print(f"Error reading from Google Sheets: {e}")
                if hasattr(self, 'data'):
                    entries = []
                    for date_str, entry in self.data.items():
                        entry_date = datetime.strptime(date_str, '%Y-%m-%d')
                        if start <= entry_date <= end:
                            entries.append({**entry, 'date': date_str})
                    return sorted(entries, key=lambda x: x['date'])
                return []
        else:
            entries = []
            for date_str, entry in self.data.items():
                entry_date = datetime.strptime(date_str, '%Y-%m-%d')
                if start <= entry_date <= end:
                    entries.append({**entry, 'date': date_str})
            
            return sorted(entries, key=lambda x: x['date'])
    
    def get_all_entries(self) -> List[Dict]:
        """Get all entries sorted by date"""
        if self.use_sheets and self.worksheet:
            try:
                all_records = self.worksheet.get_all_values()
                if len(all_records) < 2:
                    return []
                
                headers = all_records[0]
                entries = []
                for row in all_records[1:]:
                    if row and row[0]:  # Check if row has a date
                        entry_dict = self._row_to_dict(row, headers)
                        entry_dict['date'] = row[0]
                        entries.append(entry_dict)
                
                return sorted(entries, key=lambda x: x['date'])
            except Exception as e:
                print(f"Error reading from Google Sheets: {e}")
                if hasattr(self, 'data'):
                    entries = []
                    for date_str, entry in self.data.items():
                        entries.append({**entry, 'date': date_str})
                    return sorted(entries, key=lambda x: x['date'])
                return []
        else:
            entries = []
            for date_str, entry in self.data.items():
                entries.append({**entry, 'date': date_str})
            
            return sorted(entries, key=lambda x: x['date'])
    
    def calculate_weekly_averages(self, end_date: str) -> Dict:
        """Calculate averages for the past week"""
        entries = self.get_week_entries(end_date, days=7)
        
        if not entries:
            return None
        
        # Calculate averages
        weights = [e['weight'] for e in entries if e.get('weight')]
        calories = [e['calories'] for e in entries if e.get('calories')]
        proteins = [e['protein'] for e in entries if e.get('protein')]
        carbs = [e['carbs'] for e in entries if e.get('carbs')]
        fats = [e['fat'] for e in entries if e.get('fat')]
        sleep_hours = [e['sleep_hours'] for e in entries if e.get('sleep_hours')]
        steps = [e['steps'] for e in entries if e.get('steps')]
        workouts = [e for e in entries if e.get('workout_done')]
        
        return {
            'avg_weight': statistics.mean(weights) if weights else None,
            'avg_calories': statistics.mean(calories) if calories else None,
            'avg_protein': statistics.mean(proteins) if proteins else None,
            'avg_carbs': statistics.mean(carbs) if carbs else None,
            'avg_fat': statistics.mean(fats) if fats else None,
            'avg_sleep': statistics.mean(sleep_hours) if sleep_hours else None,
            'avg_steps': statistics.mean(steps) if steps else None,
            'total_workouts': len(workouts),
            'days_tracked': len(entries),
            'weight_change': weights[-1] - weights[0] if len(weights) >= 2 else None
        }
    
    def get_all_dates(self) -> List[str]:
        """Get all dates with entries"""
        return sorted(self.data.keys(), reverse=True)


if __name__ == "__main__":
    # Test the tracker
    tracker = DailyTracker()
    
    # Add test entry
    test_entry = {
        'weight': 180,
        'calories': 1840,
        'protein': 172,
        'carbs': 196,
        'fat': 41,
        'sleep_hours': 7.5,
        'sleep_quality': 'good',
        'steps': 4500,
        'workout_done': True,
        'workout_duration': 75,
        'workout_type': 'Heavy Lifting',
        'notes': 'Test entry'
    }
    
    tracker.add_entry('2026-01-01', test_entry)
    print("Test entry added successfully!")
    
    # Get weekly averages
    averages = tracker.calculate_weekly_averages('2026-01-01')
    print(f"Weekly averages: {averages}")
