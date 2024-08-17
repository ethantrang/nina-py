#Chat.py

import streamlit as st
import requests
import json
import time
from openai import OpenAI
import random
import os

# Define the path to the JSON file
USER_DATA_FILE = "user_data.json"

# Load API keys
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
NUTRITIONIX_APP_ID = st.secrets["NUTRITIONIX_APP_ID"]
NUTRITIONIX_API_KEY = st.secrets["NUTRITIONIX_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to read user data from the JSON file
def read_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to get nutritional information
def get_nutritional_info(food_query):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': NUTRITIONIX_APP_ID,
        'x-app-key': NUTRITIONIX_API_KEY
    }
    body = {"query": food_query}
    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        data = response.json()
        def format_nutrient_info(food):
            formatted = (
                f"Food Name: {food['food_name']}\n"
                f"Serving Quantity: {food['serving_qty']} {food['serving_unit']}\n"
                f"Serving Weight: {food['serving_weight_grams']} grams\n"
                f"Calories: {food['nf_calories']} kcal\n"
                f"Total Fat: {food['nf_total_fat']} g\n"
                f"Saturated Fat: {food['nf_saturated_fat']} g\n"
                f"Cholesterol: {food['nf_cholesterol']} mg\n"
                f"Sodium: {food['nf_sodium']} mg\n"
                f"Total Carbohydrate: {food['nf_total_carbohydrate']} g\n"
                f"Dietary Fiber: {food['nf_dietary_fiber']} g\n"
                f"Sugars: {food['nf_sugars']} g\n"
                f"Protein: {food['nf_protein']} g\n"
                f"Potassium: {food['nf_potassium']} mg\n"
                f"Phosphorus: {food['nf_p']} mg\n"
                f"Photo: {food['photo']['highres']}\n"
            )
            return formatted
        return "\n".join([format_nutrient_info(food) for food in data['foods']])
    else:
        return f"Failed to retrieve nutritional information: {response}"

# Function to get exercise information
def get_exercise_info(exercise_query):
    url = "https://trackapi.nutritionix.com/v2/natural/exercise"
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': NUTRITIONIX_APP_ID,
        'x-app-key': NUTRITIONIX_API_KEY
    }
    body = {"query": exercise_query}
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        def format_exercise_info(exercise):
            formatted = (
                f"Exercise: {exercise['name']}\n"
                f"Duration: {exercise['duration_min']} minutes\n"
                f"Calories Burned: {exercise['nf_calories']} kcal\n"
                f"MET: {exercise['met']}\n"
            )
            return formatted
        return "\n".join([format_exercise_info(exercise) for exercise in data['exercises']])
    else:
        return f"Failed to retrieve exercise information: {response.text}"

# Function to get assistant response
def get_assistant_response(chat_history):
    assistant_id = "asst_Cqp74KANOBsCblHKiNEMXDAg"
    thread = client.beta.threads.create()
    
    for message in chat_history:
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role=message["role"],
            content=message["content"]
        )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
    
    while True:
        time.sleep(5)
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            for msg in messages.data:
                if msg.role == "assistant":
                    return msg.content[0].text.value
        elif run_status.status == 'requires_action':
            required_actions = run_status.required_action.submit_tool_outputs.model_dump()
            tool_outputs = []
            for action in required_actions["tool_calls"]:
                func_name = action['function']['name']
                arguments = json.loads(action['function']['arguments'])
                if func_name == "get_nutritional_info":
                    output = get_nutritional_info(food_query=arguments['food_query'])
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": json.dumps(output)
                    })
                elif func_name == "get_exercise_info":
                    output = get_exercise_info(exercise_query=arguments['exercise_query'])
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": json.dumps(output)
                    })
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        else:
            time.sleep(5)


st.sidebar.header("Welcome to Nina!")

# List of food emojis
food_emojis = ["🍏", "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐", "🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑", "🥦", "🥬", "🥒", "🌶", "🌽", "🥕", "🧄", "🧅", "🥔", "🍠", "🥐", "🥯", "🍞", "🥖", "🥨", "🧀", "🥚", "🍳", "🧈", "🥞", "🧇", "🥓", "🥩", "🍗", "🍖", "🦴", "🌭", "🍔", "🍟", "🍕", "🥪", "🥙", "🧆", "🌮", "🌯", "🥗", "🥘", "🥫", "🍝", "🍜", "🍲", "🍛", "🍣", "🍱", "🥟", "🦪", "🍤", "🍙", "🍚", "🍘", "🍥", "🥮", "🍢", "🍡", "🍧", "🍨", "🍦", "🥧", "🧁", "🍰", "🎂", "🍮", "🍭", "🍬", "🍫", "🍿", "🍩", "🍪", "🌰", "🥜", "🍯"]

# Select a random food emoji
random_food_emoji = random.choice(food_emojis)

# Display the title with a random food emoji
st.title(f"{random_food_emoji} Chat about Nutrition & Exercise ")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load current user data
user_data = read_user_data()

# Function to format user data for the assistant
def format_user_data(user_data):
    return (
        f"User's Personal Information:\n"
        f"Name: {user_data.get('basic_info', {}).get('name', 'N/A')}\n"
        f"Age: {user_data.get('basic_info', {}).get('age', 'N/A')}\n"
        f"Gender: {user_data.get('basic_info', {}).get('gender', 'N/A')}\n"
        f"Height: {user_data.get('basic_info', {}).get('height', 'N/A')} cm\n"
        f"Weight: {user_data.get('basic_info', {}).get('weight', 'N/A')} kg\n"
        f"\nHealth and Fitness Information:\n"
        f"Activity Level: {user_data.get('health_fitness', {}).get('activity_level', 'N/A')}\n"
        f"Goals: {user_data.get('health_fitness', {}).get('goals', 'N/A')}\n"
        f"Types of Activity: {user_data.get('health_fitness', {}).get('activity_types', 'N/A')}\n"
        f"Medical Conditions: {user_data.get('health_fitness', {}).get('medical_conditions', 'N/A')}\n"
        f"Allergies: {user_data.get('health_fitness', {}).get('allergies', 'N/A')}\n"
        f"Dietary Preferences: {user_data.get('health_fitness', {}).get('dietary_preferences', 'N/A')}\n"
        f"\nLifestyle Information:\n"
        f"Sleep: {user_data.get('lifestyle', {}).get('sleep', 'N/A')}\n"
        f"Perceived Stress Levels: {user_data.get('lifestyle', {}).get('stress_level', 'N/A')}\n"
        f"\nFitness and Nutrition Data:\n"
        f"Workout History: {user_data.get('fitness_nutrition_data', {}).get('workout_history', 'N/A')}\n"
        f"Dietary Intake: {user_data.get('fitness_nutrition_data', {}).get('dietary_intake', 'N/A')}\n"
        f"Water Intake: {user_data.get('fitness_nutrition_data', {}).get('water_intake', 'N/A')}\n"
        f"Supplement Use: {user_data.get('fitness_nutrition_data', {}).get('supplement_use', 'N/A')}\n"
        f"\nTechnical and Engagement Data:\n"
        f"Preferences: {user_data.get('technical_engagement', {}).get('preferences', 'N/A')}\n"
        f"\nAdvanced Data (optional):\n"
        f"Heart Rate: {user_data.get('advanced_data', {}).get('heart_rate', 'N/A')}\n"
        f"Estimated Daily Steps Tracking: {user_data.get('advanced_data', {}).get('daily_steps', 'N/A')}\n"
        f"\nPrivacy and Consent:\n"
        f"Data Collection Consent: {'Yes' if user_data.get('privacy_consent', {}).get('data_collection_consent', False) else 'No'}\n"
        f"Data Sharing Preferences: {'Yes' if user_data.get('privacy_consent', {}).get('data_sharing_preferences', False) else 'No'}\n"
    )

# Display welcome message if chat history is empty
if not st.session_state.messages:
    welcome_message = (
        "Hello! I'm Nina, your Nutrition Info Navigation Assistant. 😊\n\n"
        "I'm here to help you with personalized meal suggestions, post-workout nutrition advice, health and wellness tracking, and exercise information. "
        "Feel free to ask me about the nutritional value of foods, your workout details, or any other questions related to your dietary and fitness goals. "
        "Let's get started!"
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user" and "User's Personal Information" in message["content"]:
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything about nutrition!"):
    # Prepend user information to the first user message if not already done
    if not st.session_state.messages:
        user_info_intro = format_user_data(user_data)
        st.session_state.messages.append({"role": "user", "content": user_info_intro})
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        response = get_assistant_response(st.session_state.messages)
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

