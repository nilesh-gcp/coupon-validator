# config.py

import os

try:
    import streamlit as st
    STREAMLIT = True
except ImportError:
    STREAMLIT = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: dotenv not available, .env file will not be loaded.")
    pass  # dotenv not available, skip loading .env


def get(key: str, default=None):
    """
    Retrieves configuration value from Streamlit secrets or .env.
    Priority: Streamlit secrets > .env > default
    """
    if STREAMLIT and key in st.secrets:
        print(f"Using Streamlit secret for {key}", st.secrets[key])
        return st.secrets[key]

    return os.getenv(key, default)