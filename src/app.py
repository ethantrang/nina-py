import time
import streamlit as st
from urllib.parse import urlparse, parse_qs
from streamlit_javascript import st_javascript
from dotenv import load_dotenv
import os
from streamlit_cookies_manager import EncryptedCookieManager

load_dotenv()

# Local imports
import sys 
sys.path.append("/")
from database.supabase_client import supabase

st.set_page_config(
    page_title="Nina - Your Nutritional Navigation Assistant",
)

# Initialize cookie manager
cookies = EncryptedCookieManager(prefix="ethan", password="this_is_a_password")

if not cookies.ready():
    st.stop()

# Define session state variables

if "user_id" not in st.session_state: 
    st.session_state.user_id = cookies.get("user_id", "")

if "access_token" not in st.session_state: 
    st.session_state.access_token = cookies.get("access_token", "")

# Define functions

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
        cookies[key] = value[0]  # Store in cookies

    if "user_id" not in st.session_state and "access_token" in st.session_state:
        user = get_user(st.session_state.access_token)
        st.session_state.user_id = user.user.id
        cookies["user_id"] = user.user.id  # Store user_id in cookies
    
    cookies.save()  # Save cookies

    return None

@st.experimental_dialog("Login with Email")
def login_with_email():
    email = st.text_input("Email")
    if st.button("Login"):
        try: 
            with st.spinner("Working"):
                response = supabase.auth.sign_in_with_otp(
                    {
                        "email": f"{email}",
                        "options": {"email_redirect_to": "http://localhost:8501/Home"},
                    }
                )   
                st.success("Please check your email for the login link.")
        except Exception as e: 
            st.error(f"Something went wrong:( Please try again later.")

# UI Elements 

st.header("Nina - Your Nutritional Navigation Assistant")

if st.button("Login with Email"): 
    login_with_email()

if st.session_state.access_token == "":
    auth_url = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": 'http://localhost:8501/Home'
            }
        })

    st.link_button("Login with Google", auth_url.url)

    store_session_in_state()

if st.session_state.access_token != "":
    # TODO: check if access token is valid 

    st.session_state.access_token
    st.switch_page("pages/1_Chat.py")



#### Working auth code

# import time
# import streamlit as st
# from urllib.parse import urlparse, parse_qs
# from streamlit_javascript import st_javascript
# from dotenv import load_dotenv
# import os
# load_dotenv()

# # local imports
# import sys 
# sys.path.append("/")
# from database.supabase_client import supabase

# st.set_page_config(
#     page_title="Nina - Your Nutritional Navigation Assistant",
# )


# # Define session state variables

# if "user_id" not in st.session_state: 
#     st.session_state.user_id = ""

# if "access_token" not in st.session_state: 
#     st.session_state.access_token = ""

# # Define functions

# def get_user(access_token: str):
#     user = supabase.auth.get_user(access_token)
#     return user

# def store_session_in_state():
#     callback_url = st_javascript("await fetch('').then(r => window.parent.location.href)")
#     parsed_url = urlparse(callback_url)
#     fragment = parsed_url.fragment
#     params = parse_qs(fragment)

#     for key, value in params.items():
#         st.session_state[key] = value[0] 

#     if "user_id" not in st.session_state and "access_token" in st.session_state:
#         st.session_state.user_id = get_user(st.session_state.access_token).user.id
        
#     return None

# @st.experimental_dialog("Login with Email")
# def login_with_email():
#     email = st.text_input("Email")
#     if st.button("Login"):

#         try: 
#             with st.spinner("Working"):
#                 response = supabase.auth.sign_in_with_otp(
#                     {
#                         "email": f"{email}",
#                         "options": {"email_redirect_to": "http://localhost:8501/Home"},
#                     }
#                 )   
#                 st.success("Please check your email for the login link.")
#         except Exception as e: 
#             st.error(f"Something went wrong:( Please try again later.")

#         # with st.spinner("Sending login link..."):

# # UI Elements 

# st.header("Nina - Your Nutritional Navigation Assistant")

# if st.button("Login with Email"): 
#     login_with_email()

# if st.session_state.access_token == "":

#     auth_url = supabase.auth.sign_in_with_oauth({
#             "provider": "google",
#             "options": {
#                 "redirect_to": 'http://localhost:8501/Home'
#             }
#         })

#     st.link_button("Login with Google", auth_url.url)

#     store_session_in_state()

# if not st.session_state.access_token == "":

#     # TODO: check if access token is valid 

#     st.session_state.access_token
#     st.switch_page("pages/1_Chat.py")