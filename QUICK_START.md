# 🚀 QUICK START GUIDE

## How to Run Your TDEE Calculator

### Step 1: Open Terminal/Command Prompt

Navigate to where you saved the files:
```bash
cd /path/to/your/files
```

### Step 2: Run the App

**Option A - Easy way:**
```bash
./run_calculator.sh
```

**Option B - Manual:**
```bash
streamlit run tdee_app.py
```

### Step 3: Use the Calculator

The app will open in your browser automatically at `http://localhost:8501`

## What You'll See

### Sidebar (Left) - Your Inputs
Fill out all sections:

1. **📋 Basic Stats**
   - Weight in pounds
   - Height in feet and inches
   - Age
   - Sex
   - Body fat % (optional but helpful)

2. **🍽️ Diet**
   - Daily calories
   - Protein, carbs, fat in grams

3. **🚶 Daily Activity**
   - Daily step count
   - Walking pace
   - Job type
   - Hours sitting per day

4. **🏋️ Workouts**
   - Workouts per week
   - Type (Heavy Lifting, HIIT, etc.)
   - Duration and intensity

5. **⚖️ Weight Trend** (HIGHLY RECOMMENDED)
   - Check "I have weight trend data"
   - Enter weight change (negative for loss)
   - Days tracked (minimum 7, recommend 14+)

### Main Area (Center) - Your Results

After clicking "🔥 Calculate TDEE":

**📊 Your Results**
- Big number showing your TDEE
- If you added weight data: "ACTUAL TDEE from weight data"
- If no weight data: "Estimated TDEE"

**📈 Energy Expenditure Breakdown**
- 5 boxes showing:
  - BMR (your baseline metabolism)
  - TEF (calories burned digesting food)
  - NEAT (daily movement)
  - EAT (exercise calories)
  - EPOC (afterburn from workouts)

**✅ Weight Trend Validation** (if you provided data)
- Shows formula estimate vs actual TDEE
- Tells you the difference
- Warns if metabolic adaptation detected

**🎯 Calorie Targets**
- Fat loss targets (aggressive & moderate)
- Maintenance calories
- Muscle gain targets (lean & standard)

**💡 Pro Tips**
- Quick reminders for accuracy

### Top Tabs

**📊 Calculator** - Main calculator (described above)

**📖 How It Works** - Explanation of methodology

**🔬 Methodology** - Deep dive into research and formulas

## Example Data (For Testing)

If you want to test it out first:

**Basic:**
- Weight: 185 lbs
- Height: 5 feet 11 inches
- Age: 30
- Sex: Male
- Body fat: 15%

**Diet:**
- Calories: 2500
- Protein: 200g
- Carbs: 250g
- Fat: 80g

**Activity:**
- Steps: 8000
- Pace: Average
- Job: Desk Job
- Sedentary: 9 hours

**Workouts:**
- Per week: 4
- Type: Heavy Lifting
- Duration: 75 minutes
- Intensity: High

**Weight Trend:**
- ✅ I have weight trend data
- Change: -2.2 lbs (lost weight)
- Days: 14

**Expected Result:** ~3050 cal/day

## Tips for Best Results

### For Maximum Accuracy:

1. **Track Your Weight Properly**
   - Weigh daily at same time
   - Morning, after bathroom, before eating
   - Track for 14+ days minimum
   - Use a weight trend app (Happy Scale, Libra)

2. **Be Honest About Activity**
   - Most people OVERESTIMATE
   - "Desk Job" if you sit most of the day
   - Count only actual workout time, not gym time

3. **Track Macros Accurately**
   - Use a food scale
   - Log everything
   - The TEF calculation depends on accurate macros

4. **Understand Water Weight**
   - Can fluctuate ±5 lbs daily
   - Focus on weekly trends
   - Menstrual cycle affects weight (if female)

### Recommended Apps:

- **Weight Tracking**: Happy Scale (iOS), Libra (Android)
- **Food Tracking**: MacroFactor, MyFitnessPal, Cronometer
- **Step Tracking**: Your phone (built-in) or fitness watch

## Troubleshooting

**"App won't open in browser"**
- Manually go to: http://localhost:8501
- Check if Streamlit installed: `streamlit --version`

**"Missing module error"**
- Install Streamlit: `pip install streamlit --break-system-packages`
- Make sure `tdee_calculator.py` is in same folder

**"Results seem wrong"**
- Verify all inputs are correct
- Add weight trend data for validation
- Check units (lbs, not kg)
- Remember: ±10-15% variation is normal

**"Want to use metric?"**
- Use the original `tdee_calculator.py` (command line version)
- It uses kg and cm

## Next Steps

1. Fill out the calculator with YOUR data
2. If you don't have weight trend data yet:
   - Use the estimate
   - Start tracking weight TODAY
   - Come back in 2 weeks with real data
3. Use the calorie targets to plan your diet
4. Track progress and adjust as needed

## Questions?

Check the **📖 How It Works** and **🔬 Methodology** tabs in the app for detailed explanations.

---

**Remember:** The weight trend validation is the GOLD STANDARD. Take the time to track your weight properly for maximum accuracy!
