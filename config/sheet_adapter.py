import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config.config import get



# SHEET_ID = "1xhk2T2Xk-2CtkXPNeBlPb0jtDGLmm6p4x7S2PHjYeLs"  # Replace with actual ID
# WORKSHEET_NAME = "reservations"

SHEET_ID = get("SHEET_ID")
WORKSHEET_NAME = get("WORKSHEET_NAME", "reservations")  # Default to "reservations" if not set  



# === Sheet Connection ===
def get_sheet():
    """
    Authorizes and returns the worksheet object using Sheet ID and Worksheet name.
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("config/tnsdashboard-service-acct.json", scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SHEET_ID)
    return spreadsheet.worksheet(WORKSHEET_NAME)

# def get_user_reservations(email):
#     sheet = get_sheet()
#     rows = sheet.get_all_records()
#     return [r for r in rows if r["user_email"] == email]


#  == Trial function ==
def get_all_reservations():
    sheet = get_sheet()
    return sheet.get_all_records()


# === Add Reservation ===
def add_reservation(data: dict) -> None:
    sheet = get_sheet()
    headers = sheet.row_values(1)
    new_row = [data.get(h, "") for h in headers]
    sheet.append_row(new_row, value_input_option="USER_ENTERED")


def update_reservation(res_id, updates):
    sheet = get_sheet()
    rows = sheet.get_all_records()
    for i, row in enumerate(rows):
        if str(row["id"]) == str(res_id):
            for key, value in updates.items():
                sheet.update_cell(i + 2, list(row.keys()).index(key) + 1, value)
            sheet.update_cell(i + 2, list(row.keys()).index("updated_at") + 1, datetime.utcnow().isoformat())
            break

def delete_reservation(res_id):
    sheet = get_sheet()
    rows = sheet.get_all_records()
    for i, row in enumerate(rows):
        if str(row["id"]) == str(res_id):
            sheet.delete_row(i + 2)
            break


def get_approved_emails():
    # Auth scopes for Sheets + Drive
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    print("Using SHEET_ID:", SHEET_ID)
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "config/tnsdashboard-service-acct.json", 
        scope
    )
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(SHEET_ID).worksheet("Users")
    data = sheet.get_all_records()

    # Extract email column (case-insensitive)
    emails = [row['email'].strip().lower() for row in data if row.get('email')]
    return emails