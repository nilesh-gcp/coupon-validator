import requests
import os
from urllib.parse import urlencode
from dotenv import load_dotenv
from config.config import get
load_dotenv()

# Load secrets from environment
# CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_ID = get("GOOGLE_CLIENT_ID")
# print("Client ID:", CLIENT_ID)

# CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
CLIENT_SECRET = get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = get("REDIRECT_URI", "http://localhost:8501")  # Default to localhost if not set

AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

def get_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": REDIRECT_URI,
        "access_type": "offline",
        "prompt": "consent"
    }
    # print("Auth code is:", params.get("code"))
    return f"{AUTHORIZATION_URL}?{urlencode(params)}"


def fetch_token(code):
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    # print("Preparing token request with:")
    # print("Client ID:", CLIENT_ID)
    # print("Client Secret:", CLIENT_SECRET)
    # print("Redirect URI:", REDIRECT_URI)
    # print("Auth Code:", code)

    try:
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error fetching token:", e)
        if response is not None:
            print("Response content:", response.json)
        return {}


def get_user_info(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(USERINFO_URL, headers=headers)
    return response.json()