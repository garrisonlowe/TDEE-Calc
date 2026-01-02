# Google Sheets Setup Guide

This guide will help you set up Google Sheets as the database for your TDEE Tracker app.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a Project" → "New Project"
3. Name it "TDEE Tracker" (or whatever you prefer)
4. Click "Create"

## Step 2: Enable Google Sheets API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Sheets API"
3. Click on it and press "Enable"
4. Also search for and enable "Google Drive API"

## Step 3: Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name: `tdee-tracker-service`
4. Click "Create and Continue"
5. Skip optional steps, click "Done"

## Step 4: Generate Credentials JSON

1. Click on the service account you just created
2. Go to the "Keys" tab
3. Click "Add Key" → "Create New Key"
4. Choose "JSON" format
5. Click "Create" - a JSON file will download

## Step 5: Set Up Credentials Locally

1. Rename the downloaded file to `credentials.json`
2. Move it to your TDEE-Calc-App folder
3. **IMPORTANT**: Never commit this file to GitHub!

## Step 6: Share Google Sheet (First Run)

When you first run the app, it will create a new Google Sheet called "TDEE Tracker Data". 

To access it in your Google Drive:
1. Go to [Google Drive](https://drive.google.com)
2. Search for "TDEE Tracker Data"
3. Right-click → Share
4. Add your personal Gmail address with "Editor" access

OR modify the code in `daily_tracker.py` around line 58 to automatically share:
```python
spreadsheet.share('your-email@gmail.com', perm_type='user', role='writer')
```

## Step 7: Deploy to Streamlit Cloud (Optional)

For deployment, add your credentials to Streamlit Secrets:

1. Go to your app dashboard on Streamlit Cloud
2. Click "Settings" → "Secrets"
3. Paste your entire `credentials.json` content in this format:

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR-PRIVATE-KEY\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

**Important**: For the `private_key`, replace actual newlines with `\n`

## Switching Between JSON and Google Sheets

The app automatically tries Google Sheets first and falls back to JSON if credentials are missing.

To force JSON mode (for testing), modify `tdee_app.py`:
```python
tracker = DailyTracker(use_sheets=False)
```

To use Google Sheets (default):
```python
tracker = DailyTracker(use_sheets=True)
```

## Troubleshooting

### "No module named 'gspread'"
Run: `pip install gspread google-auth`

### "Credentials not found"
Make sure `credentials.json` is in your app folder

### "Permission denied"
Share the Google Sheet with your service account email (found in credentials.json as `client_email`)

### Data not showing up
Check the "Entries" worksheet in your Google Sheet - the app creates it automatically on first run
