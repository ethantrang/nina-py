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
        nutrients = "\n".join([f"{n['attr_id']}: {n['value']}" for n in food['full_nutrients']])
        alt_measures = "\n".join([f"{m['measure']} ({m['serving_weight']} grams)" for m in food['alt_measures']])
        
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
            # f"Consumed At: {food['consumed_at']}\n"
            # f"Full Nutrients:\n{nutrients}\n"
            # f"Alternative Measures:\n{alt_measures}\n"
            f"Photo: {food['photo']['highres']}\n"
        )
        return formatted

    return "\n".join([format_nutrient_info(food) for food in data['foods']])

result = get_nutritional_info("pho")

print(result)