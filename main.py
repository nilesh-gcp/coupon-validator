import streamlit as st
from auth.oauth_flow import fetch_token, get_auth_url, get_user_info
from config.sheet_adapter import get_approved_emails


def main():
    # If user info is not yet in session, try to authenticate
    approved_emails = get_approved_emails()  # Load from Google Sheet
    if "user_info" not in st.session_state:
        query_params = st.query_params
        auth_code = query_params.get("code")

        if auth_code:
            token_data = fetch_token(auth_code)
            access_token = token_data.get("access_token") if token_data else None

            if access_token:
                user_info = get_user_info(access_token)
                email = user_info.get("email") if user_info else None

                if email in approved_emails:
                    st.session_state.user_info = user_info  # Persist user info
                    st.success(f"Welcome, {email}!")
                    print("approved email:", approved_emails)
                    print ("user email:", email)
                else:
                    print("approved email:", approved_emails)
                    print ("user email:", email)
                    st.error("Access denied.")
                    st.stop()
            else:
                st.error("Failed to retrieve access token.")
                st.stop()
        else:
            st.markdown(f"[Login with Google]({get_auth_url()})")
            st.stop()
    else:
        email = st.session_state.user_info.get("email")
        st.success(f"Welcome back, {email}!")

        # Logout button
        if st.button("Logout"):
            del st.session_state["user_info"]
            st.rerun()


if __name__ == "__main__": 
    main()