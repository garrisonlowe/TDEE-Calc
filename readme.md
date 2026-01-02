# 💪 Comprehensive TDEE Calculator - Imperial Edition

## Overview
Research-backed, highly accurate TDEE (Total Daily Energy Expenditure) calculator with a modern web interface. Built specifically for Americans who refuse to use the metric system. 🇺🇸

## 🚀 Quick Start

### Link to App! -> 

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

## Requirements

- Python 3.8+
- Streamlit
- All dependencies installed via pip

```bash
pip install streamlit --break-system-packages
```

## Files Included

- `tdee_app.py` - Main Streamlit application
- `tdee_calculator.py` - Core calculation logic
- `run_calculator.sh` - Launcher script
- `README.md` - This file

## Research Citations

- Mifflin MD et al. (1990) - A new predictive equation for REE
- Frankenfield D et al. (2005) - Comparison of predictive equations for RMR
- Johnstone AM et al. (2005) - Factors influencing BMR variation
- Trexler ET et al. (2014) - Metabolic adaptation to weight loss
- Bersheim E & Bahr R (2003) - Effect of exercise on EPOC
- Various EPOC studies (2014-2021)

## License

Free for personal use. Based on published scientific research.

---

**Made with 💪 for accurate nutrition tracking**

*"In God we trust, all others must bring data."* - W. Edwards Deming
