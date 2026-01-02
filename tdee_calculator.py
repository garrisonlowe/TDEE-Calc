#!/usr/bin/env python3
"""
Comprehensive TDEE Calculator
Based on latest research for maximum accuracy
Includes metabolic adaptation detection and real-world validation
"""

import math
from typing import Dict, Tuple, Optional

class TDEECalculator:
    """
    Advanced TDEE calculator incorporating:
    - Multiple BMR formulas (Mifflin-St Jeor, Katch-McArdle)
    - Macro-specific TEF calculation
    - Detailed activity breakdown (steps, workouts, NEAT)
    - EPOC effects from different training styles
    - Weight trend validation for metabolic adaptation detection
    """
    
    def __init__(self):
        # MET values for different walking speeds
        self.walking_mets = {
            'slow': 2.8,      # 2.0 mph / 3.2 km/h
            'average': 3.8,   # 3.0 mph / 4.8 km/h
            'brisk': 4.8,     # 3.9 mph / 6.3 km/h
            'very_brisk': 5.5 # 4.5 mph
        }
        
        # TEF percentages by macronutrient
        self.tef_rates = {
            'protein': 0.25,  # 20-30%, using 25%
            'carbs': 0.075,   # 5-10%, using 7.5%
            'fat': 0.015      # 0-3%, using 1.5%
        }
    
    def calculate_bmr_mifflin(self, weight_kg: float, height_cm: float, 
                              age: int, sex: str) -> float:
        """
        Mifflin-St Jeor equation (1990)
        Most accurate for general population
        Accuracy: within 10% for 82% of non-obese, 70% of obese
        """
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
        
        if sex.lower() in ['male', 'm']:
            bmr += 5
        else:  # female
            bmr -= 161
        
        return bmr
    
    def calculate_bmr_katch(self, lean_body_mass_kg: float) -> float:
        """
        Katch-McArdle formula
        Most accurate for lean individuals when body fat % is known
        Based on lean body mass rather than total weight
        """
        return 370 + (21.6 * lean_body_mass_kg)
    
    def calculate_lean_mass(self, weight_kg: float, body_fat_pct: float) -> float:
        """Calculate lean body mass from weight and body fat percentage"""
        fat_mass = weight_kg * (body_fat_pct / 100)
        return weight_kg - fat_mass
    
    def calculate_tef(self, total_calories: float, protein_g: float, 
                      carbs_g: float, fat_g: float) -> Dict[str, float]:
        """
        Calculate Thermic Effect of Food based on macro breakdown
        Much more accurate than the generic 10% estimate
        
        Returns both total TEF and breakdown by macro
        """
        # Calculate calories from each macro
        protein_cal = protein_g * 4
        carbs_cal = carbs_g * 4
        fat_cal = fat_g * 9
        
        # Calculate TEF for each
        protein_tef = protein_cal * self.tef_rates['protein']
        carbs_tef = carbs_cal * self.tef_rates['carbs']
        fat_tef = fat_cal * self.tef_rates['fat']
        
        total_tef = protein_tef + carbs_tef + fat_tef
        tef_percentage = (total_tef / total_calories * 100) if total_calories > 0 else 0
        
        return {
            'total_tef': total_tef,
            'protein_tef': protein_tef,
            'carbs_tef': carbs_tef,
            'fat_tef': fat_tef,
            'tef_percentage': tef_percentage
        }
    
    def calculate_neat_from_steps(self, steps: int, weight_kg: float, 
                                   height_cm: float, pace: str = 'average') -> float:
        """
        Calculate calories from steps using MET values
        More accurate than simple 0.04 cal/step estimates
        """
        # Calculate stride length (41.4% of height)
        stride_length_cm = height_cm * 0.414
        stride_length_m = stride_length_cm / 100
        
        # Calculate distance walked
        distance_m = steps * stride_length_m  # each step = one stride
        distance_km = distance_m / 1000
        
        # Estimate time based on pace
        pace_speeds = {
            'slow': 3.2,      # km/h
            'average': 4.8,
            'brisk': 6.3,
            'very_brisk': 7.2
        }
        
        speed_kmh = pace_speeds.get(pace, 4.8)
        time_hours = distance_km / speed_kmh
        
        # Calculate calories using MET formula
        # Calories = MET × weight(kg) × time(hours)
        met_value = self.walking_mets.get(pace, 3.8)
        calories = met_value * weight_kg * time_hours
        
        return calories
    
    def calculate_epoc(self, workout_type: str, duration_minutes: float, 
                       intensity: str = 'high') -> float:
        """
        Calculate Excess Post-Exercise Oxygen Consumption
        
        Research findings:
        - Heavy lifting (80%+ 1RM): ~168 kcal over 14 hours post-exercise
        - HIIT: Similar EPOC, ~33 kcal per 30 min elevated for 14 hours
        - Both dissipate by 24 hours
        - Effects last up to 3 days for heavy lifting in some studies
        
        This is a conservative estimate based on research
        """
        # Base EPOC values per hour of workout (conservative estimates)
        epoc_rates = {
            'heavy_lifting': {
                'high': 6.0,    # 80%+ 1RM with long rests
                'moderate': 4.0
            },
            'hiit': {
                'high': 5.5,    # 90%+ VO2max intervals
                'moderate': 4.0
            },
            'circuit_training': {
                'high': 4.5,
                'moderate': 3.0
            },
            'steady_cardio': {
                'high': 2.0,
                'moderate': 1.0
            }
        }
        
        workout_hours = duration_minutes / 60
        rate = epoc_rates.get(workout_type, {}).get(intensity, 0)
        
        # EPOC is primarily in the first 14 hours, then negligible
        # Multiply by effective hours of elevated metabolism
        epoc_calories = rate * workout_hours * 14
        
        return epoc_calories
    
    def calculate_eat(self, workout_type: str, duration_minutes: float,
                      weight_kg: float, intensity: str = 'high') -> float:
        """
        Calculate Exercise Activity Thermogenesis (calories during exercise)
        Using MET values for different activities
        """
        # MET values for different exercises
        exercise_mets = {
            'heavy_lifting': {
                'high': 6.0,     # Heavy resistance, vigorous
                'moderate': 5.0
            },
            'hiit': {
                'high': 12.0,    # Very vigorous
                'moderate': 10.0
            },
            'circuit_training': {
                'high': 8.0,
                'moderate': 6.0
            },
            'steady_cardio': {
                'high': 8.0,
                'moderate': 5.0
            }
        }
        
        met_value = exercise_mets.get(workout_type, {}).get(intensity, 5.0)
        time_hours = duration_minutes / 60
        
        calories = met_value * weight_kg * time_hours
        return calories
    
    def estimate_neat_adjustment(self, job_type: str, sedentary_hours: float) -> float:
        """
        Estimate NEAT multiplier based on job type and sedentary time
        
        Research shows NEAT can vary from 15% to 50% of TDEE
        This is highly individualized
        """
        base_neat_multipliers = {
            'desk': 1.2,      # Minimal movement
            'light_active': 1.3,  # Teacher, retail
            'moderate_active': 1.4,  # Nurse, waiter
            'very_active': 1.5   # Construction, etc.
        }
        
        base = base_neat_multipliers.get(job_type, 1.2)
        
        # Adjust down if high sedentary hours
        if sedentary_hours > 10:
            base *= 0.95
        elif sedentary_hours > 8:
            base *= 0.97
        
        return base
    
    def calculate_sleep_metabolic_adjustment(self, sleep_hours: float, 
                                            sleep_quality: str = 'good') -> Dict:
        """
        Calculate metabolic adjustments based on sleep
        
        Research shows:
        - Sleep deprivation reduces BMR and increases appetite
        - <5 hrs/night: 3.7x obesity risk (men), 2.3x (women)
        - 4 days of poor sleep: 30%+ drop in insulin sensitivity
        - Sleep deprivation: eat 385 more cal/day, burn fewer
        - Optimal: 7-8 hours
        
        Conservative adjustments based on research
        """
        bmr_multiplier = 1.0
        neat_multiplier = 1.0
        metabolic_note = ""
        
        quality_map = {
            'poor': 0.97,      # Poor quality reduces effectiveness
            'fair': 0.99,
            'good': 1.0,
            'excellent': 1.0
        }
        
        quality_factor = quality_map.get(sleep_quality, 1.0)
        
        # Adjust based on sleep duration
        if sleep_hours >= 9:
            # Very long sleep associated with fatigue
            bmr_multiplier = 0.98
            neat_multiplier = 0.95
            metabolic_note = "Long sleep (9+ hrs) associated with reduced activity"
        elif sleep_hours >= 7:
            # Optimal range
            bmr_multiplier = 1.0 * quality_factor
            neat_multiplier = 1.0 * quality_factor
            metabolic_note = "Optimal sleep duration for metabolism"
        elif sleep_hours >= 6:
            # Mild restriction
            bmr_multiplier = 0.97 * quality_factor
            neat_multiplier = 0.93 * quality_factor
            metabolic_note = "Mild sleep restriction - minor metabolic impact"
        elif sleep_hours >= 5:
            # Moderate restriction
            bmr_multiplier = 0.95 * quality_factor
            neat_multiplier = 0.88 * quality_factor
            metabolic_note = "Moderate sleep restriction - significant metabolic impact"
        else:
            # Severe restriction (<5 hours)
            bmr_multiplier = 0.92 * quality_factor
            neat_multiplier = 0.80 * quality_factor
            metabolic_note = "Severe sleep restriction - major metabolic consequences"
        
        return {
            'bmr_multiplier': bmr_multiplier,
            'neat_multiplier': neat_multiplier,
            'metabolic_note': metabolic_note,
            'sleep_hours': sleep_hours,
            'sleep_quality': sleep_quality
        }
    
    def calculate_tdee_formula_based(self, 
                                     weight_kg: float,
                                     height_cm: float,
                                     age: int,
                                     sex: str,
                                     body_fat_pct: Optional[float] = None,
                                     daily_steps: int = 0,
                                     step_pace: str = 'average',
                                     job_type: str = 'desk',
                                     sedentary_hours: float = 8,
                                     workouts_per_week: int = 0,
                                     workout_type: str = 'heavy_lifting',
                                     workout_duration_min: float = 60,
                                     workout_intensity: str = 'high',
                                     daily_protein_g: float = 0,
                                     daily_carbs_g: float = 0,
                                     daily_fat_g: float = 0,
                                     daily_calories: float = 0,
                                     sleep_hours: float = 7.5,
                                     sleep_quality: str = 'good') -> Dict:
        """
        Calculate TDEE using formula-based approach with all factors
        """
        # Calculate sleep impact
        sleep_adjustment = self.calculate_sleep_metabolic_adjustment(sleep_hours, sleep_quality)
        
        # Calculate BMR using both methods
        bmr_mifflin = self.calculate_bmr_mifflin(weight_kg, height_cm, age, sex)
        
        if body_fat_pct:
            lean_mass = self.calculate_lean_mass(weight_kg, body_fat_pct)
            bmr_katch = self.calculate_bmr_katch(lean_mass)
            bmr_base = bmr_katch  # Use Katch-McArdle when body fat % available
            bmr_method = "Katch-McArdle (more accurate with body fat %)"
        else:
            bmr_base = bmr_mifflin
            bmr_katch = None
            bmr_method = "Mifflin-St Jeor"
        
        # Apply sleep adjustment to BMR
        bmr = bmr_base * sleep_adjustment['bmr_multiplier']
        
        # Calculate TEF
        if daily_calories > 0 and (daily_protein_g + daily_carbs_g + daily_fat_g > 0):
            tef_data = self.calculate_tef(daily_calories, daily_protein_g, 
                                         daily_carbs_g, daily_fat_g)
            tef = tef_data['total_tef']
        else:
            # Generic 10% estimate if macros not provided
            tef = daily_calories * 0.10
            tef_data = {'total_tef': tef, 'tef_percentage': 10.0}
        
        # Calculate NEAT from steps (base, then apply sleep adjustment)
        neat_from_steps_base = self.calculate_neat_from_steps(daily_steps, weight_kg, 
                                                              height_cm, step_pace)
        neat_from_steps = neat_from_steps_base * sleep_adjustment['neat_multiplier']
        
        # Calculate EAT (calories during workouts)
        if workouts_per_week > 0:
            eat_per_session = self.calculate_eat(workout_type, workout_duration_min,
                                                 weight_kg, workout_intensity)
            # Average daily EAT
            eat_daily = (eat_per_session * workouts_per_week) / 7
            
            # Calculate EPOC
            epoc_per_session = self.calculate_epoc(workout_type, workout_duration_min,
                                                   workout_intensity)
            # Average daily EPOC
            epoc_daily = (epoc_per_session * workouts_per_week) / 7
        else:
            eat_daily = 0
            epoc_daily = 0
        
        # Estimate additional NEAT from job/lifestyle (with sleep adjustment)
        neat_multiplier = self.estimate_neat_adjustment(job_type, sedentary_hours)
        additional_neat_base = bmr_base * (neat_multiplier - 1.0) - neat_from_steps_base
        if additional_neat_base < 0:
            additional_neat_base = 0
        additional_neat = additional_neat_base * sleep_adjustment['neat_multiplier']
        
        # Calculate total TDEE
        tdee = bmr + tef + neat_from_steps + additional_neat + eat_daily + epoc_daily
        
        return {
            'tdee': tdee,
            'bmr': bmr,
            'bmr_base': bmr_base,
            'bmr_mifflin': bmr_mifflin,
            'bmr_katch': bmr_katch,
            'bmr_method': bmr_method,
            'tef': tef,
            'tef_data': tef_data,
            'neat_from_steps': neat_from_steps,
            'additional_neat': additional_neat,
            'eat_daily': eat_daily,
            'epoc_daily': epoc_daily,
            'sleep_adjustment': sleep_adjustment,
            'breakdown_pct': {
                'bmr': (bmr / tdee * 100),
                'tef': (tef / tdee * 100),
                'neat': ((neat_from_steps + additional_neat) / tdee * 100),
                'eat': (eat_daily / tdee * 100),
                'epoc': (epoc_daily / tdee * 100)
            }
        }
    
    def validate_with_weight_trend(self,
                                   current_tdee_estimate: float,
                                   daily_calories_consumed: float,
                                   weight_change_kg: float,
                                   days_period: int) -> Dict:
        """
        Validate and adjust TDEE estimate using real weight data
        This is the GOLD STANDARD for accuracy
        
        Energy balance: 1 kg fat = ~7700 calories
        If eating X calories for Y days and lost/gained Z kg:
        Actual TDEE = (X + (Z * 7700 / Y))
        """
        if days_period < 7:
            return {
                'status': 'insufficient_data',
                'message': 'Need at least 7 days of data for reliable calculation',
                'actual_tdee': None
            }
        
        # Calculate actual TDEE from weight change
        # Weight loss is negative, weight gain is positive
        daily_deficit_or_surplus = (weight_change_kg * 7700) / days_period
        actual_tdee = daily_calories_consumed - daily_deficit_or_surplus
        
        # Calculate discrepancy
        difference = actual_tdee - current_tdee_estimate
        percent_difference = (difference / current_tdee_estimate) * 100
        
        # Check for metabolic adaptation
        adaptation_detected = False
        if abs(percent_difference) > 15:
            # Significant difference suggests metabolic adaptation or error
            if difference < 0 and weight_change_kg < 0:
                # Eating at deficit, burning less than predicted
                adaptation_detected = True
                adaptation_type = "Adaptive thermogenesis detected (metabolic slowdown)"
            elif difference > 0:
                adaptation_detected = True
                adaptation_type = "Higher than expected expenditure"
        
        return {
            'status': 'calculated',
            'actual_tdee': actual_tdee,
            'formula_estimate': current_tdee_estimate,
            'difference': difference,
            'percent_difference': percent_difference,
            'adaptation_detected': adaptation_detected,
            'adaptation_type': adaptation_type if adaptation_detected else None,
            'recommendation': self._get_recommendation(percent_difference, adaptation_detected)
        }
    
    def _get_recommendation(self, percent_diff: float, adaptation: bool) -> str:
        """Provide recommendation based on validation results"""
        if abs(percent_diff) < 5:
            return "Formula estimate is highly accurate. Use it with confidence."
        elif abs(percent_diff) < 10:
            return "Formula estimate is reasonably accurate. Monitor and adjust as needed."
        elif abs(percent_diff) < 15:
            return "Moderate difference detected. Use actual TDEE from weight data."
        else:
            if adaptation:
                return "Significant metabolic adaptation detected. Use actual TDEE and consider diet break or reverse dieting."
            else:
                return "Large discrepancy detected. Use actual TDEE from weight data. Verify data accuracy."


def get_user_input():
    """Interactive function to get user input"""
    print("=" * 70)
    print("COMPREHENSIVE TDEE CALCULATOR")
    print("Based on latest research for maximum accuracy")
    print("=" * 70)
    print()
    
    # Basic stats
    print("BASIC INFORMATION")
    print("-" * 70)
    weight_kg = float(input("Weight (kg): "))
    height_cm = float(input("Height (cm): "))
    age = int(input("Age (years): "))
    sex = input("Sex (male/female): ").lower()
    
    body_fat = input("Body fat percentage (leave empty if unknown): ").strip()
    body_fat_pct = float(body_fat) if body_fat else None
    
    print()
    
    # Diet info
    print("DIET INFORMATION")
    print("-" * 70)
    daily_calories = float(input("Daily calorie intake: "))
    daily_protein = float(input("Daily protein (grams): "))
    daily_carbs = float(input("Daily carbs (grams): "))
    daily_fat = float(input("Daily fat (grams): "))
    
    print()
    
    # Activity info
    print("ACTIVITY INFORMATION")
    print("-" * 70)
    daily_steps = int(input("Average daily steps: "))
    step_pace = input("Walking pace (slow/average/brisk/very_brisk) [default: average]: ").strip() or 'average'
    
    job_type = input("Job type (desk/light_active/moderate_active/very_active) [default: desk]: ").strip() or 'desk'
    sedentary_hours = float(input("Sedentary hours per day: "))
    
    print()
    
    # Workout info
    print("WORKOUT INFORMATION")
    print("-" * 70)
    workouts_per_week = int(input("Workouts per week: "))
    
    if workouts_per_week > 0:
        print("\nWorkout types: heavy_lifting, hiit, circuit_training, steady_cardio")
        workout_type = input("Primary workout type: ").strip() or 'heavy_lifting'
        workout_duration = float(input("Average workout duration (minutes): "))
        workout_intensity = input("Workout intensity (high/moderate) [default: high]: ").strip() or 'high'
    else:
        workout_type = 'heavy_lifting'
        workout_duration = 0
        workout_intensity = 'high'
    
    print()
    
    # Weight trend data (optional but recommended)
    print("WEIGHT TREND DATA (Optional but highly recommended for accuracy)")
    print("-" * 70)
    has_trend = input("Do you have weight trend data? (yes/no): ").lower()
    
    if has_trend == 'yes':
        weight_change = float(input("Weight change in kg (negative for loss, positive for gain): "))
        days_period = int(input("Number of days tracked: "))
    else:
        weight_change = None
        days_period = None
    
    return {
        'weight_kg': weight_kg,
        'height_cm': height_cm,
        'age': age,
        'sex': sex,
        'body_fat_pct': body_fat_pct,
        'daily_calories': daily_calories,
        'daily_protein_g': daily_protein,
        'daily_carbs_g': daily_carbs,
        'daily_fat_g': daily_fat,
        'daily_steps': daily_steps,
        'step_pace': step_pace,
        'job_type': job_type,
        'sedentary_hours': sedentary_hours,
        'workouts_per_week': workouts_per_week,
        'workout_type': workout_type,
        'workout_duration_min': workout_duration,
        'workout_intensity': workout_intensity,
        'weight_change': weight_change,
        'days_period': days_period
    }


def print_results(results: Dict, validation: Dict = None):
    """Print results in a clear, formatted way"""
    print("\n" + "=" * 70)
    print("TDEE CALCULATION RESULTS")
    print("=" * 70)
    print()
    
    print(f"ESTIMATED TDEE: {results['tdee']:.0f} calories/day")
    print()
    
    print("COMPONENT BREAKDOWN:")
    print("-" * 70)
    print(f"BMR (Basal Metabolic Rate):        {results['bmr']:.0f} cal  ({results['breakdown_pct']['bmr']:.1f}%)")
    print(f"  Method used: {results['bmr_method']}")
    if results['bmr_katch']:
        print(f"  Mifflin-St Jeor would give: {results['bmr_mifflin']:.0f} cal")
    
    print(f"\nTEF (Thermic Effect of Food):      {results['tef']:.0f} cal  ({results['breakdown_pct']['tef']:.1f}%)")
    if 'tef_data' in results and 'protein_tef' in results['tef_data']:
        print(f"  From protein: {results['tef_data']['protein_tef']:.0f} cal")
        print(f"  From carbs:   {results['tef_data']['carbs_tef']:.0f} cal")
        print(f"  From fat:     {results['tef_data']['fat_tef']:.0f} cal")
    
    neat_total = results['neat_from_steps'] + results['additional_neat']
    print(f"\nNEAT (Non-Exercise Activity):      {neat_total:.0f} cal  ({results['breakdown_pct']['neat']:.1f}%)")
    print(f"  From steps:      {results['neat_from_steps']:.0f} cal")
    print(f"  Other movement:  {results['additional_neat']:.0f} cal")
    
    print(f"\nEAT (Exercise Activity):           {results['eat_daily']:.0f} cal  ({results['breakdown_pct']['eat']:.1f}%)")
    
    print(f"EPOC (Post-Exercise Burn):         {results['epoc_daily']:.0f} cal  ({results['breakdown_pct']['epoc']:.1f}%)")
    
    print()
    print("=" * 70)
    
    if validation and validation['status'] == 'calculated':
        print()
        print("VALIDATION WITH REAL WEIGHT DATA")
        print("=" * 70)
        print(f"Formula Estimate:        {validation['formula_estimate']:.0f} cal/day")
        print(f"Actual TDEE (from data): {validation['actual_tdee']:.0f} cal/day")
        print(f"Difference:              {validation['difference']:+.0f} cal/day ({validation['percent_difference']:+.1f}%)")
        print()
        
        if validation['adaptation_detected']:
            print(f"⚠️  {validation['adaptation_type']}")
        
        print(f"RECOMMENDATION: {validation['recommendation']}")
        print()
        print("=" * 70)


def main():
    """Main function"""
    calc = TDEECalculator()
    
    # Get user input
    data = get_user_input()
    
    # Calculate TDEE using formulas
    results = calc.calculate_tdee_formula_based(
        weight_kg=data['weight_kg'],
        height_cm=data['height_cm'],
        age=data['age'],
        sex=data['sex'],
        body_fat_pct=data['body_fat_pct'],
        daily_steps=data['daily_steps'],
        step_pace=data['step_pace'],
        job_type=data['job_type'],
        sedentary_hours=data['sedentary_hours'],
        workouts_per_week=data['workouts_per_week'],
        workout_type=data['workout_type'],
        workout_duration_min=data['workout_duration_min'],
        workout_intensity=data['workout_intensity'],
        daily_protein_g=data['daily_protein_g'],
        daily_carbs_g=data['daily_carbs_g'],
        daily_fat_g=data['daily_fat_g'],
        daily_calories=data['daily_calories']
    )
    
    # Validate with weight trend if available
    validation = None
    if data['weight_change'] is not None and data['days_period'] is not None:
        validation = calc.validate_with_weight_trend(
            current_tdee_estimate=results['tdee'],
            daily_calories_consumed=data['daily_calories'],
            weight_change_kg=data['weight_change'],
            days_period=data['days_period']
        )
    
    # Print results
    print_results(results, validation)
    
    # Provide final recommendations
    print("\nKEY INSIGHTS:")
    print("-" * 70)
    
    if validation and validation['status'] == 'calculated':
        final_tdee = validation['actual_tdee']
        print(f"✓ Use the ACTUAL TDEE from your weight data: {final_tdee:.0f} cal/day")
    else:
        final_tdee = results['tdee']
        print(f"✓ Estimated TDEE: {final_tdee:.0f} cal/day")
        print("⚠️  Track your weight for 2+ weeks to validate this estimate")
    
    print(f"\nFor weight loss (1 lb/week):  {final_tdee - 500:.0f} cal/day")
    print(f"For maintenance:              {final_tdee:.0f} cal/day")
    print(f"For muscle gain (slow):       {final_tdee + 200:.0f} cal/day")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
