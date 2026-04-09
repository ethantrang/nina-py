import streamlit as st
import requests
from supabase import create_client, Client
import os 

from database.supabase_client import supabase

# Define session state variables 

if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'selected_food' not in st.session_state:
    st.session_state.selected_food = None

# Define functions 

def is_authenticated():
    try:
        access_token = st.session_state['access_token']
        if not access_token:
            # TODO: try refresh access token 
            return False

        try:
            user = supabase.auth.get_user(access_token)
            if user:
                st.session_state['user'] = user
                return True
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            return False
    except:
        return False
    
if not is_authenticated():
    st.error("You are not authenticated. Please sign in.")
    st.switch_page("Home.py")

def search_food(query):
    url = "https://trackapi.nutritionix.com/v2/search/instant"
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': "65e62b92",
        'x-app-key': "1e1774e57c8a75b260b499343544f159"
    }
    params = {
        'query': query
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Request failed with status code {response.status_code}"}

def get_nutrition_info(nix_item_id):
    url = "https://trackapi.nutritionix.com/v2/search/item"
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': "65e62b92",
        'x-app-key': "1e1774e57c8a75b260b499343544f159"
    }
    params = {
        'nix_item_id': nix_item_id
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    food = data['foods'][0]
    return format_nutrient_info(food)

def format_nutrient_info(food):
    formatted = (
        f"Food Name: {food['food_name']}\n"
        f"Brand: {food['brand_name']}\n"
        f"Serving Quantity: {food['serving_qty']} {food['serving_unit']}\n"
        f"Serving Weight: {food['serving_weight_grams']} grams\n"
        f"Calories: {food['nf_calories']} kcal\n"
        f"Total Fat: {food['nf_total_fat']} g\n"
        f"Saturated Fat: {food.get('nf_saturated_fat', 'N/A')} g\n"
        f"Cholesterol: {food.get('nf_cholesterol', 'N/A')} mg\n"
        f"Sodium: {food['nf_sodium']} mg\n"
        f"Total Carbohydrate: {food['nf_total_carbohydrate']} g\n"
        f"Dietary Fiber: {food.get('nf_dietary_fiber', 'N/A')} g\n"
        f"Sugars: {food.get('nf_sugars', 'N/A')} g\n"
        f"Protein: {food['nf_protein']} g\n"
        f"Potassium: {food.get('nf_potassium', 'N/A')} mg\n"
    )
    return formatted

# UI Elements 

st.title("🍔 Search Branded Foods & Restaurants")


with st.sidebar:

    st.page_link("pages/1_Chat.py")
    st.page_link("pages/2_Search.py")
    st.page_link("pages/3_Your_Information.py")
    st.page_link("pages/4_Settings.py")


col1, col2 = st.columns(2)

with col1:

    search_query = st.text_input("Enter a branded food or restaurant to search:", placeholder="Try 'Big Mac' or 'Starbucks'")
    if st.button("🔍 Search", use_container_width=True):
        if search_query:
            results = search_food(search_query)
            if 'error' in results:
                st.error(results['error'])
            else:
                st.session_state.search_results = results['branded']  
                st.session_state.selected_food = None
                if st.session_state.search_results:
                    st.success(f"Select one item from the list below to display nutrional information.")
                else:
                    st.warning("No branded food items found. Try a different search term.")
        else:
            st.warning("Please enter a food name to search.")

with col1:
    if st.session_state.search_results:
        st.subheader("Search Items")
        for food in st.session_state.search_results:
            if st.button(f"{food['food_name']} - {food['brand_name']}", key=f"branded_{food['nix_item_id']}", use_container_width=True):
                st.session_state.selected_food = food['nix_item_id']

with col2:
    if st.session_state.selected_food:
        st.subheader("📊 Nutritional Information")
        nutrition_info = get_nutrition_info(st.session_state.selected_food)
        st.text(nutrition_info)

