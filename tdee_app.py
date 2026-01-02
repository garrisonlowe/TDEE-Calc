#!/usr/bin/env python3
"""
Comprehensive TDEE Calculator - Streamlit App
Imperial Units Edition (Freedom Units!)
"""

import streamlit as st
from typing import Dict, Optional

# Import the calculator logic
from tdee_calculator import TDEECalculator


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


def main():
    st.set_page_config(
        page_title="TDEE Calculator",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .big-font {
            font-size: 24px !important;
            font-weight: bold;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
        }
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("💪 Comprehensive TDEE Calculator")
    st.markdown("### Research-backed, highly accurate Total Daily Energy Expenditure calculator")
    st.markdown("---")
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["📊 Calculator", "📖 How It Works", "🔬 Methodology"])
    
    with tab1:
        # Sidebar for inputs
        with st.sidebar:
            st.header("Your Information")
            
            # Basic Information
            st.subheader("📋 Basic Stats")
            weight_lbs = st.number_input("Weight (lbs)", min_value=50.0, max_value=500.0, value=185.0, step=0.5)
            
            col1, col2 = st.columns(2)
            with col1:
                height_feet = st.number_input("Height (feet)", min_value=3, max_value=8, value=5, step=1)
            with col2:
                height_inches = st.number_input("Height (inches)", min_value=0.0, max_value=11.9, value=11.0, step=0.5)
            
            age = st.number_input("Age (years)", min_value=15, max_value=100, value=30, step=1)
            sex = st.selectbox("Sex", ["Male", "Female"])
            body_fat = st.number_input("Body Fat % (optional, leave 0 if unknown)", min_value=0.0, max_value=60.0, value=0.0, step=0.5)
            
            st.markdown("---")
            
            # Diet Information
            st.subheader("🍽️ Diet")
            daily_calories = st.number_input("Daily Calorie Intake", min_value=800, max_value=6000, value=2500, step=50)
            
            st.markdown("**Macros (grams per day)**")
            daily_protein = st.number_input("Protein (g)", min_value=0, max_value=500, value=200, step=5)
            daily_carbs = st.number_input("Carbs (g)", min_value=0, max_value=800, value=250, step=10)
            daily_fat = st.number_input("Fat (g)", min_value=0, max_value=300, value=80, step=5)
            
            st.markdown("---")
            
            # Activity Information
            st.subheader("🚶 Daily Activity")
            daily_steps = st.number_input("Average Daily Steps", min_value=0, max_value=50000, value=8000, step=500)
            step_pace = st.selectbox("Walking Pace", ["Slow", "Average", "Brisk", "Very Brisk"], index=1)
            
            job_type = st.selectbox("Job Type", 
                                   ["Desk Job", "Light Active", "Moderate Active", "Very Active"],
                                   index=0)
            sedentary_hours = st.slider("Sedentary Hours/Day", 0.0, 18.0, 9.0, 0.5)
            
            st.markdown("---")
            
            # Sleep Information
            st.subheader("😴 Sleep")
            sleep_hours = st.slider("Average Sleep (hours/night)", 3.0, 12.0, 7.5, 0.5,
                                   help="Optimal: 7-8 hours. <5 hrs significantly impacts metabolism")
            sleep_quality = st.select_slider("Sleep Quality", 
                                            options=["Poor", "Fair", "Good", "Excellent"],
                                            value="Good",
                                            help="Quality affects metabolic recovery")
            
            st.markdown("---")
            
            # Workout Information
            st.subheader("🏋️ Workouts")
            workouts_per_week = st.number_input("Workouts Per Week", min_value=0, max_value=14, value=4, step=1)
            
            if workouts_per_week > 0:
                workout_type = st.selectbox("Workout Type", 
                                           ["Heavy Lifting", "HIIT", "Circuit Training", "Steady Cardio"],
                                           index=0)
                workout_duration = st.number_input("Avg Workout Duration (minutes)", min_value=10, max_value=180, value=75, step=5)
                workout_intensity = st.selectbox("Intensity", ["High", "Moderate"], index=0)
            else:
                workout_type = "Heavy Lifting"
                workout_duration = 0
                workout_intensity = "High"
            
            st.markdown("---")
            
            # Weight Trend Data
            st.subheader("⚖️ Weight Trend (Optional)")
            st.markdown("*For maximum accuracy*")
            has_trend_data = st.checkbox("I have weight trend data")
            
            if has_trend_data:
                weight_change_lbs = st.number_input("Weight Change (lbs, negative = loss)", 
                                                   min_value=-50.0, max_value=50.0, value=-2.2, step=0.1,
                                                   help="Enter negative for weight loss, positive for gain")
                days_tracked = st.number_input("Days Tracked", min_value=7, max_value=365, value=14, step=1)
            else:
                weight_change_lbs = None
                days_tracked = None
            
            st.markdown("---")
            calculate_button = st.button("🔥 Calculate TDEE", type="primary", use_container_width=True)
        
        # Main content area
        if calculate_button:
            # Convert units
            weight_kg = lbs_to_kg(weight_lbs)
            height_cm = feet_inches_to_cm(height_feet, height_inches)
            body_fat_pct = body_fat if body_fat > 0 else None
            
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
                body_fat_pct=body_fat_pct,
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
            
            # Validate with weight trend if available
            validation = None
            if has_trend_data and weight_change_lbs is not None:
                weight_change_kg = lbs_to_kg(abs(weight_change_lbs)) * (-1 if weight_change_lbs < 0 else 1)
                validation = calc.validate_with_weight_trend(
                    current_tdee_estimate=results['tdee'],
                    daily_calories_consumed=daily_calories,
                    weight_change_kg=weight_change_kg,
                    days_period=days_tracked
                )
            
            # Display Results
            st.markdown("## 📊 Your Results")
            
            # Main TDEE Display
            if validation and validation['status'] == 'calculated':
                final_tdee = validation['actual_tdee']
                st.markdown(f"""
                    <div class="success-box">
                        <h2 style='text-align: center; color: #155724;'>Your TDEE: {final_tdee:.0f} calories/day</h2>
                        <p style='text-align: center;'><strong>This is your ACTUAL TDEE from weight data (most accurate)</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                final_tdee = results['tdee']
                st.markdown(f"""
                    <div class="metric-card">
                        <h2 style='text-align: center;'>Estimated TDEE: {final_tdee:.0f} calories/day</h2>
                        <p style='text-align: center;'><em>Add weight trend data for actual TDEE</em></p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Component Breakdown
            st.markdown("### 📈 Energy Expenditure Breakdown")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("BMR (Base Metabolism)", f"{results['bmr']:.0f} cal", 
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
            
            # Sleep Impact Display
            if 'sleep_adjustment' in results:
                sleep_adj = results['sleep_adjustment']
                if sleep_adj['bmr_multiplier'] < 1.0 or sleep_adj['neat_multiplier'] < 1.0:
                    bmr_impact = (1.0 - sleep_adj['bmr_multiplier']) * results['bmr_base']
                    neat_impact = (1.0 - sleep_adj['neat_multiplier']) * (results['neat_from_steps'] / sleep_adj['neat_multiplier'] + results['additional_neat'] / sleep_adj['neat_multiplier'])
                    total_sleep_impact = bmr_impact + neat_impact
                    
                    st.markdown(f"""
                        <div class="warning-box">
                            <strong>💤 Sleep Impact: -{total_sleep_impact:.0f} cal/day</strong><br>
                            {sleep_adj['metabolic_note']}<br>
                            <small>Sleeping {sleep_adj['sleep_hours']} hrs with {sleep_adj['sleep_quality']} quality</small>
                        </div>
                    """, unsafe_allow_html=True)
                elif sleep_adj['sleep_hours'] >= 7 and sleep_adj['sleep_hours'] <= 8:
                    st.markdown(f"""
                        <div class="success-box">
                            <strong>✅ Optimal Sleep</strong><br>
                            {sleep_adj['metabolic_note']}
                        </div>
                    """, unsafe_allow_html=True)
            
            col4, col5 = st.columns(2)
            
            with col4:
                st.metric("EAT (Exercise)", f"{results['eat_daily']:.0f} cal",
                         f"{results['breakdown_pct']['eat']:.1f}%")
            
            with col5:
                st.metric("EPOC (Afterburn)", f"{results['epoc_daily']:.0f} cal",
                         f"{results['breakdown_pct']['epoc']:.1f}%")
            
            # Validation Results
            if validation and validation['status'] == 'calculated':
                st.markdown("### ✅ Weight Trend Validation")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Formula Estimate", f"{validation['formula_estimate']:.0f} cal")
                with col2:
                    st.metric("Actual TDEE", f"{validation['actual_tdee']:.0f} cal")
                with col3:
                    diff_color = "normal" if abs(validation['percent_difference']) < 10 else "inverse"
                    st.metric("Difference", f"{validation['difference']:+.0f} cal", 
                             f"{validation['percent_difference']:+.1f}%",
                             delta_color=diff_color)
                
                if validation['adaptation_detected']:
                    st.markdown(f"""
                        <div class="warning-box">
                            <strong>⚠️ Metabolic Adaptation Detected</strong><br>
                            {validation['adaptation_type']}
                        </div>
                    """, unsafe_allow_html=True)
                
                st.info(f"**Recommendation:** {validation['recommendation']}")
            
            # Calorie Targets
            st.markdown("### 🎯 Calorie Targets")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Fat Loss**")
                st.markdown(f"🔥 Aggressive: **{final_tdee - 750:.0f}** cal/day")
                st.caption("1.5 lbs/week loss")
                st.markdown(f"🎯 Moderate: **{final_tdee - 500:.0f}** cal/day")
                st.caption("1 lb/week loss")
            
            with col2:
                st.markdown("**Maintenance**")
                st.markdown(f"⚖️ Maintain: **{final_tdee:.0f}** cal/day")
                st.caption("Stay at current weight")
            
            with col3:
                st.markdown("**Muscle Gain**")
                st.markdown(f"💪 Lean Bulk: **{final_tdee + 200:.0f}** cal/day")
                st.caption("0.5 lbs/week gain")
                st.markdown(f"🚀 Standard: **{final_tdee + 350:.0f}** cal/day")
                st.caption("0.75 lbs/week gain")
            
            # Pro Tips
            st.markdown("---")
            st.markdown("### 💡 Pro Tips")
            st.markdown("""
            - **Track weight daily** for 2+ weeks to validate this estimate
            - **Weigh yourself** at the same time each morning (after bathroom, before eating)
            - **Be honest** about activity - most people overestimate
            - **Reassess** every 10-15 lbs of weight change
            - **Water weight** can fluctuate ±5 lbs, focus on weekly trends
            """)
    
    with tab2:
        st.markdown("## 📖 How This Works")
        
        st.markdown("""
        ### What Makes This Different from Online Calculators?
        
        Most TDEE calculators use a simple formula and generic activity multipliers. This calculator:
        
        1. **Uses dual BMR formulas** - Mifflin-St Jeor for everyone, Katch-McArdle when you know body fat %
        2. **Calculates macro-specific TEF** - Your protein intake matters! High protein = more calories burned
        3. **Factors in detailed activity** - Steps, job type, sedentary time, workout style
        4. **Includes EPOC effects** - Heavy lifting has a longer afterburn than HIIT
        5. **Validates with real data** - Your weight trend is the GOLD STANDARD
        
        ### The Weight Trend Validation
        
        This is the game-changer. If you've been eating the same calories for 2+ weeks:
        
        ```
        If you eat 2500 cal/day for 14 days and lose 2.2 lbs:
        - Daily deficit = (2.2 lbs × 3500 cal/lb) / 14 days = 550 cal/day
        - Actual TDEE = 2500 + 550 = 3050 cal/day
        ```
        
        This bypasses all estimation and gives you YOUR exact metabolic rate.
        
        ### Why Track Macros?
        
        Different macros have different thermic effects:
        - **Protein**: 25% of calories burned in digestion
        - **Carbs**: 7.5% of calories burned
        - **Fat**: 1.5% of calories burned
        
        A diet with 200g protein burns ~100 more calories daily than one with 100g protein!
        
        ### Why Sleep Matters
        
        Sleep has MASSIVE metabolic effects that most calculators ignore:
        
        **Sleep Deprivation (<5 hours) Causes:**
        - 30%+ drop in insulin sensitivity (just 4 days!)
        - 18% decrease in leptin (satiety hormone)
        - 28% increase in ghrelin (hunger hormone)
        - Eating 385+ more calories per day
        - 3.7x obesity risk in men, 2.3x in women
        - Reduced BMR and NEAT (less fidgeting/movement)
        
        **Optimal Sleep (7-8 hours):**
        - Normal metabolic function
        - Proper hormone regulation
        - Adequate recovery from exercise
        - Optimal NEAT levels
        
        **Long Sleep (>9 hours):**
        - Associated with fatigue
        - Reduced daily activity
        - May indicate underlying issues
        
        This calculator adjusts your BMR and NEAT based on sleep quantity and quality.
        
        ### Individual Variation
        
        Even people with identical stats can have BMRs that differ by 10-15% (±300 calories).
        Factors include:
        - Genetics
        - Thyroid function
        - Previous dieting history
        - NEAT (fidgeting, posture, etc.)
        - Muscle mass
        
        This is why the weight trend validation is so important.
        """)
    
    with tab3:
        st.markdown("## 🔬 Research & Methodology")
        
        st.markdown("""
        ### BMR Formulas
        
        **Mifflin-St Jeor (1990)** - Used for general population
        - Men: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5
        - Women: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161
        - Accuracy: Within 10% for 82% of non-obese individuals
        
        **Katch-McArdle** - Used when body fat % is known
        - BMR = 370 + (21.6 × lean_body_mass_kg)
        - More accurate for lean individuals
        
        ### TEF Calculations
        
        Based on macro composition:
        - Protein TEF = protein_calories × 0.25
        - Carb TEF = carb_calories × 0.075
        - Fat TEF = fat_calories × 0.015
        
        ### Steps to Calories
        
        Uses MET (Metabolic Equivalent) values:
        - Slow walk (2 mph): 2.8 METs
        - Average walk (3 mph): 3.8 METs
        - Brisk walk (4 mph): 4.8 METs
        - Very brisk (4.5 mph): 5.5 METs
        
        Formula: Calories = MET × weight_kg × time_hours
        
        ### EPOC (Afterburn Effect)
        
        Research findings:
        - Heavy lifting (80%+ 1RM): ~168 kcal over 14 hours post-exercise
        - HIIT: Similar EPOC, higher during-exercise burn
        - Effects dissipate by 24 hours
        - This calculator uses conservative estimates based on peer-reviewed studies
        
        ### Sleep Impact on Metabolism
        
        **Research-Based Adjustments:**
        
        Sleep affects both BMR and NEAT based on peer-reviewed studies:
        
        - **<5 hours**: Severe restriction
          - BMR: -8% adjustment
          - NEAT: -20% adjustment
          - 3.7x obesity risk (men), 2.3x (women)
          - 30%+ drop in insulin sensitivity
        
        - **5-6 hours**: Moderate restriction
          - BMR: -5% adjustment
          - NEAT: -12% adjustment
          - Increased appetite, reduced activity
        
        - **6-7 hours**: Mild restriction
          - BMR: -3% adjustment
          - NEAT: -7% adjustment
          - Minor metabolic impact
        
        - **7-8 hours**: OPTIMAL
          - No adjustment
          - Optimal metabolic function
        
        - **>9 hours**: Long sleep
          - BMR: -2% adjustment
          - NEAT: -5% adjustment
          - Associated with fatigue
        
        **Sleep Quality** also matters:
        - Poor quality: Additional -3% penalty
        - Fair quality: Additional -1% penalty
        - Good/Excellent: No penalty
        
        ### Key Research Citations
        
        - Mifflin et al. (1990) - BMR equation development
        - Frankenfield et al. (2005) - BMR equation comparison study
        - Johnstone et al. (2005) - Metabolic variation factors
        - Trexler et al. (2014) - Metabolic adaptation in athletes
        - Bersheim & Bahr (2003) - EPOC review
        - Sharma & Kavuru (2010) - Sleep and metabolism overview
        - Spiegel et al. (2004) - Sleep restriction effects on leptin/ghrelin
        - Knutson et al. (2007) - Sleep duration and obesity risk
        - Nedeltcheva et al. (2010) - Sleep and diet-induced fat loss
        - Multiple 2014-2021 EPOC studies
        
        ### Accuracy Expectations
        
        **Formula-based estimate:** ±10% for most people
        
        **With weight trend validation:** ±2-5% (as accurate as lab testing)
        
        ### Individual Variation
        
        Research shows BMR can vary by ±10-15% even with identical stats.
        This is why tracking your actual results is crucial.
        """)


if __name__ == "__main__":
    main()
