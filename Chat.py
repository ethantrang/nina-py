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
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        else:
            time.sleep(5)

# List of food emojis
food_emojis = ["🍏", "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐", "🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑", "🥦", "🥬", "🥒", "🌶", "🌽", "🥕", "🧄", "🧅", "🥔", "🍠", "🥐", "🥯", "🍞", "🥖", "🥨", "🧀", "🥚", "🍳", "🧈", "🥞", "🧇", "🥓", "🥩", "🍗", "🍖", "🦴", "🌭", "🍔", "🍟", "🍕", "🥪", "🥙", "🧆", "🌮", "🌯", "🥗", "🥘", "🥫", "🍝", "🍜", "🍲", "🍛", "🍣", "🍱", "🥟", "🦪", "🍤", "🍙", "🍚", "🍘", "🍥", "🥮", "🍢", "🍡", "🍧", "🍨", "🍦", "🥧", "🧁", "🍰", "🎂", "🍮", "🍭", "🍬", "🍫", "🍿", "🍩", "🍪", "🌰", "🥜", "🍯"]

# Select a random food emoji
random_food_emoji = random.choice(food_emojis)

# Display the title with a random food emoji
st.title(f"{random_food_emoji} NINA")
st.subheader('Nutrition Info Navigation Assistant')

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
        f"Full Name: {user_data.get('personal_info', {}).get('full_name', 'N/A')}\n"
        f"Date of Birth: {user_data.get('personal_info', {}).get('date_of_birth', 'N/A')}\n"
        f"Gender: {user_data.get('personal_info', {}).get('gender', 'N/A')}\n"
        f"Height: {user_data.get('personal_info', {}).get('height', 'N/A')} cm\n"
        f"Weight: {user_data.get('personal_info', {}).get('weight', 'N/A')} kg\n"
        f"\nMedical History:\n"
        f"Chronic Conditions: {user_data.get('medical_history', {}).get('chronic_conditions', False)}\n"
        f"Conditions Details: {user_data.get('medical_history', {}).get('conditions_details', 'N/A')}\n"
        f"Medications: {user_data.get('medical_history', {}).get('medications', False)}\n"
        f"Medications List: {user_data.get('medical_history', {}).get('medications_list', 'N/A')}\n"
        f"Surgeries: {user_data.get('medical_history', {}).get('surgeries', False)}\n"
        f"Surgeries Details: {user_data.get('medical_history', {}).get('surgeries_details', 'N/A')}\n"
        f"Allergies: {user_data.get('medical_history', {}).get('allergies', False)}\n"
        f"Allergies Details: {user_data.get('medical_history', {}).get('allergies_details', 'N/A')}\n"
        f"\nLifestyle and Habits:\n"
        f"Sleep Hours: {user_data.get('lifestyle_habits', {}).get('sleep_hours', 'N/A')}\n"
        f"Smoking: {user_data.get('lifestyle_habits', {}).get('smoking', False)}\n"
        f"Alcohol: {user_data.get('lifestyle_habits', {}).get('alcohol', False)}\n"
        f"Alcohol Frequency: {user_data.get('lifestyle_habits', {}).get('alcohol_frequency', 'N/A')}\n"
        f"Recreational Drugs: {user_data.get('lifestyle_habits', {}).get('recreational_drugs', False)}\n"
        f"\nFitness and Activity Level:\n"
        f"Fitness Level: {user_data.get('fitness_activity', {}).get('fitness_level', 'N/A')}\n"
        f"Exercise Days Per Week: {user_data.get('fitness_activity', {}).get('exercise_days_per_week', 'N/A')}\n"
        f"Exercise Types: {user_data.get('fitness_activity', {}).get('exercise_types', 'N/A')}\n"
        f"Injuries: {user_data.get('fitness_activity', {}).get('injuries', False)}\n"
        f"Injuries Details: {user_data.get('fitness_activity', {}).get('injuries_details', 'N/A')}\n"
        f"\nDietary Preferences:\n"
        f"Specific Diet: {user_data.get('dietary_preferences', {}).get('specific_diet', False)}\n"
        f"Diet Details: {user_data.get('dietary_preferences', {}).get('diet_details', 'N/A')}\n"
        f"Meals Per Day: {user_data.get('dietary_preferences', {}).get('meals_per_day', 'N/A')}\n"
        f"Dietary Supplements: {user_data.get('dietary_preferences', {}).get('dietary_supplements', False)}\n"
        f"Supplements List: {user_data.get('dietary_preferences', {}).get('supplements_list', 'N/A')}\n"
        f"\nPreferences and Goals:\n"
        f"Preferences: {user_data.get('preferences_goals', {}).get('preferences', 'N/A')}\n"
        f"Goals: {user_data.get('preferences_goals', {}).get('goals', 'N/A')}\n"
        f"\nConsent and Privacy:\n"
        f"Consent Data Collection: {user_data.get('consent_privacy', {}).get('consent_data_collection', False)}\n"
        f"Consent Advice: {user_data.get('consent_privacy', {}).get('consent_advice', False)}\n"
    )

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything about nutrition!"):
    # Prepend user information to the first user message
    user_info_intro = format_user_data(user_data)
    
    # Add user information and message to chat history
    if not st.session_state.messages:
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



# import streamlit as st
# import requests
# import json
# import time
# from openai import OpenAI
# import random

# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# NUTRITIONIX_APP_ID = st.secrets["NUTRITIONIX_APP_ID"]
# NUTRITIONIX_API_KEY = st.secrets["NUTRITIONIX_API_KEY"]

# client = OpenAI(api_key=OPENAI_API_KEY)

# def get_nutritional_info(food_query):
#     url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
#     headers = {
#         'Content-Type': 'application/json',
#         'x-app-id': NUTRITIONIX_APP_ID,
#         'x-app-key': NUTRITIONIX_API_KEY
#     }
#     body = {"query": food_query}
#     response = requests.post(url, headers=headers, data=json.dumps(body))
#     if response.status_code == 200:
#         data = response.json()
#         def format_nutrient_info(food):
#             formatted = (
#                 f"Food Name: {food['food_name']}\n"
#                 f"Serving Quantity: {food['serving_qty']} {food['serving_unit']}\n"
#                 f"Serving Weight: {food['serving_weight_grams']} grams\n"
#                 f"Calories: {food['nf_calories']} kcal\n"
#                 f"Total Fat: {food['nf_total_fat']} g\n"
#                 f"Saturated Fat: {food['nf_saturated_fat']} g\n"
#                 f"Cholesterol: {food['nf_cholesterol']} mg\n"
#                 f"Sodium: {food['nf_sodium']} mg\n"
#                 f"Total Carbohydrate: {food['nf_total_carbohydrate']} g\n"
#                 f"Dietary Fiber: {food['nf_dietary_fiber']} g\n"
#                 f"Sugars: {food['nf_sugars']} g\n"
#                 f"Protein: {food['nf_protein']} g\n"
#                 f"Potassium: {food['nf_potassium']} mg\n"
#                 f"Phosphorus: {food['nf_p']} mg\n"
#                 f"Photo: {food['photo']['highres']}\n"
#             )
#             return formatted
#         return "\n".join([format_nutrient_info(food) for food in data['foods']])
#     else:
#         return f"Failed to retrieve nutritional information {response}"

# def get_assistant_response(chat_history):
#     assistant_id = "asst_Cqp74KANOBsCblHKiNEMXDAg"
#     thread = client.beta.threads.create()
    
#     for message in chat_history:
#         client.beta.threads.messages.create(
#             thread_id=thread.id,
#             role=message["role"],
#             content=message["content"]
#         )
    
#     run = client.beta.threads.runs.create(
#         thread_id=thread.id,
#         assistant_id=assistant_id,
#     )
    
#     while True:
#         time.sleep(5)
#         run_status = client.beta.threads.runs.retrieve(
#             thread_id=thread.id,
#             run_id=run.id
#         )
#         if run_status.status == 'completed':
#             messages = client.beta.threads.messages.list(
#                 thread_id=thread.id
#             )
#             for msg in messages.data:
#                 if msg.role == "assistant":
#                     return msg.content[0].text.value
#         elif run_status.status == 'requires_action':
#             required_actions = run_status.required_action.submit_tool_outputs.model_dump()
#             tool_outputs = []
#             for action in required_actions["tool_calls"]:
#                 func_name = action['function']['name']
#                 arguments = json.loads(action['function']['arguments'])
#                 if func_name == "get_nutritional_info":
#                     output = get_nutritional_info(food_query=arguments['food_query'])
#                     tool_outputs.append({
#                         "tool_call_id": action['id'],
#                         "output": json.dumps(output)
#                     })
#             client.beta.threads.runs.submit_tool_outputs(
#                 thread_id=thread.id,
#                 run_id=run.id,
#                 tool_outputs=tool_outputs
#             )
#         else:
#             time.sleep(5)


# # List of food emojis
# food_emojis = ["🍏", "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐", "🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑", "🥦", "🥬", "🥒", "🌶", "🌽", "🥕", "🧄", "🧅", "🥔", "🍠", "🥐", "🥯", "🍞", "🥖", "🥨", "🧀", "🥚", "🍳", "🧈", "🥞", "🧇", "🥓", "🥩", "🍗", "🍖", "🦴", "🌭", "🍔", "🍟", "🍕", "🥪", "🥙", "🧆", "🌮", "🌯", "🥗", "🥘", "🥫", "🍝", "🍜", "🍲", "🍛", "🍣", "🍱", "🥟", "🦪", "🍤", "🍙", "🍚", "🍘", "🍥", "🥮", "🍢", "🍡", "🍧", "🍨", "🍦", "🥧", "🧁", "🍰", "🎂", "🍮", "🍭", "🍬", "🍫", "🍿", "🍩", "🍪", "🌰", "🥜", "🍯"]

# # Select a random food emoji
# random_food_emoji = random.choice(food_emojis)

# # Display the title with a random food emoji
# st.title(f"{random_food_emoji} NINA")
# st.subheader('Nutrition Info Navigation Assistant')


# # Set a default model
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("Ask me anything about nutrition!"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     # Get assistant response
#     with st.chat_message("assistant"):
#         response = get_assistant_response(st.session_state.messages)
#         st.markdown(response)
    
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})

