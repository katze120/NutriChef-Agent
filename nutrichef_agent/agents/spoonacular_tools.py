import requests
import json
from ..config import SPOONACULAR_API_KEY # Relative import from parent directory

SPOONACULAR_BASE_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
SPOONACULAR_HEADERS = {
    "x-rapidapi-key": SPOONACULAR_API_KEY,
    "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

def search_recipes_by_ingredients(ingredients: str, number: int = 5, max_calories: int = 0) -> list[dict]:
    """
    Searches for recipes based on a list of ingredients.
    Args:
        ingredients: A comma-separated string of ingredients (e.g., "chicken,broccoli,onion").
        number: The maximum number of recipes to return.
        max_calories: Optional. The maximum calorie count per serving for the recipes.
    Returns:
        A JSON list of recipes, each with 'id', 'title', 'image', 'usedIngredientCount', 'missedIngredientCount'.
    """
    print("[FinderAgent] Searching for recipes..")
    url = f"{SPOONACULAR_BASE_URL}/recipes/findByIngredients"
    querystring = {
        "ingredients": ingredients,
        "number": str(number),
        "ignorePantry": "true",
        "ranking": "1" # "1" = maximize used ingredients
    }
    if max_calories != 0:
        querystring["maxCalories"] = str(max_calories)
    recipes = []
    response = requests.get(url, headers=SPOONACULAR_HEADERS, params=querystring)
    if response.status_code == 200:
        # Return just the essential data to save context window
        recipes = [{"id": r['id'], "title": r['title']} for r in response.json()]
    print("[FinderAgent] Found recipes: ", recipes)
    return recipes

def get_recipe_information(recipe_ids: list[int]) -> list[dict]:
    """
    Retrieves detailed information for specific recipes, including nutrition.
    Args:
        recipe_ids: The list of IDs of the recipe to retrieve.
    Returns:
        A JSON objects containing detailed recipe information, instructions, and nutrition.
    """
    print("[NutritionistAgent] Searching for nutrition data..")
    nutrition_data = []
    for r_id in recipe_ids:

        url = f"{SPOONACULAR_BASE_URL}/recipes/{r_id}/information"
        querystring = {"includeNutrition": "true"}
        response = requests.get(url, headers=SPOONACULAR_HEADERS, params=querystring)
        if response.status_code == 200:
            data = response.json()
            nutrients = data.get('nutrition', {}).get('nutrients', [])
            cal = next((n['amount'] for n in nutrients if n['name'] == 'Calories'), 0)
            prot = next((n['amount'] for n in nutrients if n['name'] == 'Protein'), 0)
                
            nutrition_data.append({
                "title": data.get('title'),
                "ready_in_minutes": data.get('readyInMinutes'),
                "calories": cal,
                "protein": f"{prot}g",
                "link": data.get('sourceUrl'),
                "full_data": data
            })
    print("[NutritionistAgent] Enriched recipes with nutrition data: ", nutrition_data)
    return nutrition_data