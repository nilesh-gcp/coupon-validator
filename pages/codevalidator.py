import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# pages/codevalidator.py

SHEET_ID='1xhk2T2Xk-2CtkXPNeBlPb0jtDGLmm6p4x7S2PHjYeLs'
WORKSHEET_NAME = "CouponCodes"

def connect_to_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("config/tnsdashboard-service-acct.json", scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SHEET_ID)
    return spreadsheet.worksheet(WORKSHEET_NAME)


# EXCEL_PATH = "coupons.xlsx"

# @st.cache_data

def load_sheet_as_df():
    sheet = connect_to_sheet(WORKSHEET_NAME)
    data = sheet.get_all_records()
    # st.write("Raw data from gspread:", data)
    return pd.DataFrame(data)

def find_coupon(df, code):
    code = code.strip().upper()
    match = df[df['CouponCode'].str.upper() == code]
    return match.iloc[0] if not match.empty else None

def update_coupon(sheet, df, code, user_email, expiry_date, comments):
    idx = df[df['CouponCode'].str.upper() == code.strip().upper()].index[0]
    print (f"Updating coupon at index: {idx}")
    row_number = idx + 2  # account for header row
    sheet.update_cell(row_number, 2, "Expired")  # Status
    sheet.update_cell(row_number, 3, user_email)  # Updated By
    sheet.update_cell(row_number, 4, expiry_date.strftime("%Y-%m-%d"))  # Expiry Date
    sheet.update_cell(row_number, 5, comments)  # Comments
    sheet.update_cell(row_number, 6, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # Timestamp


st.title("🔐 CouponCode Validator")

if "user_info" in st.session_state:
    user_email = st.session_state.user_info.get("email")
else:
    st.error("Not logged in")
    st.stop()


df = load_sheet_as_df()
# st.write("Columns returned:", df.columns.tolist())
sheet = connect_to_sheet(WORKSHEET_NAME)
code_input = st.text_input("Enter CouponCode")

# Step 1: Validate and store the result
if st.button("Validate"):
    record = find_coupon(df, code_input)
    if record is None:
        st.error("❌ CouponCode not found.")
    else:
        st.session_state['validated_record'] = record
        st.session_state['validated_code'] = code_input

# Step 2: If we have a validated record, show it + the form
if 'validated_record' in st.session_state:
    record = st.session_state['validated_record']
    code_input = st.session_state['validated_code']

    st.write(f"**Status:** {record['Status']}")

    if record['Status'].lower() == "expired":
        st.warning("This code is already marked as expired.")
    else:
        with st.form("expire_form"):
            expiry_date = st.date_input("Expiry Date")
            comments = st.text_area("Comments (max 256 chars)", max_chars=256)
            submit = st.form_submit_button("Mark as Expired")

            if submit:
                print(f"Updating coupon: {code_input}, user_email: {user_email}, expiry_date: {expiry_date}, comments: {comments}")
                update_coupon(sheet, df, code_input, user_email, expiry_date, comments)
                st.success("✅ Coupon marked as expired.")
                # df = load_sheet_as_df(sheet)
                st.session_state.pop('validated_record')
                st.rerun()



# if st.button("Validate"):
#     record = find_coupon(df, code_input)
#     if record is None:
#         st.error("❌ CouponCode not found.")
#     else:
#         st.write(f"**Status:** {record['Status']}")
#         if record['Status'].lower() == "expired":
#             st.warning("This code is already marked as expired.")
#         else:
#             with st.form("expire_form"):
#                 expiry_date = st.date_input("Expiry Date")
#                 comments = st.text_area("Comments (max 256 chars)", max_chars=256)
#                 submit = st.form_submit_button("Mark as Expired")
#                 print(f"Form submitted with expiry_date: {expiry_date}, comments: {comments}")
#                 if not expiry_date:
#                     st.error("Please select an expiry date.")
#                 if submit:
#                     print(f"Updating coupon: {code_input}, user_email: {user_email}, expiry_date: {expiry_date}, comments: {comments}" )
#                     update_coupon(sheet, df, code_input, user_email, expiry_date, comments)
#                     st.success("✅ Coupon marked as expired.")
#                     st.experimental_rerun()
#                 else:
#                     st.info("Fill the form and click 'Mark as Expired' to update the status.")
# else:
#     st.info("Enter a CouponCode to validate.")  