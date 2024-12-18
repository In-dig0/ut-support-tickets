import streamlit as st


def display_app_title() -> None:
    """ Show app title and description """
    st.set_page_config(page_title="TORP_APP_Main_menù", page_icon="🎯")
    st.title("🎯 :blue[TORP APP: Technical Office Request POC]")
    st.write(
        """
        This is the IPH TORP APP, that lets IPH users to create a support request to IPH Technical Office. 
        """
    )
    st.markdown("Powered with Streamlit :streamlit:")
    st.divider()

def main():
#    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")
    display_app_title()

if __name__ == "__main__":
    main()