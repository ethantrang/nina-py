import streamlit as st
import json
import os
from datetime import datetime, date

# Define the path to the JSON file
USER_DATA_FILE = "user_data.json"

# Function to read user data from the JSON file
def read_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {
        "personal_info": {
            "full_name": "",
            "date_of_birth": "",
            "gender": "",
            "height": 0,
            "weight": 0
        },
        "medical_history": {
            "chronic_conditions": False,
            "conditions_details": "",
            "medications": False,
            "medications_list": "",
            "surgeries": False,
            "surgeries_details": "",
            "allergies": False,
            "allergies_details": ""
        },
        "lifestyle_habits": {
            "sleep_hours": "",
            "smoking": False,
            "alcohol": False,
            "alcohol_frequency": "",
            "recreational_drugs": False
        },
        "fitness_activity": {
            "fitness_level": "",
            "exercise_days_per_week": "",
            "exercise_types": "",
            "injuries": False,
            "injuries_details": ""
        },
        "dietary_preferences": {
            "specific_diet": False,
            "diet_details": "",
            "meals_per_day": "",
            "dietary_supplements": False,
            "supplements_list": ""
        },
        "preferences_goals": {
            "preferences": "",
            "goals": ""
        },
        "consent_privacy": {
            "consent_data_collection": False,
            "consent_advice": False
        }
    }

# Function to write user data to the JSON file
def write_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

st.title("Settings")

# Load current user data
user_data = read_user_data()

# Ensure date_of_birth is in datetime.date format
if isinstance(user_data["personal_info"]["date_of_birth"], str):
    try:
        user_data["personal_info"]["date_of_birth"] = datetime.strptime(user_data["personal_info"]["date_of_birth"], "%Y-%m-%d").date()
    except ValueError:
        user_data["personal_info"]["date_of_birth"] = date.today()  # Default to today if there's an issue

# Personal Information Section
with st.expander("1. Personal Information"):
    user_data["personal_info"]["full_name"] = st.text_input("Full Name:", value=user_data["personal_info"]["full_name"])
    
    user_data["personal_info"]["date_of_birth"] = st.date_input("Date of Birth:", value=user_data["personal_info"]["date_of_birth"])
    
    gender_options = ["Select", "Male", "Female", "Other"]
    gender_index = gender_options.index(user_data["personal_info"]["gender"]) if user_data["personal_info"]["gender"] in gender_options else 0
    user_data["personal_info"]["gender"] = st.selectbox("Gender:", gender_options, index=gender_index)
    
    user_data["personal_info"]["height"] = st.number_input("Height (cm):", min_value=0, value=user_data["personal_info"]["height"])
    user_data["personal_info"]["weight"] = st.number_input("Weight (kg):", min_value=0, value=user_data["personal_info"]["weight"])

# Medical History Section
with st.expander("2. Medical History"):
    user_data["medical_history"]["chronic_conditions"] = st.radio("Do you have any chronic medical conditions (e.g., diabetes, hypertension)?", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["medical_history"]["chronic_conditions"] else "No")) == "Yes"
    if user_data["medical_history"]["chronic_conditions"]:
        user_data["medical_history"]["conditions_details"] = st.text_input("If yes, please specify:", value=user_data["medical_history"]["conditions_details"])
    user_data["medical_history"]["medications"] = st.radio("Are you currently taking any medications?", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["medical_history"]["medications"] else "No")) == "Yes"
    if user_data["medical_history"]["medications"]:
        user_data["medical_history"]["medications_list"] = st.text_input("If yes, please list them:", value=user_data["medical_history"]["medications_list"])
    user_data["medical_history"]["surgeries"] = st.radio("Have you had any surgeries in the past year?", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["medical_history"]["surgeries"] else "No")) == "Yes"
    if user_data["medical_history"]["surgeries"]:
        user_data["medical_history"]["surgeries_details"] = st.text_input("If yes, please specify:", value=user_data["medical_history"]["surgeries_details"])
    user_data["medical_history"]["allergies"] = st.radio("Do you have any allergies?", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["medical_history"]["allergies"] else "No")) == "Yes"
    if user_data["medical_history"]["allergies"]:
        user_data["medical_history"]["allergies_details"] = st.text_input("If yes, please specify:", value=user_data["medical_history"]["allergies_details"])

# Lifestyle and Habits Section
with st.expander("3. Lifestyle and Habits"):
    sleep_options = ["Select", "Less than 5", "5-7", "7-9", "More than 9"]
    sleep_index = sleep_options.index(user_data["lifestyle_habits"]["sleep_hours"]) if user_data["lifestyle_habits"]["sleep_hours"] in sleep_options else 0
    user_data["lifestyle_habits"]["sleep_hours"] = st.selectbox("How many hours of sleep do you get on average per night?", sleep_options, index=sleep_index)
    
    user_data["lifestyle_habits"]["smoking"] = st.radio("Do you smoke?", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["lifestyle_habits"]["smoking"] else "No")) == "Yes"
    user_data["lifestyle_habits"]["alcohol"] = st.radio("Do you consume alcohol?", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["lifestyle_habits"]["alcohol"] else "No")) == "Yes"
    if user_data["lifestyle_habits"]["alcohol"]:
        user_data["lifestyle_habits"]["alcohol_frequency"] = st.text_input("If yes, how often?", value=user_data["lifestyle_habits"]["alcohol_frequency"])
    user_data["lifestyle_habits"]["recreational_drugs"] = st.radio("Do you use recreational drugs?", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["lifestyle_habits"]["recreational_drugs"] else "No")) == "Yes"

# Fitness and Activity Level Section
with st.expander("4. Fitness and Activity Level"):
    fitness_level_options = ["Select", "Sedentary", "Lightly active", "Moderately active", "Very active"]
    fitness_level_index = fitness_level_options.index(user_data["fitness_activity"]["fitness_level"]) if user_data["fitness_activity"]["fitness_level"] in fitness_level_options else 0
    user_data["fitness_activity"]["fitness_level"] = st.selectbox("How would you rate your current fitness level?", fitness_level_options, index=fitness_level_index)
    
    exercise_days_options = ["Select", "0", "1-2", "3-4", "5-6", "7"]
    exercise_days_index = exercise_days_options.index(user_data["fitness_activity"]["exercise_days_per_week"]) if user_data["fitness_activity"]["exercise_days_per_week"] in exercise_days_options else 0
    user_data["fitness_activity"]["exercise_days_per_week"] = st.selectbox("How many days per week do you engage in physical exercise?", exercise_days_options, index=exercise_days_index)
    
    user_data["fitness_activity"]["exercise_types"] = st.text_input("What types of exercise do you usually do? (e.g., walking, running, weightlifting, yoga, other)", value=user_data["fitness_activity"]["exercise_types"])
    user_data["fitness_activity"]["injuries"] = st.radio("Do you have any injuries or physical limitations that affect your ability to exercise?", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["fitness_activity"]["injuries"] else "No")) == "Yes"
    if user_data["fitness_activity"]["injuries"]:
        user_data["fitness_activity"]["injuries_details"] = st.text_input("If yes, please specify:", value=user_data["fitness_activity"]["injuries_details"])

# Dietary Preferences Section
with st.expander("5. Dietary Preferences"):
    user_data["dietary_preferences"]["specific_diet"] = st.radio("Do you follow any specific diet or dietary restrictions?", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["dietary_preferences"]["specific_diet"] else "No")) == "Yes"
    if user_data["dietary_preferences"]["specific_diet"]:
        user_data["dietary_preferences"]["diet_details"] = st.text_input("If yes, please specify:", value=user_data["dietary_preferences"]["diet_details"])
    
    meals_per_day_options = ["Select", "1", "2", "3", "4+"]
    meals_per_day_index = meals_per_day_options.index(user_data["dietary_preferences"]["meals_per_day"]) if user_data["dietary_preferences"]["meals_per_day"] in meals_per_day_options else 0
    user_data["dietary_preferences"]["meals_per_day"] = st.selectbox("How many meals do you typically eat in a day?", meals_per_day_options, index=meals_per_day_index)
    
    user_data["dietary_preferences"]["dietary_supplements"] = st.radio("Do you consume any dietary supplements?", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["dietary_preferences"]["dietary_supplements"] else "No")) == "Yes"
    if user_data["dietary_preferences"]["dietary_supplements"]:
        user_data["dietary_preferences"]["supplements_list"] = st.text_input("If yes, please list them:", value=user_data["dietary_preferences"]["supplements_list"])

# Preferences and Goals Section
with st.expander("6. Preferences and Goals"):
    user_data["preferences_goals"]["preferences"] = st.text_input("Enter your dietary preferences (e.g., vegetarian, low-carb):", value=user_data["preferences_goals"]["preferences"])
    user_data["preferences_goals"]["goals"] = st.text_input("Enter your nutritional goals (e.g., muscle gain, weight loss):", value=user_data["preferences_goals"]["goals"])

# Consent and Privacy Section
with st.expander("7. Consent and Privacy"):
    user_data["consent_privacy"]["consent_data_collection"] = st.radio("I consent to the collection and use of my personal health data as outlined in the privacy policy.", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["consent_privacy"]["consent_data_collection"] else "No")) == "Yes"
    user_data["consent_privacy"]["consent_advice"] = st.radio("I agree to receive personalized health advice and recommendations from NINA AI.", ("Yes", "No"), index=("Yes", "No").index("Yes" if user_data["consent_privacy"]["consent_advice"] else "No")) == "Yes"

# Save button
if st.button("Save"):
    # Convert date_of_birth to string before saving
    if isinstance(user_data["personal_info"]["date_of_birth"], date):
        user_data["personal_info"]["date_of_birth"] = user_data["personal_info"]["date_of_birth"].strftime("%Y-%m-%d")
    write_user_data(user_data)
    st.success("Settings saved successfully!")
