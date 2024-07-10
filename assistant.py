# assistant.py

import requests
import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load API keys from environment variables
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
# NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")

OPENAI_API_KEY = "sk-proj-Y9BwiJjmueVA1ZDgR8k8T3BlbkFJeJpFDqpiwLIQnFSdje5O"
NUTRITIONIX_APP_ID = "65e62b92"
NUTRITIONIX_API_KEY = "1e1774e57c8a75b260b499343544f159"

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

if __name__ == "__main__":
    user_message = "How many calories in a pizza"
    response = get_assistant_response(user_message)
    print(response)


# import requests

# import os
# import json
# import time
# from openai import OpenAI
# from dotenv import load_dotenv
# load_dotenv()

# # Load API keys from environment variables
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
# NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")

# client = OpenAI(api_key=OPENAI_API_KEY)

# tools = [
#     {
#         "name": "get_nutritional_info",
#         "description": "Accepts a query about food items and their quantities and returns their nutritional information",
#         "parameters": {
#             "type": "object",
#             "properties": {
#             "food_query": {
#                 "type": "string",
#                 "description": "The query containing the name of the foods and their quantities"
#             }
#             },
#             "required": [
#                 "food_query"
#             ]
#         }
#     }
# ]

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
#             nutrients = "\n".join([f"{n['attr_id']}: {n['value']}" for n in food['full_nutrients']])
#             alt_measures = "\n".join([f"{m['measure']} ({m['serving_weight']} grams)" for m in food['alt_measures']])
            
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
#                 # f"Consumed At: {food['consumed_at']}\n"
#                 # f"Full Nutrients:\n{nutrients}\n"
#                 # f"Alternative Measures:\n{alt_measures}\n"
#                 f"Photo: {food['photo']['highres']}\n"
#             )
#             return formatted
#         return "\n".join([format_nutrient_info(food) for food in data['foods']])
#     else:
#         return f"Failed to retrieve nutritional information {response}"

# def create_assistants():
    
#     #retrieve the assitant_id 
#     assistant_id = "asst_Cqp74KANOBsCblHKiNEMXDAg"
#     assistant = client.beta.assistants.retrieve(assistant_id)  
#     print(f"Assistant created with ID: {assistant_id}")  
    
#     #step 2: Create a thread 
#     print("Creating a Thread for a new user conversation.....")
#     thread = client.beta.threads.create()
#     print(f"Thread created with ID: {thread.id}")

#     #step add a message to the thread 
#     user_message="How many calories in a pizza"
#     print(f"Adding user's message to the Thread: {user_message}")
#     message = client.beta.threads.messages.create(
#         thread_id=thread.id,
#         role="user",
#         content=user_message
#     )
#     print("Message added to the Thread.")

#     # Step 4: Run the Assistant
#     print("Running the Assistant to generate a response...")
#     run = client.beta.threads.runs.create(
#         thread_id=thread.id,
#         assistant_id=assistant.id,
#         # instructions="Please provide the nutritional information"
#     )
#     print(f"Run created with ID: {run.id} and status: {run.status}")
#     print(run.model_dump_json(indent=4))

#     # Step 5: Display the Assistant's Response
#     # Poll the Run status until it's completed
#     while True:
#        # Wait for 5 seconds
#         time.sleep(5)

#          # Retrieve the run status
#         run_status = client.beta.threads.runs.retrieve(
#             thread_id=thread.id,
#             run_id=run.id
#         )
#         print(run_status.model_dump_json(indent=4))

#     # If run is completed, get messages
#         if run_status.status == 'completed':
#             messages = client.beta.threads.messages.list(
#                 thread_id=thread.id
#         )

#         # Loop through messages and print content based on role
#             for msg in messages.data:
#                 role = msg.role
#                 content = msg.content[0].text.value
#                 print(f"{role.capitalize()}: {content}")
            
#               # save run steps to json file
#             run_steps = client.beta.threads.runs.steps.list(
#                 thread_id=thread.id,
#                 run_id=run.id
#             )
#             print(run_steps)

#             break
#         elif run_status.status == 'requires_action':
#             print("Function Calling")
#             required_actions = run_status.required_action.submit_tool_outputs.model_dump()
#             print( "Run Required Action State")
#             print(required_actions)
#             tool_outputs = []
#             for action in required_actions["tool_calls"]:
#                 func_name = action['function']['name']
#                 arguments = json.loads(action['function']['arguments'])
         
#                 if func_name == "get_nutritional_info":
#                     output = get_nutritional_info(food_query=arguments['food_query'])
#                     output_string = json.dumps(output)
#                     tool_outputs.append({
#                     "tool_call_id": action['id'],
#                     "output": output_string
#                 })
#                 else:
#                     raise ValueError(f"Unknown function: {func_name}")
                
#             print("Tool Outputs")
#             print(tool_outputs)
#             print("Submitting outputs back to the Assistant...")
#             client.beta.threads.runs.submit_tool_outputs(
#             thread_id=thread.id,
#             run_id=run.id,
#             tool_outputs=tool_outputs
#             )
#         else:
#             print("Waiting for the Assistant to process...")
#             time.sleep(5)

# if __name__ == "__main__":
#    create_assistants()