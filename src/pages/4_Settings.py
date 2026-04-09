
import streamlit as st 

st.title("Settings")

with st.sidebar:
    st.page_link("pages/1_Chat.py")
    st.page_link("pages/2_Search.py")
    st.page_link("pages/3_Your_Information.py")
    st.page_link("pages/4_Settings.py")

if st.button("Log out"): 
    st.session_state.access_token = ""
    st.session_state.user_id = ""
    st.success("You have been logged out successfully.") 
    st.switch_page("Home.py")