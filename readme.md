# 💪 Comprehensive TDEE Calculator - Imperial Edition

## Overview
Research-backed, highly accurate TDEE (Total Daily Energy Expenditure) calculator with a modern web interface. Built specifically for people who couldn't find a good enough TDEE calculator on the internet, like myself. 🇺🇸

## 🚀 Quick Start

### Link to App! -> https://tdee-calc.streamlit.app/

## Features

### Calculator Tab
- 🧮 **Dual BMR Calculation**: Compares Mifflin-St Jeor and Katch-McArdle formulas
- 🔥 **Macro-Specific TEF**: Accurate thermic effect based on your actual protein/carb/fat intake
- 🚶 **Detailed Activity Breakdown**: Separate inputs for walking, standing, light/moderate activity
- 🏋️ **Workout-Specific EPOC**: Different EPOC values for cardio, strength, HIIT, circuits
- ⚖️ **Weight Trend Validation** (GOLD STANDARD): Uses actual weight change over time to calculate true TDEE
- 📊 **Multiple Calorie Targets**: Fat loss (aggressive/moderate), maintenance, muscle gain (lean/standard)

### Daily Tracker Tab
- 📅 **Track daily metrics**: Weight, calories, protein/carbs/fat, steps, sleep, energy levels
- 📈 **Visual analytics**: 3 interactive charts showing your complete history
  - Weight progress over time
  - Daily step count
  - Sleep duration tracking
- 🔍 **Pan & scroll charts**: Navigate through your entire data history
- ☁️ **Cloud storage**: Data automatically synced to Google Sheets
- 👥 **Multi-user support**: Track multiple people separately (perfect for families!)
- 💾 **Data persistence**: Never lose your entries, accessible from any device

<!-- ### Option 1: Launch Script
```bash
chmod +x run_calculator.sh
./run_calculator.sh
```

### Option 2: Direct Command
```bash
streamlit run tdee_app.py
```

The app will automatically open in your browser at `http://localhost:8501` -->

## What Makes This Different

### 1. **Dual BMR Calculation**
- **Mifflin-St Jeor (1990)**: Most accurate for general population (82% accuracy)
- **Katch-McArdle**: Most accurate for lean individuals when body fat % is known
- Automatically uses the best formula based on your data

### 2. **Macro-Specific TEF (Thermic Effect of Food)**
Unlike calculators that use generic 10% for everyone:
- **Protein**: 25% thermic effect (burns 1 cal per 4 cal eaten)
- **Carbs**: 7.5% thermic effect
- **Fat**: 1.5% thermic effect

**Example**: 200g protein/day burns ~100 more calories than 100g protein/day!

### 3. **Detailed Activity Breakdown**
- Steps converted using MET values (not generic 0.04 cal/step)
- Job type matters (desk vs active)
- Sedentary time factored in
- Walking pace matters

### 4. **Workout-Specific EPOC**
Research-based afterburn calculations:
- **Heavy lifting** (80%+ 1RM with long rests): ~168 kcal over 14 hours
- **HIIT**: High during-exercise burn, similar EPOC
- **Circuit training**: Moderate benefits
- **Steady cardio**: Lower EPOC but still counted

### 5. **🏆 GOLD STANDARD: Weight Trend Validation**
The secret weapon. If you track your weight for 2+ weeks:

**Example**: Eating 2500 cal/day for 14 days, lost 2.2 lbs
- Daily deficit = (2.2 lbs × 3500 cal/lb) ÷ 14 days = 550 cal/day
- **Actual TDEE = 2500 + 550 = 3050 cal/day**

This bypasses ALL estimation and gives you YOUR exact metabolic rate. As accurate as lab testing.

## Features

### Modern UI
- Clean, organized tabs
- Real-time calculations
- Visual breakdown of components
- Color-coded metrics
- Responsive design

### Comprehensive Inputs
- **Basic Stats**: Weight (lbs), height (feet/inches), age, sex, body fat %
- **Diet**: Daily calories and macro breakdown
- **Activity**: Steps, walking pace, job type, sedentary hours
- **Workouts**: Type, frequency, duration, intensity
- **Weight Trend**: Optional but recommended for accuracy

### Detailed Results
- Total TDEE estimate
- Component breakdown (BMR, TEF, NEAT, EAT, EPOC)
- Percentage contribution of each component
- Weight trend validation (if data provided)
- Metabolic adaptation detection
- Calorie targets for fat loss, maintenance, and muscle gain

## Understanding Your Results

### TDEE Components
```
TDEE = BMR + TEF + NEAT + EAT + EPOC
```

- **BMR** (60-75%): Calories to keep you alive
- **TEF** (8-15%): Calories to digest food
- **NEAT** (15-30%): Daily movement, fidgeting, etc.
- **EAT** (5-15%): Actual exercise
- **EPOC** (1-5%): Post-workout elevated metabolism

### Validation Accuracy

**Formula estimate only:**
- ±10% accuracy for most people
- Better than generic online calculators

**With weight trend data (2+ weeks):**
- ±2-5% accuracy
- As accurate as metabolic chamber testing
- Detects metabolic adaptation

### Metabolic Adaptation

If your actual TDEE is significantly lower than predicted:
- **Adaptive thermogenesis** detected
- Common during prolonged deficits
- Solution: Diet break or reverse diet

## Calorie Targets

The app provides targets for:

### Fat Loss
- **Aggressive**: -750 cal/day (1.5 lbs/week)
- **Moderate**: -500 cal/day (1 lb/week)

### Maintenance
- **Maintain**: TDEE ± 100 cal/day

### Muscle Gain
- **Lean Bulk**: +200 cal/day (0.5 lbs/week)
- **Standard**: +350 cal/day (0.75 lbs/week)

## Pro Tips for Maximum Accuracy

1. **Track weight daily** for 14+ days at consistent intake
2. **Weigh at same time** - morning, after bathroom, before eating/drinking
3. **Use a weight trend app** - daily fluctuations are normal
4. **Be honest about activity** - 80% of people overestimate
5. **Track macros accurately** - TEF calculation depends on it
6. **Reassess every 10-15 lbs** - TDEE changes with weight
7. **Account for water weight**:
   - Sodium/carbs affect retention
   - Menstrual cycle (females): ±5 lbs fluctuation
   - New exercise routine: temporary water gain

## Key Research Findings

1. **Individual variation**: BMR varies ±10-15% even with identical stats (±300 kcal)
2. **Activity overestimation**: 80% of people select activity levels too high
3. **Protein matters**: High protein diets burn significantly more calories via TEF
4. **EPOC is real but modest**: Heavy lifting produces most, ~168 kcal over 14 hours
5. **Metabolic adaptation exists**: Body adapts to prolonged deficits

## Why Track Macros?

**Same calories, different TEF:**

Diet A (100g protein):
- 2500 calories
- ~10% TEF = 250 calories burned

Diet B (200g protein):
- 2500 calories  
- ~12% TEF = 300 calories burned

**50 extra calories burned per day = 5 lbs fat loss per year from diet alone!**

## Common Questions

### "Why is my TDEE different from calculator X?"
Most calculators:
- Use outdated formulas (Harris-Benedict from 1919)
- Don't factor in body composition
- Use generic TEF (10% for everyone)
- Oversimplify activity levels
- Don't validate with real data

### "Should I use formula estimate or actual TDEE?"
- **Formula only**: Use if no weight trend data available
- **Weight trend available**: ALWAYS use actual TDEE (gold standard)
- **Track for 14+ days** for reliable data

### "My TDEE seems too high/low"
- Individual variation is real (±300 kcal)
- Trust your weight trend data over formulas
- Metabolic adaptation can lower TDEE
- Track consistently and adjust

### "How often should I recalculate?"
- Every 10-15 lbs of weight change
- Every 8-12 weeks if maintaining
- When activity levels change significantly
- When encountering plateaus

## How The Calculator Works

### Why This Calculator is Different

Most TDEE calculators use overly simple activity multipliers. This one breaks down your energy expenditure into precise components based on peer-reviewed research.

### Components Explained

**BMR (Basal Metabolic Rate)**: Calories burned at complete rest  
**TEF (Thermic Effect of Food)**: Calories burned digesting food  
**NEAT (Non-Exercise Activity)**: Daily movement, fidgeting, walking  
**EAT (Exercise Activity)**: Calories during structured workouts  
**EPOC (Excess Post-Exercise Oxygen Consumption)**: "Afterburn" effect

### Sleep's Impact on Metabolism

Poor sleep drastically reduces both BMR and NEAT through:
- Reduced insulin sensitivity
- Hormonal dysregulation (leptin ↓18%, ghrelin ↑28%)
- Decreased spontaneous movement
- Metabolic "grogginess"

### Weight Trend Validation

The gold standard for TDEE accuracy is reverse-engineering from weight change data. Track for 14+ days and use the weight trend feature for ±2-5% accuracy!

## Technical Details

### BMR Formulas Used

**Mifflin-St Jeor:**
```
Men:   BMR = (4.536 × weight_lbs) + (15.875 × height_inches) - (5 × age) + 5
Women: BMR = (4.536 × weight_lbs) + (15.875 × height_inches) - (5 × age) - 161
```

**Katch-McArdle:**
```
BMR = 370 + (21.6 × lean_mass_kg)
Lean Mass = Weight × (1 - body_fat_decimal)
```

### MET Values

- Slow walk (2 mph): 2.8 METs
- Average walk (3 mph): 3.8 METs  
- Brisk walk (4 mph): 4.8 METs
- Very brisk (4.5 mph): 5.5 METs

### Weight Trend Math

```
Daily Energy Balance = (Weight_change_lbs × 3500) / Days
Actual TDEE = Daily_intake - Daily_energy_balance
```

Example:
- Eating: 2500 cal/day
- Lost: 2.2 lbs in 14 days
- Balance: (2.2 × 3500) / 14 = -550 cal/day
- TDEE: 2500 - (-550) = 3050 cal/day

## Data Persistence

The app uses **Google Sheets** for cloud-based data storage, ensuring your entries persist across sessions and devices.

### Features
- ☁️ **Cloud sync** - Data stored in your Google Drive
- 👨‍👩‍👧‍👦 **Multi-user support** - Separate tracking for multiple users
- 📊 **Automatic backup** - Never lose your data
- 📱 **Access anywhere** - Works on any device with the deployed link

### Setup

For deployment setup, see [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)

**Local fallback:** If Google Sheets isn't configured, the app automatically falls back to local JSON storage.

## Multi-User Support

Track multiple people without data mixing:

1. Select user from dropdown in Daily Tracker tab
2. Add new users with the "Add New User" expander
3. Each user gets their own:
   - Google Sheets worksheet
   - Local JSON file (if not using Sheets)
   - Complete data separation

Perfect for families or fitness coaching!

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- Google Sheets API (gspread, google-auth)

```bash
pip install -r requirements.txt
```

## Files Included

- `tdee_app.py` - Main Streamlit application
- `tdee_calculator.py` - Core calculation logic
- `daily_tracker.py` - Data persistence layer (Google Sheets + JSON)
- `requirements.txt` - Python dependencies
- `credentials.json` - Google Sheets API credentials (not in repo)
- `GOOGLE_SHEETS_SETUP.md` - Setup guide for cloud storage
- `run_calculator.sh` - Launcher script
- `README.md` - This file

## Research Citations

### Key Research Studies

- **Mifflin MD et al. (1990)** - A new predictive equation for REE / BMR equation development
- **Frankenfield D et al. (2005)** - Comparison of predictive equations for RMR / BMR equation comparison study
- **Johnstone AM et al. (2005)** - Factors influencing BMR variation / Metabolic variation factors
- **Trexler ET et al. (2014)** - Metabolic adaptation to weight loss / Metabolic adaptation in athletes
- **Sharma & Kavuru (2010)** - Sleep and metabolism overview
- **Spiegel et al. (2004)** - Sleep restriction effects on hormones
- **Schoenfeld et al. (2016)** - Rest intervals and hypertrophy
- **Bersheim E & Bahr R (2003)** - Effect of exercise on EPOC
- **Multiple 2014-2021 studies** - EPOC research

All formulas and adjustments are based on peer-reviewed research.

## License

Free for personal use. Based on published scientific research.

---

**Made with 💪 for accurate nutrition tracking**

*"In God we trust, all others must bring data."* - W. Edwards Deming
