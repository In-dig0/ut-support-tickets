import streamlit as st
import hmac 

def display_app_title() -> None:
    """ Show app title and description """
    st.set_page_config(page_title="TORP_APP_main_page", page_icon="🎯")
    st.title("🎯 :blue[TORP APP: Technical Office Request POC]")
    st.write(
        """
        This is the IPH TORP APP, that lets IPH users to create a support request to IPH Technical Office. 
        """
    )
    st.markdown("Powered with Streamlit :streamlit:")
    st.divider()

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

def main():
    if not check_password():
        st.stop()
    display_app_title()

if __name__ == "__main__":
    main()