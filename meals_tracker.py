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
            # Add headers (removed date and time - just meal library)
            headers = ['meal_name', 'calories', 'protein', 'carbs', 'fat']
            worksheet.update('A1:E1', [headers])
        
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
    
    def add_meal(self, meal_data: Dict):
        """Add a meal entry to the meal library"""
        if self.use_sheets:
            # Add to Google Sheets
            row = [
                meal_data.get('name', ''),
                meal_data.get('calories', 0),
                meal_data.get('protein', 0),
                meal_data.get('carbs', 0),
                meal_data.get('fat', 0)
            ]
            self.worksheet.append_row(row)
        else:
            # Add to JSON
            if 'meals' not in self.data:
                self.data['meals'] = []
            self.data['meals'].append(meal_data)
            self.save_data(self.data)
    
    def get_all_meals(self) -> List[Dict]:
        """Get all meals in the library"""
        if self.use_sheets:
            # Fetch from Google Sheets
            all_values = self.worksheet.get_all_values()
            meals = []
            
            for row in all_values[1:]:  # Skip header
                if row and row[0]:  # If meal name exists
                    meal = {
                        'name': row[0] if len(row) > 0 else '',
                        'calories': int(row[1]) if len(row) > 1 and row[1] else 0,
                        'protein': int(row[2]) if len(row) > 2 and row[2] else 0,
                        'carbs': int(row[3]) if len(row) > 3 and row[3] else 0,
                        'fat': int(row[4]) if len(row) > 4 and row[4] else 0
                    }
                    meals.append(meal)
            
            return meals
        else:
            # Get from JSON
            return self.data.get('meals', [])
    
    def delete_meal(self, meal_index: int):
        """Delete a meal at the specified index"""
        if self.use_sheets:
            # Delete from Google Sheets (row index + 2 to account for header and 0-based indexing)
            row_to_delete = meal_index + 2
            self.worksheet.delete_rows(row_to_delete)
        else:
            # Delete from JSON
            if 'meals' in self.data and meal_index < len(self.data['meals']):
                self.data['meals'].pop(meal_index)
                self.save_data(self.data)
    
    def update_meal(self, meal_index: int, meal_data: Dict):
        """Update a meal at the specified index"""
        if self.use_sheets:
            # Update in Google Sheets (row index + 2 to account for header and 0-based indexing)
            row_to_update = meal_index + 2
            row = [
                meal_data.get('name', ''),
                meal_data.get('calories', 0),
                meal_data.get('protein', 0),
                meal_data.get('carbs', 0),
                meal_data.get('fat', 0)
            ]
            self.worksheet.update(f'A{row_to_update}:E{row_to_update}', [row])
        else:
            # Update in JSON
            if 'meals' in self.data and meal_index < len(self.data['meals']):
                self.data['meals'][meal_index] = meal_data
                self.save_data(self.data)
