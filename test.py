import requests
import json

def get_nutritional_info(food_query):

    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': '65e62b92',
        'x-app-key': '1e1774e57c8a75b260b499343544f159'
    }
    body = {
        "query": f"{food_query}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))

    data = json.loads(response.text)

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
        )
        return formatted

    return "\n".join([format_nutrient_info(food) for food in data['foods']])

# result = get_nutritional_info("pho")



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

# result = search_food("burger king whopper")
# print(result)

def get_nutrition_info(upc_or_nix_item_id, search_type='nix_item_id'):
    url = "https://trackapi.nutritionix.com/v2/search/item"
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': "65e62b92",
        'x-app-key': "1e1774e57c8a75b260b499343544f159"
    }
    params = {
        search_type: upc_or_nix_item_id
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    food = data['foods'][0]
    return format_nutrient_info(food)

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
    )
    return formatted

# Example usage:
upc_or_nix_item_id = "889417000045"  # Or a valid nix_item_id
result = get_nutrition_info(upc_or_nix_item_id, search_type='upc')
print(result)


def get_nutrition_for_query(query):
    # Search for the food item
    search_url = "https://trackapi.nutritionix.com/v2/search/instant"
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': "65e62b92",
        'x-app-key': "1e1774e57c8a75b260b499343544f159"
    }
    search_params = {
        'query': query
    }
    
    search_response = requests.get(search_url, headers=headers, params=search_params)
    search_data = search_response.json()

    # Check if there are branded foods available
    if search_data.get('branded'):
        first_item = search_data['branded'][0]
        nix_item_id = first_item['nix_item_id']
    else:
        return "No branded food items found."

    # Get nutritional info for the first branded item found
    nutrition_url = "https://trackapi.nutritionix.com/v2/search/item"
    nutrition_params = {
        'nix_item_id': nix_item_id
    }
    
    nutrition_response = requests.get(nutrition_url, headers=headers, params=nutrition_params)
    nutrition_data = nutrition_response.json()
    food = nutrition_data['foods'][0]
    
    return format_nutrient_info(food)

def format_nutrient_info(food):
    formatted = (
        f"Food Name: {food['food_name']}\n"
        f"Brand Name: {food.get('brand_name', 'N/A')}\n"
        f"Serving Quantity: {food['serving_qty']} {food['serving_unit']}\n"
        f"Serving Weight: {food['serving_weight_grams']} grams\n"
        f"Calories: {food['nf_calories']} kcal\n"
        f"Total Fat: {food['nf_total_fat']} g\n"
        f"Saturated Fat: {food.get('nf_saturated_fat', 'N/A')} g\n"
        f"Cholesterol: {food.get('nf_cholesterol', 'N/A')} mg\n"
        f"Sodium: {food.get('nf_sodium', 'N/A')} mg\n"
        f"Total Carbohydrate: {food['nf_total_carbohydrate']} g\n"
        f"Dietary Fiber: {food.get('nf_dietary_fiber', 'N/A')} g\n"
        f"Sugars: {food.get('nf_sugars', 'N/A')} g\n"
        f"Protein: {food['nf_protein']} g\n"
        f"Potassium: {food.get('nf_potassium', 'N/A')} mg\n"
        f"Phosphorus: {food.get('nf_p', 'N/A')} mg\n"
    )
    return formatted

# # Example usage:
# result = get_nutrition_for_query("Nutella")
# print(result)

def get_exercise_info(exercise_query):
    url = "https://trackapi.nutritionix.com/v2/natural/exercise"
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': "65e62b92",
        'x-app-key': "1e1774e57c8a75b260b499343544f159"
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
    
# Example usage:
exercise_query = "ran 3 miles"
result = get_exercise_info(exercise_query)
print(result)