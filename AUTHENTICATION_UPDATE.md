# Authentication System Update

## Overview
Added an optional authentication system with user accounts, password management, and personalized profiles. Users can now use the app without logging in (with default values) or create an account for personalized settings and data persistence.

## New Features

### 1. Optional Authentication
- **Guest Mode**: Use the app immediately with average American male defaults
- **Login Button**: Click the "🔐 Login" button in the top-right to access your account
- **No Forced Login**: Start using the calculator right away without creating an account
- **Secure Login**: When ready, create an account for personalized defaults and data saving

### 2. Login Dialog (Popup)
- Clean popup interface activated by clicking the Login button
- **Login Form**: Quick access for existing users
- **Create Account**: Seamlessly switch to account creation
- **No Page Redirect**: Dialog overlay keeps you in context

### 3. Create Account Flow
When creating a new account, users can set:
- Username and password (minimum 6 characters)
- **Default Profile Settings**:
  - Basic Info: Sex, Age, Height, Weight, Body Fat %
  - Activity: Daily Steps, Daily Calories, Sleep Hours
  - All values become defaults in the TDEE Calculator when logged in

### 4. My Profile Tab
Dedicated tab for managing your account (requires login):
- **Change Password**: Secure password reset functionality
  - Requires current password verification
  - Minimum 6 character requirement
  - Password confirmation for safety
  
- **Edit Default Settings**: Update all profile defaults
  - Basic Info (sex, age, height, weight, body fat %)
  - Activity Levels (steps, pace, job type, sedentary hours)
  - Diet Defaults (calories, protein, carbs, fat)
  - Sleep Defaults (hours, quality)
  - Workout Defaults (frequency, duration, type, intensity)
  
- **Logout**: Securely end your session and return to guest mode

### 5. Guest Mode with Smart Defaults
- **Average American Male Defaults** when not logged in:
  - Height: 5'9" (average US male)
  - Weight: 200 lbs (average US male)  
  - Age: 38 (median age)
  - Body Fat: 28% (average)
  - Daily Steps: 4,000 (average)
  - Calories: 2,200 (average intake)
  - Sleep: 7 hours (average)
- Use the calculator immediately without any setup
- Header shows "Using default values (Average American Man)"

### 6. Data Saving Prompts
- **Smart Prompts**: Try to save an entry without logging in? Get a friendly prompt
- **One-Click Login**: "🔐 Login Now" button appears right in the save confirmation
- **No Data Loss**: Your entered data stays on screen while you decide to login
- Easy transition from guest to authenticated user

### 7. Conditional Sidebar
- Sidebar only shows on **TDEE Calculator** tab
- Hidden on all other tabs for cleaner interface
- Maximizes screen space for data entry and viewing

## Data Storage

### New Google Sheets Worksheet: "Users"
Automatically created with columns:
- `username`: Unique identifier
- `password_hash`: SHA256 hashed password (never stores plain text)
- `display_name`: User's display name
- Profile defaults: sex, height, weight, age, body fat, steps, calories, sleep, etc.
- Diet defaults: protein, carbs, fat, calories
- Activity defaults: pace, job type, sedentary hours
- Workout defaults: frequency, duration, type, intensity

## Security Features
- ✅ Passwords hashed with SHA256 (not stored as plain text)
- ✅ Password length validation (minimum 6 characters)
- ✅ Password confirmation on creation
- ✅ Current password verification for changes
- ✅ Session-based authentication
- ✅ Automatic logout on browser close

## User Experience Improvements

### Before
- Manual user selection dropdown
- Static defaults for everyone
- No password protection
- Sidebar always visible
- Required account to use app

### After
- **Optional Login** - use immediately or create account later
- **Smart Guest Mode** with average American male defaults
- Login button in top-right corner (clean UI)
- Popup dialog for login/create account (no page redirect)
- Personalized defaults when logged in
- Password-protected accounts
- Profile management tab
- Clean interface with conditional sidebar
- **Save prompts** guide guest users to create accounts
- Easy account creation with initial settings

## How to Use

### Guest Mode (No Account)
1. Open the app - it works immediately!
2. TDEE Calculator uses average American male defaults
3. Adjust any values as needed for your calculations
4. Try to save a Daily Tracker entry → Get prompted to login
5. Create account when ready to save data

### Creating an Account
1. Click **🔐 Login** button in top-right corner
2. Click **Create Account** in the dialog
3. Enter username and password
4. Set your default profile values
5. Click **Create Account**
6. Login with your new credentials

### Returning Users
1. Click **🔐 Login** button
2. Enter username and password
3. Click **Login**
4. Your personalized defaults load automatically

### Managing Your Profile
1. Login to your account
2. Navigate to **👤 My Profile** tab
3. **Change Password**: Expand the "🔒 Change Password" section
4. **Update Defaults**: Modify any settings in the form
5. Click **💾 Save Profile** to save changes

### Daily Use
- **Without Account**: Use TDEE Calculator anytime with default values
- **With Account**: 
  - Login with your credentials
  - Personalized defaults load automatically in TDEE Calculator
  - Daily Tracker saves entries to your account
  - All your data is tied to your username

## Files Modified
- `tdee_app.py`: Added authentication screens, My Profile tab, conditional sidebar
- `auth.py`: **NEW** - Authentication manager with user CRUD operations
- User data stored in Google Sheets "Users" worksheet

## Migration from Previous Version
- Old user selector removed
- App now accessible without authentication
- Guest mode uses average American male defaults
- Existing daily tracker data preserved (tied to username)
- Previous users need to create accounts to access their saved data
- Users can continue using app without account (guest mode)

## Security Features & Recommendations
- ✅ Passwords hashed with SHA256 (not stored as plain text)
- ✅ Password length validation (minimum 6 characters)
- ✅ Password confirmation on creation
- ✅ Current password verification for changes
- ✅ Session-based authentication
- ✅ **Optional authentication** - no forced account creation
- ✅ Guest mode for immediate use
- Use strong passwords (6+ characters minimum)
- Don't share your password
- Logout when using shared computers
- Consider upgrading to bcrypt hashing in future (current: SHA256)

## Future Enhancements
- Password recovery/reset via email
- bcrypt password hashing (more secure than SHA256)
- Multi-factor authentication
- OAuth integration (Google, Facebook login)
- Admin user roles
- Account deletion functionality
- Remember me option
- Email verification for new accounts
