# 🆕 UPDATE: Sleep Tracking Added!

## What's New

The TDEE calculator now includes **sleep pattern/hours tracking** based on the latest metabolic research!

### New Inputs in the Calculator

**😴 Sleep Section** (in sidebar):
- **Average Sleep Hours** (3-12 hrs, slider)
  - Optimal: 7-8 hours
  - Warning if <5 hours
- **Sleep Quality** (Poor/Fair/Good/Excellent)
  - Affects metabolic recovery

### How Sleep Affects Your TDEE

Sleep impacts your metabolism in TWO major ways:

#### 1. BMR (Basal Metabolic Rate)
- Sleep deprivation reduces your baseline metabolism
- **Severe (<5 hrs)**: -8% BMR
- **Moderate (5-6 hrs)**: -5% BMR  
- **Mild (6-7 hrs)**: -3% BMR
- **Optimal (7-8 hrs)**: No penalty
- **Long (>9 hrs)**: -2% BMR

#### 2. NEAT (Non-Exercise Activity)
- Sleep deprivation = less fidgeting, less movement
- **Severe (<5 hrs)**: -20% NEAT
- **Moderate (5-6 hrs)**: -12% NEAT
- **Mild (6-7 hrs)**: -7% NEAT
- **Optimal (7-8 hrs)**: No penalty
- **Long (>9 hrs)**: -5% NEAT

### Real-World Impact

**Example: 30yo male, 185 lbs, desk job, lifts 4x/week**

| Sleep Amount | TDEE | vs Optimal |
|-------------|------|------------|
| 4.5 hrs (poor quality) | 2,679 cal | **-279 cal (-9.4%)** |
| 5.5 hrs (fair quality) | 2,802 cal | -156 cal (-5.3%) |
| 6.5 hrs (good quality) | 2,877 cal | -80 cal (-2.7%) |
| **7.5 hrs (good quality)** | **2,957 cal** | **Baseline** |
| 9.5 hrs (good quality) | 2,903 cal | -54 cal (-1.8%) |

**Getting only 4.5 hours of poor sleep vs 7.5 hours = burning 279 fewer calories per day!**

That's equivalent to:
- Skipping a 30-minute workout
- Or needing to eat 279 fewer calories to maintain the same deficit
- Over a year: Could be 29 lbs difference!

### The Research Behind It

Based on peer-reviewed studies showing:

- **<5 hrs/night**: 3.7x obesity risk (men), 2.3x (women)
- **4 days of poor sleep**: 30%+ drop in insulin sensitivity
- **Sleep deprivation**: eat 385 more calories/day
- **Hormones affected**:
  - Leptin (satiety) ↓18%
  - Ghrelin (hunger) ↑28%
- **Recovery**: BMR returns to normal with adequate sleep

### Citations Added

- Sharma & Kavuru (2010) - Sleep and metabolism overview
- Spiegel et al. (2004) - Sleep restriction effects on hormones
- Knutson et al. (2007) - Sleep duration and obesity risk  
- Nedeltcheva et al. (2010) - Sleep and diet-induced fat loss

## What You'll See in the App

### Sleep Impact Warning

If you're not getting optimal sleep, you'll see:

```
💤 Sleep Impact: -279 cal/day
Severe sleep restriction - major metabolic consequences
Sleeping 4.5 hrs with poor quality
```

### Optimal Sleep Confirmation

If you're in the sweet spot:

```
✅ Optimal Sleep
Optimal sleep duration for metabolism
```

### Updated Results

Your TDEE breakdown now shows:
- BMR adjusted for sleep
- NEAT adjusted for sleep
- Total metabolic impact displayed

## Why This Matters

Most TDEE calculators completely ignore sleep. But research shows sleep deprivation can reduce your daily calorie burn by **200-300 calories** - that's HUGE!

This is especially important if you're:
- Trying to lose weight but not seeing results
- Training hard but not recovering
- Eating "right" but still gaining weight
- Chronically tired or stressed

## Pro Tips

1. **Track your sleep** for 1-2 weeks to get an average
2. **7-8 hours is optimal** - more isn't always better
3. **Quality matters** - poor quality sleep still impacts metabolism
4. **Sleep debt accumulates** - one good night doesn't fix chronic deprivation
5. **Use a sleep tracker** (watch, phone, or dedicated app)

## How to Update

If you already downloaded the calculator, just replace:
- `tdee_calculator.py`
- `tdee_app.py`

With the new versions from the outputs folder.

Or re-download everything fresh!

## Try It Out

Run the calculator and compare:
- Your current sleep vs optimal sleep
- See how many calories you're losing to poor sleep
- Understand why sleep is crucial for your goals

---

**Bottom Line:** Sleep isn't just for recovery - it directly affects how many calories you burn every single day. Track it!
