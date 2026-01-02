#!/usr/bin/env python3
"""
Meals Tracker Data Management
Handles Google Sheets storage and retrieval of meal entries
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import gspread
from google.oauth2.service_account import Credentials


class MealsTracker:
    def __init__(self, use_sheets: bool = True, sheet_name: str = "TDEE Tracker Data", user: str = "Default"):
        """
        Initialize meals tracker with Google Sheets or JSON fallback
        
        Args:
            use_sheets: If True, use Google Sheets. If False or credentials missing, use JSON
            sheet_name: Name of the Google Sheet to use
            user: Username to separate data (creates separate worksheet per user)
        """
        self.use_sheets = use_sheets
        self.sheet_name = sheet_name
        self.user = user
        self.data_file = f"meals_data_{user}.json"
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
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = None
        
        # Try Streamlit secrets first
        try:
            import streamlit as st
            if 'gcp_service_account' in st.secrets:
                creds = Credentials.from_service_account_info(
                    st.secrets["gcp_service_account"],
                    scopes=scope
                )
        except:
            pass
        
        # Fall back to credentials.json
        if creds is None:
            if os.path.exists('credentials.json'):
                creds = Credentials.from_service_account_file(
                    'credentials.json',
                    scopes=scope
                )
            else:
                raise FileNotFoundError("credentials.json not found")
        
        client = gspread.authorize(creds)
        spreadsheet = client.open(self.sheet_name)
        
        # Create or get user-specific worksheet for meals
        worksheet_name = f"{self.user}_Meals"
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            # Create new worksheet for this user's meals
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=10)
            # Add headers
            headers = ['date', 'time', 'meal_name', 'calories', 'protein', 'carbs', 'fat']
            worksheet.update('A1:G1', [headers])
        
        return worksheet
    
    def load_data(self) -> Dict:
        """Load meal data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_data(self, data: Dict):
        """Save meal data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_meal(self, date: str, meal_data: Dict):
        """Add a meal entry for a specific date"""
        if self.use_sheets:
            # Add to Google Sheets
            row = [
                date,
                meal_data.get('time', ''),
                meal_data.get('name', ''),
                meal_data.get('calories', 0),
                meal_data.get('protein', 0),
                meal_data.get('carbs', 0),
                meal_data.get('fat', 0)
            ]
            self.worksheet.append_row(row)
        else:
            # Add to JSON
            if date not in self.data:
                self.data[date] = []
            self.data[date].append(meal_data)
            self.save_data(self.data)
    
    def get_meals_for_date(self, date: str) -> List[Dict]:
        """Get all meals for a specific date"""
        if self.use_sheets:
            # Fetch from Google Sheets
            all_values = self.worksheet.get_all_values()
            meals = []
            
            for row in all_values[1:]:  # Skip header
                if row and row[0] == date:
                    meal = {
                        'time': row[1] if len(row) > 1 else '',
                        'name': row[2] if len(row) > 2 else '',
                        'calories': int(row[3]) if len(row) > 3 and row[3] else 0,
                        'protein': int(row[4]) if len(row) > 4 and row[4] else 0,
                        'carbs': int(row[5]) if len(row) > 5 and row[5] else 0,
                        'fat': int(row[6]) if len(row) > 6 and row[6] else 0
                    }
                    meals.append(meal)
            
            return meals
        else:
            # Get from JSON
            return self.data.get(date, [])
    
    def delete_meal(self, date: str, meal_index: int):
        """Delete a meal at the specified index for a date"""
        if self.use_sheets:
            # Find and delete from Google Sheets
            all_values = self.worksheet.get_all_values()
            date_meals_count = 0
            row_to_delete = None
            
            for idx, row in enumerate(all_values[1:], start=2):  # Start from row 2 (skip header)
                if row and row[0] == date:
                    if date_meals_count == meal_index:
                        row_to_delete = idx
                        break
                    date_meals_count += 1
            
            if row_to_delete:
                self.worksheet.delete_rows(row_to_delete)
        else:
            # Delete from JSON
            if date in self.data and meal_index < len(self.data[date]):
                self.data[date].pop(meal_index)
                if not self.data[date]:
                    del self.data[date]
                self.save_data(self.data)
