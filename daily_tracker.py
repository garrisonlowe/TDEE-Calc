#!/usr/bin/env python3
"""
Daily Tracker Data Management
Handles JSON storage and retrieval of daily entries
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import statistics


class DailyTracker:
    def __init__(self, data_file: str = "tracker_data.json"):
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_data(self):
        """Save data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_entry(self, date: str, entry_data: Dict):
        """Add or update an entry for a specific date"""
        self.data[date] = entry_data
        self.save_data()
    
    def get_entry(self, date: str) -> Optional[Dict]:
        """Get entry for a specific date"""
        return self.data.get(date)
    
    def get_previous_entry(self, current_date: str) -> Optional[Dict]:
        """Get the most recent entry before the current date"""
        dates = sorted([d for d in self.data.keys() if d < current_date], reverse=True)
        if dates:
            return self.data[dates[0]], dates[0]
        return None, None
    
    def get_week_entries(self, end_date: str, days: int = 7) -> List[Dict]:
        """Get entries for the past N days"""
        end = datetime.strptime(end_date, '%Y-%m-%d')
        start = end - timedelta(days=days-1)
        
        entries = []
        for date_str, entry in self.data.items():
            entry_date = datetime.strptime(date_str, '%Y-%m-%d')
            if start <= entry_date <= end:
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
