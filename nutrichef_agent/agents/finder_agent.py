from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from nutrichef_agent.agents.spoonacular_tools import search_recipes_by_ingredients
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
        Your job is to find potential recipes using search_recipes_by_ingredients() tool based on ingredients {parsed_constraints}

        1. Take the ingredients and constraints provided.
        2. Use the `search_recipes_by_ingredients` tool to find matching dishes.
        3. Output the list of Recipe IDs found by the tool.

        If there's error from the tool, summarize the reason.

    """,
    tools = [search_recipes_by_ingredients],
    output_key= "recipe_ids"
)