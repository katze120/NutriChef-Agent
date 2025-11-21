import requests
import json
from ..config import SPOONACULAR_API_KEY # Relative import from parent directory

SPOONACULAR_BASE_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
SPOONACULAR_HEADERS = {
    "x-rapidapi-key": SPOONACULAR_API_KEY,
    "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

def search_recipes(ingredients: str, method: str = "", number: int = 5, max_calories: int = 0) -> list[dict]:
    """
    Searches for recipes based on a list of ingredients AND an optional cooking method
    using the Spoonacular complexSearch API for greater flexibility.
    Args:
        ingredients: A comma-separated string of ingredients (e.g., "chicken,broccoli,onion").
        method: Optional. A keyword or cooking method (e.g., "boil", "fry", "grilled").
        number: The maximum number of recipes to return.
        max_calories: Optional. The maximum calorie count per serving for the recipes.
    Returns:
        A JSON list of recipes, each with 'id', 'title'.
    """
    url = f"{SPOONACULAR_BASE_URL}/recipes/complexSearch"
    querystring = {
        "includeIngredients": ingredients, # Used for ingredients
        "number": str(number),
        "sort": "min-missing-ingredients", # Prioritize recipes that use the available ingredients
        "fillIngredients": "true" 
    }

    if max_calories != 0:
        querystring["maxCalories"] = str(max_calories)

    recipes = []
    print("[FinderAgent] Searching for recipes with query: ", querystring)
    response = requests.get(url, headers=SPOONACULAR_HEADERS, params=querystring)
    if response.status_code == 200:
        # complexSearch returns results in the 'results' key
        results = response.json().get('results', [])
        # Return just the essential data to save context window
        recipes = [{"id": r['id'], "title": r['title']} for r in results]
    print("[FinderAgent] Found recipes: ", recipes)
    return recipes

def get_recipe_information(recipe_ids: list[int]) -> list[dict]:
    """
    Retrieves detailed information for specific recipes, including nutrition, 
    using the efficient bulk endpoint.
    
    Args:
        recipe_ids: The list of IDs of the recipes to retrieve (e.g., [123, 456]).
    
    Returns:
        A list of dictionaries containing key recipe and nutrition data, 
        or an error dictionary if the API call fails.
    """
    print("[NutritionistAgent] Searching for nutrition data (BULK request).. IDs: " + str(recipe_ids))
    nutrition_data = []

    # 1. Prepare the Bulk Request URL and Query Parameters
    # Convert list of integers to a comma-separated string: "123,456,789"
    recipe_id_string = ",".join(map(str, recipe_ids))
    url = f"{SPOONACULAR_BASE_URL}/recipes/informationBulk"
    querystring = {
        "ids": recipe_id_string,
        "includeNutrition": "true"
    }

    try:
        # 2. Make a single request for all IDs
        response = requests.get(url, headers=SPOONACULAR_HEADERS, params=querystring, timeout=10)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        
        recipes = response.json()
        
        # 3. Process the list of recipes returned by the bulk endpoint
        for data in recipes:
            # Helper logic to safely extract Calories and Protein
            nutrients = data.get('nutrition', {}).get('nutrients', [])
            
            cal = next((n['amount'] for n in nutrients if n['name'] == 'Calories'), 0)
            prot = next((n['amount'] for n in nutrients if n['name'] == 'Protein'), 0)

            nutrition_data.append({
                "title": data.get('title'),
                "ready_in_minutes": data.get('readyInMinutes'),
                "calories": cal,
                "link": data.get('sourceUrl'),
                "instructions": data.get('instructions', 'Instructions not available')
            })
            
    except requests.exceptions.HTTPError as errh:
        # Handle 4xx or 5xx status codes
        print(f"[NutritionistAgent] HTTP Error: {errh}")
        return [{"error": f"API returned HTTP error: {response.status_code}."}]
    except requests.exceptions.RequestException as err:
        # Handle Connection, Timeout, or other requests library errors
        print(f"[NutritionistAgent] Network/Connection Error: {err}")
        return [{"error": f"Failed to connect to Spoonacular API: {err}"}]

    print("[NutritionistAgent] Enriched recipes with nutrition data: ", nutrition_data)
    return nutrition_data