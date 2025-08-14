import json

# Load your credentials.json
with open("config/tnsdashboard-service-acct.json", "r") as f:
    creds = json.load(f)

# Escape the private key
escaped_key = creds["private_key"].replace("\n", "\\n")

# Generate TOML block
toml_block = f"""
# Paste this into Streamlit secrets.toml

SERVICE_EMAIL = "{creds['client_email']}"
PRIVATE_KEY = "{escaped_key}"
SHEET_ID = "your-google-sheet-id"  # Replace with actual Sheet ID
"""

print(toml_block)