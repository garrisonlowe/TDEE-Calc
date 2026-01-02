#!/usr/bin/env python3
"""
Authentication Module
Handles user login, registration, and password management
"""

import hashlib
import json
from typing import Optional, Dict
import gspread
from google.oauth2.service_account import Credentials
import os


class AuthManager:
    def __init__(self, sheet_name: str = "TDEE Tracker Data"):
        """Initialize authentication manager with Google Sheets"""
        self.sheet_name = sheet_name
        self.spreadsheet = None
        self.users_worksheet = None
        self._connect_to_sheets()
    
    def _connect_to_sheets(self):
        """Connect to Google Sheets"""
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
        self.spreadsheet = client.open(self.sheet_name)
        
        # Get or create Users worksheet
        try:
            self.users_worksheet = self.spreadsheet.worksheet("Users")
        except gspread.WorksheetNotFound:
            self.users_worksheet = self.spreadsheet.add_worksheet(title="Users", rows=100, cols=20)
            # Add headers
            headers = ['username', 'password_hash', 'display_name', 'sex', 'height_ft', 
                      'height_in', 'weight_lbs', 'age', 'body_fat_pct', 'daily_steps', 
                      'step_pace', 'job_type', 'sedentary_hours', 'workouts_per_week',
                      'workout_duration', 'workout_type', 'workout_intensity', 
                      'daily_protein', 'daily_carbs', 'daily_fat', 'daily_calories',
                      'sleep_hours', 'sleep_quality']
            self.users_worksheet.update('A1:W1', [headers])
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str, user_data: Dict) -> bool:
        """Create a new user account"""
        try:
            # Check if username exists
            all_users = self.users_worksheet.get_all_values()
            for row in all_users[1:]:  # Skip header
                if row and row[0].lower() == username.lower():
                    return False  # Username already exists
            
            # Hash password
            password_hash = self._hash_password(password)
            
            # Prepare user row
            row = [
                username,
                password_hash,
                user_data.get('display_name', username),
                user_data.get('sex', 'Male'),
                user_data.get('height_ft', 5),
                user_data.get('height_in', 11),
                user_data.get('weight_lbs', 180),
                user_data.get('age', 26),
                user_data.get('body_fat_pct', 19),
                user_data.get('daily_steps', 4500),
                user_data.get('step_pace', 'Average'),
                user_data.get('job_type', 'Desk Job'),
                user_data.get('sedentary_hours', 10),
                user_data.get('workouts_per_week', 3),
                user_data.get('workout_duration', 77),
                user_data.get('workout_type', 'Heavy Lifting'),
                user_data.get('workout_intensity', 'High'),
                user_data.get('daily_protein', 172),
                user_data.get('daily_carbs', 196),
                user_data.get('daily_fat', 41),
                user_data.get('daily_calories', 1840),
                user_data.get('sleep_hours', 9),
                user_data.get('sleep_quality', 'Good')
            ]
            
            self.users_worksheet.append_row(row)
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data if successful"""
        try:
            password_hash = self._hash_password(password)
            all_users = self.users_worksheet.get_all_values()
            
            if len(all_users) < 2:
                return None
            
            headers = all_users[0]
            for row in all_users[1:]:
                if row and row[0].lower() == username.lower() and row[1] == password_hash:
                    # User authenticated, return user data
                    user_data = {}
                    for i, header in enumerate(headers):
                        if i < len(row):
                            user_data[header] = row[i]
                    return user_data
            
            return None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def update_user_data(self, username: str, user_data: Dict) -> bool:
        """Update user profile data"""
        try:
            all_users = self.users_worksheet.get_all_values()
            headers = all_users[0]
            
            for i, row in enumerate(all_users[1:], start=2):
                if row and row[0].lower() == username.lower():
                    # Update the row
                    updated_row = [username, row[1]]  # Keep username and password_hash
                    
                    # Add all other fields
                    updated_row.extend([
                        user_data.get('display_name', row[2] if len(row) > 2 else username),
                        user_data.get('sex', row[3] if len(row) > 3 else 'Male'),
                        user_data.get('height_ft', row[4] if len(row) > 4 else 5),
                        user_data.get('height_in', row[5] if len(row) > 5 else 11),
                        user_data.get('weight_lbs', row[6] if len(row) > 6 else 180),
                        user_data.get('age', row[7] if len(row) > 7 else 26),
                        user_data.get('body_fat_pct', row[8] if len(row) > 8 else 19),
                        user_data.get('daily_steps', row[9] if len(row) > 9 else 4500),
                        user_data.get('step_pace', row[10] if len(row) > 10 else 'Average'),
                        user_data.get('job_type', row[11] if len(row) > 11 else 'Desk Job'),
                        user_data.get('sedentary_hours', row[12] if len(row) > 12 else 10),
                        user_data.get('workouts_per_week', row[13] if len(row) > 13 else 3),
                        user_data.get('workout_duration', row[14] if len(row) > 14 else 77),
                        user_data.get('workout_type', row[15] if len(row) > 15 else 'Heavy Lifting'),
                        user_data.get('workout_intensity', row[16] if len(row) > 16 else 'High'),
                        user_data.get('daily_protein', row[17] if len(row) > 17 else 172),
                        user_data.get('daily_carbs', row[18] if len(row) > 18 else 196),
                        user_data.get('daily_fat', row[19] if len(row) > 19 else 41),
                        user_data.get('daily_calories', row[20] if len(row) > 20 else 1840),
                        user_data.get('sleep_hours', row[21] if len(row) > 21 else 9),
                        user_data.get('sleep_quality', row[22] if len(row) > 22 else 'Good')
                    ])
                    
                    self.users_worksheet.update(f'A{i}:W{i}', [updated_row])
                    return True
            
            return False
        except Exception as e:
            print(f"Error updating user data: {e}")
            return False
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            # Verify old password
            old_hash = self._hash_password(old_password)
            all_users = self.users_worksheet.get_all_values()
            
            for i, row in enumerate(all_users[1:], start=2):
                if row and row[0].lower() == username.lower() and row[1] == old_hash:
                    # Update password
                    new_hash = self._hash_password(new_password)
                    self.users_worksheet.update(f'B{i}', [[new_hash]])
                    return True
            
            return False
        except Exception as e:
            print(f"Error changing password: {e}")
            return False
