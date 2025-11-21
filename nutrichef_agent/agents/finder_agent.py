from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from nutrichef_agent.tools.spoonacular_tools import search_recipes
from nutrichef_agent.config import retry_config
from nutrichef_agent.config import LLM_MODEL_NAME

# It takes the ingredients list and uses the tool to find raw recipes.
finder_agent = Agent(
    name="finder_agent",
    model=Gemini(
        model=LLM_MODEL_NAME,
        retry_options=retry_config
    ),    
    instruction="""
        You are a Finder Agent for a nutrition app. 
        Your job is to find potential recipes using `search_recipes` tool based on ingredients {parsed_constraints}

        1. Take the ingredients, cooking method (if present), other constraints (like max calories) from {parsed_constraints}.
        2. Use the `search_recipes` tool to find matching dishes. 
            Pass ingredients to the `ingredients` parameter.
            Pass the cooking method (e.g. boil) to the `method` parameter.
            
        3. Output the list of Recipe IDs found by the tool.

        OUTPUT RULES:
        1. You must return ONLY a valid JSON object.
        2. Do not include markdown formatting (no ```json or ```).
        3. Structure: {"status": [X], "recipe_id": [X, X]}
            If there's error from the `search_recipes` tool, return `status` as `failed`.
            If everything is good, return `status` as `success`.

    """,
    tools = [search_recipes],
    output_key= "recipe_ids"
)