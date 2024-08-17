import streamlit as st
from supabase import create_client, Client
import streamlit_oauth as oauth
from urllib.parse import urlencode, urlparse, parse_qs

from streamlit_javascript import st_javascript

from dotenv import load_dotenv
import os
load_dotenv()
# Initialize Supabase client

st.set_page_config(
    page_title="Nina - Your Nutritional Navigation Assistant",
)

st.header("Nina - Your Nutritional Navigation Assistant")

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

if "user_id" not in st.session_state: 
    st.session_state.user_id = ""

if "access_token" not in st.session_state: 
    st.session_state.access_token = ""


def get_user(access_token: str):
    user = supabase.auth.get_user(access_token)
    return user

def store_session_in_state():
    callback_url = st_javascript("await fetch('').then(r => window.parent.location.href)")
    parsed_url = urlparse(callback_url)
    fragment = parsed_url.fragment
    params = parse_qs(fragment)

    for key, value in params.items():
        st.session_state[key] = value[0] 

    if "user_id" not in st.session_state and "access_token" in st.session_state:
        st.session_state["user_id"] = get_user(st.session_state["access_token"]).user.id
        
    return None

if st.session_state.access_token == "":
    auth_url = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": 'http://localhost:8501/main'
            }
        })

    st.link_button("Login via Google", auth_url.url)

    store_session_in_state()

if not st.session_state.access_token == "":

    # TODO: check if access token is valid 

    st.session_state.access_token
    st.switch_page("pages/Chat.py")