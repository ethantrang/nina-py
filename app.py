import json
from fastapi import FastAPI, HTTPException
from mangum import Mangum
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import time
from pydantic import BaseModel
import uvicorn

load_dotenv()

app = FastAPI()
handler = Mangum(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

class ChatHistory(BaseModel):
    chat_history: list

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

@app.post("/chat/")
async def chat_endpoint(chat_history: ChatHistory):
    try:
        response = get_assistant_response(chat_history.chat_history)
        return {
            "role": "assistant",
            "content": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=True)

