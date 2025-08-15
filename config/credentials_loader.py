# config/credentials_loader.py

import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import logging

def load_gcp_credentials(scope, *, dev_mode=False):
    """
    Loads and validates GCP service account credentials from Streamlit secrets.
    
    Args:
        scope (list): List of OAuth scopes.
        dev_mode (bool): If True, logs full credential details for debugging.
    
    Returns:
        ServiceAccountCredentials object if valid, else raises ValueError.
    """
    try:
        raw_creds = st.secrets.get("gcp_service_account")
        if raw_creds is None:
            raise ValueError("Missing 'gcp_service_account' in secrets.")

        creds_dict = dict(raw_creds)  # Convert AttrDict to dict

        # Validate required fields
        # print("🔍 Raw private_key from secrets:", repr(creds_dict["private_key"]))
        required_keys = ["private_key", "client_email", "token_uri"]
        missing = [k for k in required_keys if not creds_dict.get(k)]
        if missing:
            raise ValueError(f"Missing required keys in credentials: {missing}")

        # Validate private key format
        pk = creds_dict["private_key"].replace("\\n", "\n")
        if not pk.strip().startswith("-----BEGIN PRIVATE KEY-----"):
            raise ValueError("Invalid private key format.")
        creds_dict["private_key"] = pk  # Update before passing to Google
        # print("🔍 Processed private_key:", repr(creds_dict["private_key"]))

        if dev_mode:
            logging.info("✅ GCP credentials loaded successfully.")
            logging.debug("🔍 Full credentials:\n%s", creds_dict)

        return ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    except Exception as e:
        logging.error("❌ Failed to load GCP credentials: %s", e)
        raise