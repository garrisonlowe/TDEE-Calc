# Version History

## Version 1.0.2 🍽️
**Release Date:** January 2, 2026

### New Features

#### Meal Plan Tab
- **Meal Library System**: Create a library of meals you eat every day (no date tracking)
- **Interactive Goal Selection**: Dynamic dropdown to switch between diet goals instantly
  - Aggressive Fat Loss (-750 cal)
  - Moderate Fat Loss (-500 cal)
  - Maintenance (0 cal)
  - Lean Bulk (+250 cal)
  - Standard Bulk (+350 cal)
- **TDEE Auto-Sync**: Automatically pulls TDEE from calculator results
- **Add Meals**: Log meals with name, calories, and macros (protein, carbs, fat)
- **Edit Meals**: Expandable forms to edit any meal with save/delete options
- **Visual Analytics**: 
  - Donut chart showing calories by macro (Protein, Carbs, Fat)
  - Bar chart showing calories per meal
  - Charts use purple gradient theme matching TDEE calculator
  - Bold white text for readability
- **Smart Layout**: 3-column design with donut chart, macro totals, and bar chart
- **Progress Tracking**: Custom-colored progress bar (#0be881) showing daily intake vs target
- **Smart Caching**: Prevents API rate limiting with session state caching
- **Input Auto-Clear**: Form fields reset after successfully adding a meal
- **Google Sheets Integration**: All meals persist across sessions and devices

---

## Version 1.0.1 🔐
**Release Date:** January 2, 2026

### New Features

#### Authentication System
- **Optional Login**: Use the app as a guest or create an account
- **Guest Mode**: Instant access with US average defaults (5'9", 200 lbs, age 38)
- **Create Account**: Save your personal profile with custom defaults
- **My Profile Tab**: Edit your default settings and change password
- **Personalized Experience**: Your defaults auto-populate in the TDEE Calculator
- **Separate Login/Create Account Dialogs**: Clean, easy-to-use interface

#### User Interface Improvements
- Two-button authentication: Login and Create Account buttons for guests
- Streamlined dialog system with easy close/cancel options
- Name field added to user profiles
- Profile settings persist across sessions

---

## Version 1.0 🎉
**Release Date:** January 2, 2026

### Current Features

#### TDEE Calculator
- Dual BMR calculation (Mifflin-St Jeor & Katch-McArdle)
- Macro-specific TEF (Thermic Effect of Food)
- Detailed activity breakdown with MET values
- Workout-specific EPOC calculations
- Weight trend validation (gold standard accuracy)
- Multiple calorie targets for different goals

#### Daily Tracker
- Daily metrics logging (weight, calories, macros, steps, sleep, energy)
- 5 interactive charts with pan/scroll:
  - Weight Progress
  - Calories & Macros
  - Daily Steps
  - Sleep Duration
  - Energy Levels
- Date-only x-axis labels (MMM-DD format)
- Full-width responsive charts
- Yesterday/Today quick buttons
- View & edit all entries in expandable table
- Weekly averages display

#### Multi-User Support
- User selector dropdown
- Add new users on the fly
- Completely separate data per user
- Each user gets own Google Sheets worksheet

#### Cloud Storage
- Automatic Google Sheets sync
- Persistent data across sessions
- Accessible from any device

#### Documentation
- Quick Reference Guide (in-app)
- Full README with research citations
- Version tracking

---

**Next planned features:**
- Data export functionality
- Advanced analytics & trends
- Goal tracking
- Custom macro targets per user
