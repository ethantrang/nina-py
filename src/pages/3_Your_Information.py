import streamlit as st
import json
import os
from datetime import datetime, date
from database.supabase_client import supabase

USER_DATA_FILE = "user_data.json"

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
    



# Function to read user data from the JSON file
def read_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {
        "basic_info": {
            "name": "",
            "age": 0,
            "gender": "Select",
            "height": 0,
            "weight": 0
        },
        "health_fitness": {
            "activity_level": "Select",
            "goals": "",
            "activity_types": "",
            "medical_conditions": "",
            "allergies": "",
            "dietary_preferences": ""
        },
        "lifestyle": {
            "sleep": "Select",
            "stress_level": 0
        },
        "fitness_nutrition_data": {
            "workout_history": "",
            "dietary_intake": "",
            "water_intake": "Select",
            "supplement_use": ""
        },
        "technical_engagement": {
            "preferences": ""
        },
        "advanced_data": {
            "heart_rate": "",
            "daily_steps": ""
        },
        "privacy_consent": {
            "data_collection_consent": False,
            "data_sharing_preferences": False
        }
    }

# Function to write user data to the JSON file
def write_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

st.title("⚙️ Your Information")

with st.sidebar:

    st.page_link("pages/1_Chat.py")
    st.page_link("pages/2_Search.py")
    st.page_link("pages/3_Your_Information.py")
    st.page_link("pages/4_Settings.py")

# Load current user data
user_data = read_user_data()

# Basic Personal Information
with st.expander("🧍 Basic Personal Information"):
    user_data["basic_info"]["name"] = st.text_input("Name", value=user_data["basic_info"]["name"])
    user_data["basic_info"]["age"] = st.number_input("Age", min_value=0, value=user_data["basic_info"]["age"])
    
    gender_options = ["Select", "Male", "Female", "Other"]
    gender_index = gender_options.index(user_data["basic_info"]["gender"]) if user_data["basic_info"]["gender"] in gender_options else 0
    user_data["basic_info"]["gender"] = st.selectbox("Gender", gender_options, index=gender_index)
    
    user_data["basic_info"]["height"] = st.number_input("Height (cm)", min_value=0, value=user_data["basic_info"]["height"])
    user_data["basic_info"]["weight"] = st.number_input("Weight (kg)", min_value=0, value=user_data["basic_info"]["weight"])

# Health and Fitness Information
with st.expander("🏋️ Health and Fitness Information"):
    activity_level_options = ["Select", "sedentary (little to no exercise)", "lightly active (1-3 days)", "moderately active (3-5 days)", "very active (6-7 days)"]
    activity_level_index = activity_level_options.index(user_data["health_fitness"]["activity_level"]) if user_data["health_fitness"]["activity_level"] in activity_level_options else 0
    user_data["health_fitness"]["activity_level"] = st.selectbox("Activity Level", activity_level_options, index=activity_level_index)

    user_data["health_fitness"]["goals"] = st.text_input("Goals (e.g., weight loss, muscle gain, endurance, maintaining)", value=user_data["health_fitness"]["goals"])

    user_data["health_fitness"]["activity_types"] = st.text_input("Types of Activity (e.g., Cardio, Strength Training, Flexibility, Mixed)", value=user_data["health_fitness"]["activity_types"])

    user_data["health_fitness"]["medical_conditions"] = st.text_input("Medical Conditions", value=user_data["health_fitness"]["medical_conditions"])
    user_data["health_fitness"]["allergies"] = st.text_input("Allergies", value=user_data["health_fitness"]["allergies"])

    user_data["health_fitness"]["dietary_preferences"] = st.text_input("Dietary Preferences (e.g., Vegan, Vegetarian, Gluten-free, Keto, Paleo, None)", value=user_data["health_fitness"]["dietary_preferences"])

# Lifestyle Information
with st.expander("🌙 Lifestyle Information"):
    sleep_options = ["Select", "10+ hours", "8+ hours", "6+ hours", "Less than 6 hours"]
    sleep_index = sleep_options.index(user_data["lifestyle"]["sleep"]) if user_data["lifestyle"]["sleep"] in sleep_options else 0
    user_data["lifestyle"]["sleep"] = st.selectbox("Sleep", sleep_options, index=sleep_index)

    user_data["lifestyle"]["stress_level"] = st.slider("Perceived Stress Levels (1-10)", min_value=1, max_value=10, value=user_data["lifestyle"]["stress_level"])

# Fitness and Nutrition Data
with st.expander("🥗 Fitness and Nutrition Data"):
    user_data["fitness_nutrition_data"]["workout_history"] = st.text_input("Workout History (previous and current workout routines, intensity, duration, and frequency)", value=user_data["fitness_nutrition_data"]["workout_history"])
    user_data["fitness_nutrition_data"]["dietary_intake"] = st.text_input("Dietary Intake (specific cuisine preferences and frequency of meals per day)", value=user_data["fitness_nutrition_data"]["dietary_intake"])

    water_intake_options = ["Select", "2-3 liters/day (standard)", "less than 2L", "more than 2L", "3+ Liters"]
    water_intake_index = water_intake_options.index(user_data["fitness_nutrition_data"]["water_intake"]) if user_data["fitness_nutrition_data"]["water_intake"] in water_intake_options else 0
    user_data["fitness_nutrition_data"]["water_intake"] = st.selectbox("Water Intake", water_intake_options, index=water_intake_index)

    user_data["fitness_nutrition_data"]["supplement_use"] = st.text_area("Supplements taken", value=user_data["fitness_nutrition_data"]["supplement_use"])

# Advanced Data (optional)
with st.expander("📊 Advanced Data (optional)"):
    user_data["advanced_data"]["heart_rate"] = st.text_input("Heart Rate (if applicable)", value=user_data["advanced_data"]["heart_rate"])
    user_data["advanced_data"]["daily_steps"] = st.text_input("Estimated Daily Steps Tracking (if applicable)", value=user_data["advanced_data"]["daily_steps"])

# Privacy and Consent
with st.expander("🔒 Privacy and Consent"):
    user_data["privacy_consent"]["data_collection_consent"] = st.radio("Consent for Data Collection", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["privacy_consent"]["data_collection_consent"] else "No")) == "Yes"
    user_data["privacy_consent"]["data_sharing_preferences"] = st.radio("Data Sharing Preferences (with third parties or only within app)", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["privacy_consent"]["data_sharing_preferences"] else "No")) == "Yes"

# Save button
if st.button("Save"):
    write_user_data(user_data)
    st.success("Settings saved successfully!")
