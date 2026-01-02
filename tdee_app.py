#!/usr/bin/env python3
"""
Comprehensive TDEE Calculator & Daily Tracker
Imperial Units Edition with Persistence
"""

import streamlit as st
from typing import Dict, Optional
from datetime import datetime, timedelta
import json
import pandas as pd
import plotly.graph_objects as go

# Import the calculator logic and tracker
from tdee_calculator import TDEECalculator
from daily_tracker import DailyTracker


# Garrison's defaults
DEFAULTS = {
    'sex': 'Male',
    'height_ft': 5,
    'height_in': 11.0,  # Float for number_input compatibility
    'weight_lbs': 180.0,
    'age': 26,  # Estimated
    'body_fat_pct': 19.0,
    'daily_steps': 4500,
    'step_pace': 'Average',
    'job_type': 'Desk Job',
    'sedentary_hours': 10.0,
    'workouts_per_week': 3.0,
    'workout_duration': 77,
    'workout_type': 'Heavy Lifting',
    'workout_intensity': 'High',
    'daily_protein': 172,
    'daily_carbs': 196,
    'daily_fat': 41,
    'daily_calories': 1840,
    'sleep_hours': 9.0,
    'sleep_quality': 'Good'
}


def lbs_to_kg(lbs: float) -> float:
    """Convert pounds to kilograms"""
    return lbs * 0.453592


def kg_to_lbs(kg: float) -> float:
    """Convert kilograms to pounds"""
    return kg / 0.453592


def feet_inches_to_cm(feet: int, inches: float) -> float:
    """Convert feet and inches to centimeters"""
    total_inches = (feet * 12) + inches
    return total_inches * 2.54


def cm_to_feet_inches(cm: float) -> tuple:
    """Convert centimeters to feet and inches"""
    total_inches = cm / 2.54
    feet = int(total_inches // 12)
    inches = total_inches % 12
    return feet, inches


def render_tdee_calculator_tab():
    """Render the TDEE Calculator tab"""
    st.header("TDEE Calculator")
    st.markdown("Calculate your Total Daily Energy Expenditure based on multiple factors")
    
    # Sidebar for inputs
    with st.sidebar:
        st.title("Your Stats")
        
        # Basic Information
        st.subheader("👤 Basic Info")
        sex = st.selectbox("Sex", ["Male", "Female"], index=0 if DEFAULTS['sex'] == 'Male' else 1)
        age = st.number_input("Age", 15, 100, DEFAULTS['age'])
        
        col1, col2 = st.columns(2)
        with col1:
            height_ft = st.number_input("Height (ft)", 4, 7, DEFAULTS['height_ft'])
        with col2:
            height_in = st.number_input("Height (in)", 0.0, 11.9, DEFAULTS['height_in'], 0.1)
        
        weight = st.number_input("Weight (lbs)", 80.0, 500.0, DEFAULTS['weight_lbs'], 0.1)
        body_fat_pct = st.number_input("Body Fat % (optional)", 0.0, 60.0, DEFAULTS['body_fat_pct'], 0.1,
                                       help="More accurate TDEE if provided")
        
        st.markdown("---")
        
        # Diet Information
        st.subheader("🍽️ Diet")
        daily_calories = st.number_input("Daily Calories", 0, 10000, DEFAULTS['daily_calories'],
                                        help="Average daily intake")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            daily_protein = st.number_input("Protein (g)", 0, 500, DEFAULTS['daily_protein'])
        with col2:
            daily_carbs = st.number_input("Carbs (g)", 0, 1000, DEFAULTS['daily_carbs'])
        with col3:
            daily_fat = st.number_input("Fat (g)", 0, 300, DEFAULTS['daily_fat'])
        
        st.markdown("---")
        
        # Activity Information
        st.subheader("🚶 Daily Activity")
        daily_steps = st.number_input("Daily Steps", 0, 50000, DEFAULTS['daily_steps'], 100)
        step_pace = st.select_slider("Walking Pace", 
                                     options=["Slow", "Average", "Brisk", "Very Brisk"],
                                     value=DEFAULTS['step_pace'])
        job_type = st.select_slider("Job Activity Level",
                                    options=["Desk Job", "Light Active", "Moderate Active", "Very Active"],
                                    value=DEFAULTS['job_type'])
        sedentary_hours = st.slider("Hours Sitting/Day", 0.0, 24.0, DEFAULTS['sedentary_hours'], 0.5)
        
        st.markdown("---")
        
        # Sleep Information
        st.subheader("😴 Sleep")
        sleep_hours = st.slider("Average Sleep (hours/night)", 3.0, 12.0, DEFAULTS['sleep_hours'], 0.5,
                               help="Optimal: 7-8 hours. <5 hrs significantly impacts metabolism")
        sleep_quality = st.select_slider("Sleep Quality", 
                                        options=["Poor", "Fair", "Good", "Excellent"],
                                        value=DEFAULTS['sleep_quality'],
                                        help="Quality affects metabolic recovery")
        
        st.markdown("---")
        
        # Workout Information
        st.subheader("🏋️ Workouts")
        workouts_per_week = st.number_input("Workouts per Week", 0.0, 14.0, DEFAULTS['workouts_per_week'], 0.5)
        workout_duration = st.number_input("Avg Duration (minutes)", 0, 300, DEFAULTS['workout_duration'])
        workout_type = st.selectbox("Workout Type", 
                                   ["Heavy Lifting", "HIIT", "Circuit Training", "Steady Cardio"],
                                   index=0)
        workout_intensity = st.select_slider("Intensity", options=["Moderate", "High"],
                                            value=DEFAULTS['workout_intensity'])
        
        st.markdown("---")
        
        # Weight Trend Validation (optional)
        st.subheader("📊 Weight Trend Validation")
        use_weight_trend = st.checkbox("Use weight trend data", value=False,
                                       help="For most accurate TDEE calculation")
        
        if use_weight_trend:
            weight_change = st.number_input("Weight Change (lbs)", -50.0, 50.0, 0.0, 0.1,
                                          help="Negative for loss, positive for gain")
            days_tracked = st.number_input("Days Tracked", 7, 365, 14,
                                         help="Minimum 7 days, 14+ recommended")
    
    # Main content area - calculate and display (auto-calculates on any input change)
    # Convert imperial to metric
    weight_kg = lbs_to_kg(weight)
    height_cm = feet_inches_to_cm(height_ft, height_in)
    
    # Map selections to internal values
    pace_map = {"Slow": "slow", "Average": "average", "Brisk": "brisk", "Very Brisk": "very_brisk"}
    job_map = {"Desk Job": "desk", "Light Active": "light_active", 
              "Moderate Active": "moderate_active", "Very Active": "very_active"}
    workout_map = {"Heavy Lifting": "heavy_lifting", "HIIT": "hiit", 
                  "Circuit Training": "circuit_training", "Steady Cardio": "steady_cardio"}
    intensity_map = {"High": "high", "Moderate": "moderate"}
    quality_map = {"Poor": "poor", "Fair": "fair", "Good": "good", "Excellent": "excellent"}
    
    # Calculate TDEE
    calc = TDEECalculator()
    results = calc.calculate_tdee_formula_based(
        weight_kg=weight_kg,
        height_cm=height_cm,
        age=age,
        sex=sex.lower(),
        body_fat_pct=body_fat_pct if body_fat_pct > 0 else None,
        daily_steps=daily_steps,
        step_pace=pace_map[step_pace],
        job_type=job_map[job_type],
        sedentary_hours=sedentary_hours,
        workouts_per_week=workouts_per_week,
        workout_type=workout_map[workout_type],
        workout_duration_min=workout_duration,
        workout_intensity=intensity_map[workout_intensity],
        daily_protein_g=daily_protein,
        daily_carbs_g=daily_carbs,
        daily_fat_g=daily_fat,
        daily_calories=daily_calories,
        sleep_hours=sleep_hours,
        sleep_quality=quality_map[sleep_quality]
    )
    
    # Weight trend validation if provided
    if use_weight_trend:
        validation = calc.validate_with_weight_trend(
            daily_calories=daily_calories,
            weight_change_kg=lbs_to_kg(weight_change),
            days_tracked=days_tracked
        )
    else:
        validation = None
    
    # Display results
    st.markdown("---")
    
    # Main TDEE number
    tdee_to_display = validation['actual_tdee'] if validation else results['tdee']
    tdee_source = "FROM WEIGHT DATA ✅" if validation else "FROM FORMULA ESTIMATE"
    
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-size: 4em;">Your TDEE is <span style="color: white; text-decoration: none; font-size: 1.5em;">{tdee_to_display:,.0f}</span> calories per day.</h1>
            <p style="color: #e0e0e0; margin: 5px 0 0 0; font-size: 0.9em;">{tdee_source}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Component breakdown
    st.subheader("Energy Expenditure Breakdown")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("BMR (Baseline)", f"{results['bmr']:.0f} cal",
                 f"{results['breakdown_pct']['bmr']:.1f}%")
        st.caption(f"Method: {results['bmr_method']}")
    
    with col2:
        st.metric("TEF (Food Digestion)", f"{results['tef']:.0f} cal",
                 f"{results['breakdown_pct']['tef']:.1f}%")
        if 'tef_data' in results and 'protein_tef' in results['tef_data']:
            st.caption(f"Protein: {results['tef_data']['protein_tef']:.0f} cal")
    
    with col3:
        neat_total = results['neat_from_steps'] + results['additional_neat']
        st.metric("NEAT (Daily Movement)", f"{neat_total:.0f} cal",
                 f"{results['breakdown_pct']['neat']:.1f}%")
        st.caption(f"Steps: {results['neat_from_steps']:.0f} cal")
    
    with col4:
        st.metric("EAT (Exercise)", f"{results['eat_daily']:.0f} cal/day",
                 f"{results['breakdown_pct']['eat']:.1f}%")
    
    with col5:
        st.metric("EPOC (Afterburn)", f"{results['epoc_daily']:.0f} cal/day",
                 f"{results['breakdown_pct']['epoc']:.1f}%")
    
    # Sleep Impact Display
    if 'sleep_adjustment' in results:
        sleep_adj = results['sleep_adjustment']
        if sleep_adj['bmr_multiplier'] < 1.0 or sleep_adj['neat_multiplier'] < 1.0:
            bmr_impact = (1.0 - sleep_adj['bmr_multiplier']) * results['bmr_base']
            neat_impact = (1.0 - sleep_adj['neat_multiplier']) * (results['neat_from_steps'] / sleep_adj['neat_multiplier'] + results['additional_neat'] / sleep_adj['neat_multiplier'])
            total_sleep_impact = bmr_impact + neat_impact
            
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #E84625 0%, #FF6B4A 100%); padding: 15px; border-left: 5px solid #C4371F; border-radius: 5px; margin: 20px 0; color: white;">
                    <strong>💤 Sleep Impact: -{total_sleep_impact:.0f} cal/day</strong><br>
                    {sleep_adj['metabolic_note']}<br>
                    <small>Sleeping {sleep_adj['sleep_hours']} hrs with {sleep_adj['sleep_quality']} quality</small>
                </div>
            """, unsafe_allow_html=True)
        elif sleep_adj['sleep_hours'] >= 7 and sleep_adj['sleep_hours'] <= 8:
            st.markdown(f"""
                <div style="background-color: #d4edda; padding: 15px; border-left: 5px solid #28a745; border-radius: 5px; margin: 20px 0;">
                    <strong>✅ Optimal Sleep</strong><br>
                    {sleep_adj['metabolic_note']}
                </div>
            """, unsafe_allow_html=True)
    
    # Weight trend validation results
    if validation:
        st.markdown("---")
        st.subheader("📊 Weight Trend Validation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Formula TDEE", f"{results['tdee']:.0f} cal")
        
        with col2:
            st.metric("Actual TDEE", f"{validation['actual_tdee']:.0f} cal",
                     help="Reverse-engineered from weight change")
        
        with col3:
            diff_pct = ((validation['actual_tdee'] - results['tdee']) / results['tdee']) * 100
            st.metric("Difference", f"{validation['actual_tdee'] - results['tdee']:+.0f} cal",
                     f"{diff_pct:+.1f}%")
        
        if validation['metabolic_adaptation_detected']:
            st.warning(f"⚠️ **Metabolic Adaptation Detected** - Your actual TDEE is {abs(diff_pct):.1f}% {('lower' if diff_pct < 0 else 'higher')} than predicted. This suggests metabolic adaptation from prolonged dieting/surplus.")
        else:
            st.success("✅ Formula matches your actual results well!")
    
    # Calorie targets
    st.markdown("---")
    st.subheader("🎯 Calorie Targets")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Aggressive Cut", f"{tdee_to_display - 750:.0f} cal",
                 "-750 cal/day",
                 help="~1.5 lbs/week loss")
    
    with col2:
        st.metric("Moderate Cut", f"{tdee_to_display - 500:.0f} cal",
                 "-500 cal/day",
                 help="~1 lb/week loss")
    
    with col3:
        st.metric("Lean Bulk", f"{tdee_to_display + 250:.0f} cal",
                 "+250 cal/day",
                 help="~0.5 lb/week gain")
    
    with col4:
        st.metric("Standard Bulk", f"{tdee_to_display + 500:.0f} cal",
                 "+500 cal/day",
                 help="~1 lb/week gain")


def render_daily_tracker_tab(selected_user: str):
    """Render the Daily Tracker tab"""
    st.header("📝 Daily Tracker")
    st.markdown("Track your daily metrics and see weekly averages")
    
    # Initialize tracker with selected user
    tracker = DailyTracker(user=selected_user)
    
    # Initialize session state for entry date if not exists
    if 'entry_date' not in st.session_state:
        st.session_state.entry_date = datetime.now().date()
    
    # Date selector
    col_date1, col_date2 = st.columns([1, 2])
    with col_date1:
        entry_date = st.date_input("Entry Date", st.session_state.entry_date)
    
    # Date buttons directly below
    col_btn1, col_btn2, col_btn3 = st.columns([0.35, 0.35, 3.3])
    with col_btn1:
        if st.button("Yesterday", type="secondary"):
            st.session_state.entry_date = (datetime.now() - timedelta(days=1)).date()
            st.rerun()
    with col_btn2:
        if st.button("Today", type="primary"):
            st.session_state.entry_date = datetime.now().date()
            st.rerun()
    
    date_str = entry_date.strftime('%Y-%m-%d')
    
    # Get previous entry for reference
    prev_entry, prev_date = tracker.get_previous_entry(date_str)
    
    # Display previous entry if exists
    if prev_entry and prev_date:
        with st.expander(f"📅 Previous Entry ({prev_date})", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Weight", f"{prev_entry.get('weight', 'N/A')} lbs")
                st.metric("Calories", f"{prev_entry.get('calories', 'N/A')} cal")
            with col2:
                st.metric("Protein", f"{prev_entry.get('protein', 'N/A')}g")
                st.metric("Carbs", f"{prev_entry.get('carbs', 'N/A')}g")
            with col3:
                st.metric("Fat", f"{prev_entry.get('fat', 'N/A')}g")
                st.metric("Steps", f"{prev_entry.get('steps', 'N/A')}")
            with col4:
                st.metric("Sleep", f"{prev_entry.get('sleep_hours', 'N/A')} hrs")
                st.metric("Workout", "✅ Yes" if prev_entry.get('workout_done') else "❌ No")
    
    # Load existing entry for this date if it exists
    existing_entry = tracker.get_entry(date_str)
    
    st.markdown("---")
    
    # Input form with defaults
    st.subheader("Today's Metrics")
    
    # Weight & Intake Section (Horizontal)
    st.markdown("**⚖️ Weight & Intake**")
    col_w1, col_w2, col_w3, col_w4, col_w5 = st.columns(5)
    with col_w1:
        weight = st.number_input("Morning Weight (lbs)", 100.0, 500.0,
                                existing_entry.get('weight', DEFAULTS['weight_lbs']) if existing_entry else DEFAULTS['weight_lbs'],
                                0.1, key="weight_input")
    with col_w2:
        calories = st.number_input("Total Calories", 0, 10000,
                                  existing_entry.get('calories', DEFAULTS['daily_calories']) if existing_entry else DEFAULTS['daily_calories'],
                                  key="cal_input")
    with col_w3:
        protein = st.number_input("Protein (g)", 0, 500,
                                 existing_entry.get('protein', DEFAULTS['daily_protein']) if existing_entry else DEFAULTS['daily_protein'],
                                 key="protein_input")
    with col_w4:
        carbs = st.number_input("Carbs (g)", 0, 1000,
                               existing_entry.get('carbs', DEFAULTS['daily_carbs']) if existing_entry else DEFAULTS['daily_carbs'],
                               key="carbs_input")
    with col_w5:
        fat = st.number_input("Fat (g)", 0, 300,
                             existing_entry.get('fat', DEFAULTS['daily_fat']) if existing_entry else DEFAULTS['daily_fat'],
                             key="fat_input")
    
    st.markdown("---")
    
    # Activity & Sleep Section (Horizontal)
    st.markdown("**🚶 Activity & Sleep**")
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    with col_a1:
        steps = st.number_input("Steps", 0, 50000,
                               existing_entry.get('steps', DEFAULTS['daily_steps']) if existing_entry else DEFAULTS['daily_steps'],
                               100, key="steps_input")
    with col_a2:
        sleep_hours = st.number_input("Sleep (hours)", 0.0, 24.0,
                                     existing_entry.get('sleep_hours', DEFAULTS['sleep_hours']) if existing_entry else DEFAULTS['sleep_hours'],
                                     0.5, key="sleep_input")
    with col_a3:
        sleep_quality = st.select_slider("Sleep Quality",
                                        options=["Poor", "Fair", "Good", "Excellent"],
                                        value=existing_entry.get('sleep_quality', DEFAULTS['sleep_quality']) if existing_entry else DEFAULTS['sleep_quality'],
                                        key="sleep_quality_input")
    with col_a4:
        water_intake = st.number_input("Water (oz)", 0, 300,
                                      existing_entry.get('water_oz', 80) if existing_entry else 80,
                                      key="water_input")
    
    st.markdown("---")
    
    # Workout Section (Horizontal)
    st.markdown("**🏋️ Workout**")
    col_workout1, col_workout2 = st.columns([1, 3])
    with col_workout1:
        workout_done = st.checkbox("Workout Completed",
                                  value=existing_entry.get('workout_done', False) if existing_entry else False,
                                  key="workout_check")
    
    if workout_done:
        col_w1, col_w2, col_w3, col_w4, col_w5 = st.columns(5)
        with col_w1:
            workout_type = st.selectbox("Workout Type",
                                       ["Heavy Lifting", "HIIT", "Circuit Training", "Steady Cardio", "Other"],
                                       index=0 if not existing_entry else ["Heavy Lifting", "HIIT", "Circuit Training", "Steady Cardio", "Other"].index(existing_entry.get('workout_type', 'Heavy Lifting')),
                                       key="workout_type_input")
        with col_w2:
            workout_duration = st.number_input("Duration (min)", 0, 300,
                                             existing_entry.get('workout_duration', DEFAULTS['workout_duration']) if existing_entry else DEFAULTS['workout_duration'],
                                             key="workout_duration_input")
        with col_w3:
            rest_time = st.select_slider("Rest Between Sets",
                                        options=["Short (<60s)", "Moderate (60-90s)", "Long (2-3min)", "Very Long (3-5min)"],
                                        value=existing_entry.get('rest_time', "Long (2-3min)") if existing_entry else "Long (2-3min)",
                                        key="rest_time_input")
        with col_w4:
            training_style = st.selectbox("Training Style",
                                         ["Low Volume High Intensity", "High Volume Moderate Intensity", "Moderate Volume Moderate Intensity"],
                                         index=0 if not existing_entry else ["Low Volume High Intensity", "High Volume Moderate Intensity", "Moderate Volume Moderate Intensity"].index(existing_entry.get('training_style', 'Low Volume High Intensity')),
                                         key="training_style_input")
        with col_w5:
            energy_level = st.select_slider("Energy Level",
                                           options=["Very Low", "Low", "Moderate", "High", "Very High"],
                                           value=existing_entry.get('energy_level', "Moderate") if existing_entry else "Moderate",
                                           key="energy_input")
    else:
        workout_type = None
        workout_duration = 0
        rest_time = None
        training_style = None
        energy_level = st.select_slider("Energy Level",
                                       options=["Very Low", "Low", "Moderate", "High", "Very High"],
                                       value=existing_entry.get('energy_level', "Moderate") if existing_entry else "Moderate",
                                       key="energy_input")
    
    # Notes
    notes = st.text_area("Notes", 
                        value=existing_entry.get('notes', '') if existing_entry else '',
                        placeholder="How did you feel today? Any observations?",
                        key="notes_input")
    
    # Save button
    if st.button("💾 Save Entry", type="primary"):
        entry_data = {
            'weight': weight,
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fat': fat,
            'steps': steps,
            'sleep_hours': sleep_hours,
            'sleep_quality': sleep_quality,
            'water_oz': water_intake,
            'workout_done': workout_done,
            'workout_type': workout_type,
            'workout_duration': workout_duration,
            'rest_time': rest_time,
            'training_style': training_style,
            'energy_level': energy_level,
            'notes': notes
        }
        
        tracker.add_entry(date_str, entry_data)
        st.success(f"✅ Entry saved for {date_str}!")
        st.rerun()
    
    # Weekly Averages
    st.markdown("---")
    st.subheader("📊 Weekly Averages (Last 7 Days)")
    
    weekly_avg = tracker.calculate_weekly_averages(date_str)
    
    if weekly_avg and weekly_avg['days_tracked'] > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if weekly_avg['avg_weight']:
                st.metric("Avg Weight", f"{weekly_avg['avg_weight']:.1f} lbs",
                         f"{weekly_avg['weight_change']:.1f} lbs" if weekly_avg['weight_change'] else None)
        
        with col2:
            if weekly_avg['avg_steps']:
                st.metric("Avg Steps", f"{weekly_avg['avg_steps']:.0f}")
        
        with col3:
            if weekly_avg['avg_sleep']:
                st.metric("Avg Sleep", f"{weekly_avg['avg_sleep']:.1f} hrs")
        
        with col4:
            st.metric("Workouts", f"{weekly_avg['total_workouts']}/{weekly_avg['days_tracked']}")
        
        # Charts Section
        st.markdown("---")
        st.subheader("📈 Progress Trends (All Time)")
        
        # Get all entries
        all_entries = tracker.get_all_entries()
        
        if len(all_entries) > 1:
            # Create DataFrame for charting
            df = pd.DataFrame(all_entries)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Create tabs for different charts
            chart_tab1, chart_tab2, chart_tab3 = st.tabs([
                "⚖️ Weight", "🚶 Steps", "😴 Sleep"
            ])
            
            with chart_tab1:
                if 'weight' in df.columns and df['weight'].notna().any():
                    weight_data = df[['date', 'weight']].dropna()
                    
                    # Format dates as strings (MMM-DD format)
                    weight_data['date_str'] = weight_data['date'].dt.strftime('%b-%d')
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=weight_data['date_str'],
                        y=weight_data['weight'],
                        mode='lines+markers',
                        marker=dict(size=8),
                        line=dict(width=2)
                    ))
                    
                    fig.update_layout(
                        xaxis_title='Date',
                        yaxis_title='Weight (lbs)',
                        height=400,
                        hovermode='x unified',
                        dragmode='pan',
                        xaxis=dict(fixedrange=True, type='category'),
                        yaxis=dict(fixedrange=True)
                    )
                    
                    config = {
                        'scrollZoom': False,
                        'displayModeBar': True,
                        'modeBarButtonsToRemove': ['zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'lasso2d', 'select2d']
                    }
                    
                    st.plotly_chart(fig, use_container_width=True, config=config)
                    st.caption(f"Weight trend over {len(weight_data)} days tracked")
                else:
                    st.info("No weight data available for charting")
            
            with chart_tab2:
                if 'steps' in df.columns and df['steps'].notna().any():
                    steps_data = df[['date', 'steps']].dropna()
                    
                    # Format dates as strings (MMM-DD format)
                    steps_data['date_str'] = steps_data['date'].dt.strftime('%b-%d')
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=steps_data['date_str'],
                        y=steps_data['steps'],
                        mode='lines+markers',
                        marker=dict(size=8, color='green'),
                        line=dict(width=2, color='green')
                    ))
                    
                    fig.update_layout(
                        xaxis_title='Date',
                        yaxis_title='Steps',
                        height=400,
                        hovermode='x unified',
                        dragmode='pan',
                        xaxis=dict(fixedrange=True, type='category'),
                        yaxis=dict(fixedrange=True)
                    )
                    
                    config = {
                        'scrollZoom': False,
                        'displayModeBar': True,
                        'modeBarButtonsToRemove': ['zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'lasso2d', 'select2d']
                    }
                    
                    st.plotly_chart(fig, use_container_width=True, config=config)
                    st.caption(f"Daily step count over {len(steps_data)} days tracked")
                else:
                    st.info("No step data available for charting")
            
            with chart_tab3:
                if 'sleep_hours' in df.columns and df['sleep_hours'].notna().any():
                    sleep_data = df[['date', 'sleep_hours']].dropna()
                    
                    # Format dates as strings (MMM-DD format)
                    sleep_data['date_str'] = sleep_data['date'].dt.strftime('%b-%d')
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=sleep_data['date_str'],
                        y=sleep_data['sleep_hours'],
                        mode='lines+markers',
                        marker=dict(size=8, color='purple'),
                        line=dict(width=2, color='purple')
                    ))
                    
                    fig.update_layout(
                        xaxis_title='Date',
                        yaxis_title='Sleep Hours',
                        height=400,
                        hovermode='x unified',
                        dragmode='pan',
                        xaxis=dict(fixedrange=True, type='category'),
                        yaxis=dict(fixedrange=True)
                    )
                    
                    config = {
                        'scrollZoom': False,
                        'displayModeBar': True,
                        'modeBarButtonsToRemove': ['zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'lasso2d', 'select2d']
                    }
                    
                    st.plotly_chart(fig, use_container_width=True, config=config)
                    st.caption(f"Sleep hours over {len(sleep_data)} days tracked")
                    
                    # Add optimal sleep reference line info
                    avg_sleep = sleep_data['sleep_hours'].mean()
                    if avg_sleep < 7:
                        st.warning(f"⚠️ Average sleep ({avg_sleep:.1f} hrs) is below optimal (7-8 hrs)")
                    elif avg_sleep > 9:
                        st.info(f"ℹ️ Average sleep ({avg_sleep:.1f} hrs) is above optimal (7-8 hrs)")
                    else:
                        st.success(f"✅ Average sleep ({avg_sleep:.1f} hrs) is in optimal range")
                else:
                    st.info("No sleep data available for charting")
            
            # Add expandable section to view/edit all entries
            st.markdown("---")
            with st.expander("📋 View & Edit All Entries", expanded=False):
                st.info(f"Showing entries for: **{selected_user}**")
                all_entries = tracker.get_all_entries()
                if all_entries:
                    # Create a DataFrame for display
                    display_df = pd.DataFrame(all_entries)
                    
                    # Reorder columns for better readability
                    column_order = ['date', 'weight', 'calories', 'protein', 'carbs', 'fat', 
                                  'steps', 'sleep_hours', 'sleep_quality', 'energy_level', 
                                  'workout_done', 'workout_type', 'workout_duration']
                    
                    # Keep only columns that exist
                    column_order = [col for col in column_order if col in display_df.columns]
                    display_df = display_df[column_order]
                    
                    # Sort by date descending (most recent first)
                    display_df = display_df.sort_values('date', ascending=False)
                    
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    st.markdown("---")
                    st.markdown("**Edit an Entry:**")
                    
                    # Select date to edit
                    dates_list = sorted([entry['date'] for entry in all_entries], reverse=True)
                    selected_edit_date = st.selectbox(
                        "Select date to edit:",
                        dates_list,
                        key="edit_date_selector"
                    )
                    
                    if selected_edit_date:
                        edit_entry = tracker.get_entry(selected_edit_date)
                        
                        if edit_entry:
                            st.info(f"Editing entry for {selected_edit_date}")
                            
                            # Create edit form
                            edit_col1, edit_col2, edit_col3 = st.columns(3)
                            
                            with edit_col1:
                                edit_weight = st.number_input("Weight (lbs)", 0.0, 500.0, 
                                                            float(edit_entry.get('weight', 180)), 0.1, key="edit_weight")
                                edit_calories = st.number_input("Calories", 0, 10000, 
                                                              int(edit_entry.get('calories', 2000)), 10, key="edit_calories")
                                edit_protein = st.number_input("Protein (g)", 0, 500, 
                                                             int(edit_entry.get('protein', 150)), 1, key="edit_protein")
                            
                            with edit_col2:
                                edit_carbs = st.number_input("Carbs (g)", 0, 1000, 
                                                           int(edit_entry.get('carbs', 200)), 1, key="edit_carbs")
                                edit_fat = st.number_input("Fat (g)", 0, 300, 
                                                         int(edit_entry.get('fat', 60)), 1, key="edit_fat")
                                edit_steps = st.number_input("Steps", 0, 50000, 
                                                           int(edit_entry.get('steps', 5000)), 100, key="edit_steps")
                            
                            with edit_col3:
                                edit_sleep = st.number_input("Sleep (hours)", 0.0, 24.0, 
                                                           float(edit_entry.get('sleep_hours', 7.5)), 0.5, key="edit_sleep")
                                edit_energy = st.select_slider("Energy Level",
                                                             options=["Very Low", "Low", "Moderate", "High", "Very High"],
                                                             value=edit_entry.get('energy_level', 'Moderate'),
                                                             key="edit_energy")
                            
                            # Update and Delete buttons
                            btn_col1, btn_col2, btn_col3 = st.columns([1, 1.5, 1])
                            with btn_col1:
                                if st.button("💾 Update Entry", type="primary", key="update_entry_btn"):
                                    updated_data = {
                                        'weight': edit_weight,
                                        'calories': edit_calories,
                                        'protein': edit_protein,
                                        'carbs': edit_carbs,
                                        'fat': edit_fat,
                                        'steps': edit_steps,
                                        'sleep_hours': edit_sleep,
                                        'sleep_quality': edit_entry.get('sleep_quality', 'Good'),
                                        'water_oz': edit_entry.get('water_oz', 80),
                                        'workout_done': edit_entry.get('workout_done', False),
                                        'workout_type': edit_entry.get('workout_type'),
                                        'workout_duration': edit_entry.get('workout_duration', 0),
                                        'rest_time': edit_entry.get('rest_time'),
                                        'training_style': edit_entry.get('training_style'),
                                        'energy_level': edit_energy,
                                        'notes': edit_entry.get('notes', '')
                                    }
                                    
                                    tracker.add_entry(selected_edit_date, updated_data)
                                    st.success(f"✅ Entry updated for {selected_edit_date}!")
                                    st.rerun()
                            
                            with btn_col3:
                                # Right-align the delete button within this column
                                _, right_align = st.columns([2, 1])
                                with right_align:
                                    if st.button("🗑️ Delete Entry", type="secondary", key="delete_entry_btn"):
                                        if tracker.delete_entry(selected_edit_date):
                                            st.success(f"✅ Entry deleted for {selected_edit_date}!")
                                            st.rerun()
                                        else:
                                            st.error(f"❌ Failed to delete entry for {selected_edit_date}")
                else:
                    st.info("No entries to display yet. Start tracking!")
        else:
            st.info("📊 Need at least 2 days of data to show trend charts")
    else:
        st.info("👉 No data yet for this week. Start tracking to see weekly averages!")


def main():
    st.set_page_config(
        page_title="TDEE & Daily Tracker",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Get list of users from session state or default
    if 'users' not in st.session_state:
        st.session_state.users = ["Garrison", "Gary"]
    
    # Header with user selector on the same row
    col_title, col_spacer, col_user = st.columns([3, 1, 1])
    
    with col_title:
        st.title("💪 TDEE Calculator & Daily Tracker")
        st.markdown("Your personalized fitness companion!")
    
    with col_user:
        selected_user = st.selectbox(
            "👤 Select User",
            st.session_state.users,
            key="user_selector"
        )
        with st.expander("➕ Add User"):
            new_user = st.text_input("New username", key="new_user_input")
            if st.button("Add", key="add_user_btn"):
                if new_user and new_user not in st.session_state.users:
                    st.session_state.users.append(new_user)
                    st.success(f"Added {new_user}!")
                    st.rerun()
    
    st.markdown("---")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 TDEE Calculator", "📝 Daily Tracker", "📖 Read Me!", "⚡ Quick Reference", "🔖 Version"])
    
    with tab1:
        render_tdee_calculator_tab()
    
    with tab2:
        render_daily_tracker_tab(selected_user)
    
    with tab3:
        # Display the README content
        try:
            with open('readme.md', 'r', encoding='utf-8') as f:
                readme_content = f.read()
            st.markdown(readme_content, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("README.md file not found!")
        except Exception as e:
            st.error(f"Error loading README: {str(e)}")
    
    with tab4:
        # Display the Quick Reference Guide
        try:
            with open('QUICK_REFERENCE.md', 'r', encoding='utf-8') as f:
                quick_ref_content = f.read()
            st.markdown(quick_ref_content, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("QUICK_REFERENCE.md file not found!")
        except Exception as e:
            st.error(f"Error loading Quick Reference: {str(e)}")
    
    with tab5:
        # Display the Version history
        try:
            with open('VERSION.md', 'r', encoding='utf-8') as f:
                version_content = f.read()
            st.markdown(version_content, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("VERSION.md file not found!")
        except Exception as e:
            st.error(f"Error loading Version history: {str(e)}")


if __name__ == "__main__":
    main()
