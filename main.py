import streamlit as st
import requests
import json
import time
from openai import OpenAI


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
NUTRITIONIX_APP_ID = st.secrets["NUTRITIONIX_APP_ID"]
NUTRITIONIX_API_KEY = st.secrets["NUTRITIONIX_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

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
        return f"Failed to retrieve nutritional information {response}"

def get_assistant_response(user_message):
    assistant_id = "asst_Cqp74KANOBsCblHKiNEMXDAg"
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
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



st.title("NINA")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        response = get_assistant_response(prompt)
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


# import streamlit as st
# from openai import OpenAI

# st.title("NINA")

# # Set OpenAI API key from Streamlit secrets
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
# if prompt := st.chat_input("What is up?"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         stream = client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=[
#                 # {"role": "system", "content": SYSTEM_PROMPT}
#             ] + [
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         )
#         response = st.write_stream(stream)
#     st.session_state.messages.append({"role": "assistant", "content": response})