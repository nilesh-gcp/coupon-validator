import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
from config.config import get


# HH
def get_logger_sheet():

    ACCESS_LOG = get("ACCESS_LOG")
    LOG_WORKSHEET_NAME = get("LOG_WORKSHEET_NAME") 
    # print("Accessing logger sheet...")
    if not ACCESS_LOG or not LOG_WORKSHEET_NAME:
        raise ValueError("ACCESS_LOG and LOG_WORKSHEET_NAME must be set in secrets or .env")    
    # Define the scope for Google Sheets API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    # print("Using Streamlit secrets for GCP service account logging module")
    # print("Connecting to logger sheet...")
    # Open the logger sheet by its ID and return the specified worksheet
    # print(f"Accessing sheet: {ACCESS_LOG}, worksheet: {LOG_WORKSHEET_NAME}")
    logspreadsheet = client.open_by_key(ACCESS_LOG)
    if LOG_WORKSHEET_NAME in [ws.title for ws in logspreadsheet.worksheets()]:
        # print(f"Worksheet '{LOG_WORKSHEET_NAME}' found.")
        # logspreadsheet.add_worksheet(title=LOG_WORKSHEET_NAME, rows="100", cols="20")
        return logspreadsheet.worksheet(LOG_WORKSHEET_NAME)
    else:
        # print(f"Worksheet '{LOG_WORKSHEET_NAME}' found. Returning it.")
        log_event("SheetAccess", source="Logger", details=f"Workshet not found: {LOG_WORKSHEET_NAME}")
        # Return the existing worksheet
    # Ensure the sheet ID and worksheet name are correct
    # return client.open(ACCESS_LOG).worksheet(LOG_WORKSHEET_NAME)

def log_event(event_type, email=None, details="", source="Home"):
    try:
        # print("Logging event:", event_type, email, details, source)
        sheet = get_logger_sheet()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, event_type, email or "Unknown", details, source]
        response = sheet.append_row(row)
        # print("✅ Logged event:", row)
        return response
    except Exception as e:
        import traceback
        print("❌ Logging failed:", e)
        traceback.print_exc()
